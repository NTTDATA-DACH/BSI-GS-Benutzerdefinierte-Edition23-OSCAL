import asyncio
import json
import logging
from typing import Dict, Any, List

import vertexai
from jsonschema import validate, ValidationError
from vertexai.generative_models import (
    GenerativeModel,
    GenerationConfig,
    FinishReason,
)
from config import GCP_PROJECT_ID, TEST_MODE

# Logger setup is handled in the main script, we just get it here.
logger = logging.getLogger(__name__)

# --- Model Configuration ---
MODEL_NAME = "gemini-2.5-pro"
MAX_OUTPUT_TOKENS = 65536
RETRY_ATTEMPTS = 5
MAX_CONCURRENT_REQUESTS = 10

# Initialize Vertex AI
try:
    # Set the location to "global" as requested
    vertexai.init(project=GCP_PROJECT_ID, location="global")
    logger.info("Vertex AI initialized successfully for project %s in location 'global'.", GCP_PROJECT_ID)
except Exception as e:
    logger.critical(f"Failed to initialize Vertex AI: {e}", exc_info=TEST_MODE)
    raise


def load_prompt_and_schema(prompt_path: str, schema_path: str) -> tuple[str, dict]:
    """Loads a prompt and a JSON schema from local files."""
    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            prompt = f.read()
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)
        return prompt, schema
    except FileNotFoundError as e:
        logger.error(f"Could not find a required file: {e.filename}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Could not parse JSON schema file at {schema_path}: {e}")
        raise


# Load prompt and schema once on module import
BATCH_PRACTICE_PROMPT, BATCH_PRACTICE_STUB_SCHEMA = load_prompt_and_schema(
    "prompts/batch_practice_prompt.txt",
    "schemas/batch_practice_stub.schema.json"
)


async def generate_practices_for_batch(batch_of_controls: List[Dict[str, Any]]) -> List[Dict[str, Any] | None]:
    """
    Generates practice and CIA props for a batch of controls in a single API call.

    Args:
        batch_of_controls: A list of control object dictionaries.

    Returns:
        A list of generated data dictionaries, or None for failures.
        The list length matches the input batch length.
    """
    # Create a list of minimal control stubs to send to the model
    control_stubs = [
        {"id": control.get("id", "Unknown ID"), "title": control.get("title")}
        for control in batch_of_controls
    ]

    # Prepare the prompt with the batch of stubs and the schema
    prompt = (f"{BATCH_PRACTICE_PROMPT}\n\n"
              f"Control Data Array:\n{json.dumps(control_stubs, indent=2)}\n\n"
              f"Schema for your JSON response array:\n{json.dumps(BATCH_PRACTICE_STUB_SCHEMA, indent=2)}")

    model = GenerativeModel(MODEL_NAME)
    generation_config = GenerationConfig(
        max_output_tokens=MAX_OUTPUT_TOKENS,
        response_mime_type="application/json",
        temperature=0.1,
    )

    logger.debug(f"Generating practices for batch of {len(batch_of_controls)} controls.")

    for attempt in range(RETRY_ATTEMPTS):
        try:
            response = await model.generate_content_async(
                contents=prompt,
                generation_config=generation_config,
            )
            
            # --- Detailed Gemini Response Validation ---
            if not response.candidates:
                finish_reason_str = response.prompt_feedback.block_reason.name if response.prompt_feedback.block_reason else "UNKNOWN"
                logger.warning(f"Attempt {attempt + 1}: No candidates returned. Finish Reason: {finish_reason_str}")
                await asyncio.sleep(2 ** attempt)
                continue
            
            finish_reason = response.candidates[0].finish_reason
            # CORRECTED LINE: The successful finish reason is 'STOP', not 'OK'.
            if finish_reason != FinishReason.STOP:
                logger.warning(f"Attempt {attempt + 1}: Model finished with non-OK reason: {finish_reason.name}")
                if finish_reason in [FinishReason.SAFETY, FinishReason.RECITATION]:
                    logger.error(f"Generation stopped permanently due to {finish_reason.name}. Cannot retry batch.")
                    return [None] * len(batch_of_controls)
                await asyncio.sleep(2 ** attempt)
                continue

            raw_text = response.text.strip()
            model_output = json.loads(raw_text)

            validate(instance=model_output, schema=BATCH_PRACTICE_STUB_SCHEMA)

            if len(model_output) != len(batch_of_controls):
                logger.warning(
                    f"Attempt {attempt + 1}: Model returned {len(model_output)} items, but batch size was {len(batch_of_controls)}. Retrying."
                )
                await asyncio.sleep(2 ** attempt)
                continue

            # Results are mapped back by id (not position), so every requested
            # id must be present exactly once.
            requested_ids = {control.get("id") for control in batch_of_controls}
            returned_ids = {item.get("id") for item in model_output}
            if returned_ids != requested_ids:
                logger.warning(
                    f"Attempt {attempt + 1}: Returned ids do not match requested ids "
                    f"(missing: {requested_ids - returned_ids}, unexpected: {returned_ids - requested_ids}). Retrying."
                )
                await asyncio.sleep(2 ** attempt)
                continue

            logger.info(f"Successfully generated and validated data for batch of {len(batch_of_controls)} controls.")
            return model_output

        except (json.JSONDecodeError, ValueError) as e:
            logger.warning(f"Attempt {attempt + 1}/{RETRY_ATTEMPTS}: Failed to decode or process JSON response. Error: {e}")
            await asyncio.sleep(2 ** attempt)
        except ValidationError as e:
            logger.error(f"Schema validation failed for batch: {e.message}", exc_info=TEST_MODE)
            await asyncio.sleep(2 ** attempt)
        except Exception as e:
            logger.error(f"Unexpected error during model generation on attempt {attempt + 1}: {e}", exc_info=TEST_MODE)
            await asyncio.sleep(2 ** attempt)
            
    logger.error(f"All {RETRY_ATTEMPTS} retry attempts failed for a batch. Returning failures for this batch.")
    return [None] * len(batch_of_controls)