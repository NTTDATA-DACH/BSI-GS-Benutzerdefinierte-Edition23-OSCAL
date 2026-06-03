import logging
import json
import asyncio
import datetime
import httpx
from typing import List, Dict, Any, Optional

# New SDK Imports
from google import genai
from google.genai import types, errors

# Third-party Imports
from jsonschema import validate, ValidationError

# App Config
from config import app_config
from constants import *

logger = logging.getLogger(__name__)

class AiClient:
    """A client for all Vertex AI model interactions, using the google-genai SDK (v1.52.0)."""

    def __init__(self, config):
        """
        Initializes the AiClient using the Unified Vertex AI Client.

        Args:
            config: The application configuration object.
        """
        self.config = config
        
        with open(PROMPT_CONFIG_PATH, 'r', encoding='utf-8') as f:
            prompt_config = json.load(f)
        
        base_system_message = prompt_config.get("system_message", "")
        if not base_system_message:
            logger.warning("System message is empty. AI calls will not have a predefined persona.")

        # Append the current date to the system prompt
        current_date = datetime.date.today().strftime("%Y-%m-%d")
        self.system_message = f"{base_system_message}\n\nImportant: Today's date is {current_date}."

        # Initialize the Unified Client with ADC (vertexai=True)
        # We do not need to cache model objects anymore; the client handles the connection.
        logger.info(f"Initializing Google GenAI Client for project '{config.gcp_project_id}' in region '{config.region}'.")
        self.client = genai.Client(
            vertexai=True,
            project=config.gcp_project_id,
            location=config.region,
            http_options={'api_version': 'v1'}
        )
        
        logger.debug(f"System Message Context includes today's date: {current_date}")

    def create_context_cache(self, content: str, system_instruction: str, model_override: Optional[str] = None) -> Optional[str]:
        """Creates an explicit Vertex AI context cache for a large, reused grounding corpus.

        Implicit caching does not engage for this model/region, so a fixed corpus that every
        request shares (e.g. the stripped ED2023 Anforderungen list) is cached once here and
        reused via `cached_content=<name>` on subsequent calls — paying for the prefix tokens
        a single time. Returns the cache resource name, or None if caching is unavailable
        (e.g. the corpus is below the model's minimum cacheable token count); callers should
        fall back to sending the corpus inline.
        """
        model_to_use = model_override if model_override else GROUND_TRUTH_MODEL
        try:
            cache = self.client.caches.create(
                model=model_to_use,
                config=types.CreateCachedContentConfig(
                    contents=[content],
                    system_instruction=system_instruction,
                ),
            )
            logger.info(f"Created context cache '{cache.name}' for model '{model_to_use}'.")
            return cache.name
        except Exception as e:
            logger.warning(f"Could not create context cache (falling back to inline corpus): {e}")
            return None

    def delete_context_cache(self, name: str) -> None:
        """Deletes a previously created context cache. Best-effort; logs and continues on error."""
        if not name:
            return
        try:
            self.client.caches.delete(name=name)
            logger.info(f"Deleted context cache '{name}'.")
        except Exception as e:
            logger.warning(f"Failed to delete context cache '{name}': {e}")

    def _prepare_generation_config(self, json_schema: Dict[str, Any], use_thinking: bool = False, cached_content: Optional[str] = None) -> types.GenerateContentConfig:
        """Prepares and converts the JSON schema for the GenerateContentConfig.

        When `cached_content` (an explicit context-cache resource name) is provided, the
        system instruction lives inside that cache, so we attach the cache and must NOT also
        set `system_instruction` on the request (the API rejects setting both).
        """
        try:
            # Create a copy to avoid modifying the original
            schema_for_api = json.loads(json.dumps(json_schema))
            # The new SDK is robust, but removing $schema is still good practice
            schema_for_api.pop("$schema", None)
        except Exception as e:
            logger.error(f"Failed to process JSON schema before API call: {e}")
            raise ValueError("Invalid JSON schema provided.") from e

        try:
            # Map constants to the new types.GenerateContentConfig structure
            config_kwargs = {
                "response_mime_type": "application/json",
                "response_schema": schema_for_api,
                "max_output_tokens": API_MAX_OUTPUT_TOKEN,
                "temperature": API_TEMPERATURE,
            }
            if cached_content:
                # System instruction + grounding corpus are baked into the cache.
                config_kwargs["cached_content"] = cached_content
            else:
                config_kwargs["system_instruction"] = self.system_message
            if use_thinking:
                config_kwargs["thinking_config"] = types.ThinkingConfig(
                    thinking_level=types.ThinkingLevel.HIGH
                )
            return types.GenerateContentConfig(**config_kwargs)
        except Exception as e:
            logger.error(f"Failed to prepare generation config: {e}", exc_info=True)
            raise ValueError(f"Invalid or incompatible GenerateContentConfig: {e}") from e

    def _process_response(self, response) -> Dict[str, Any]:
        """Processes the model response, handling finish reasons, thought parts, and JSON parsing."""
        if not response.candidates:
            raise ValueError("The model response contained no candidates.")

        candidate = response.candidates[0]

        # --- Robust Finish Reason Check ---
        # In the new SDK, finish_reason is often an Enum string (e.g., "STOP"). 
        # We check strictly for success indicators.
        # "STOP" is standard success. "MAX_TOKENS" (often mapped to 2) might be acceptable depending on logic, 
        # but usually implies truncation.
        valid_reasons = ["STOP", 1] # 1 is the integer value for STOP in some contexts
        
        # Helper to get string representation safely
        f_reason = candidate.finish_reason
        
        is_valid = False
        if isinstance(f_reason, str) and f_reason in valid_reasons:
            is_valid = True
        elif isinstance(f_reason, int) and f_reason in valid_reasons:
            is_valid = True
            
        if not is_valid:
             raise ValueError(f"Model finished with non-OK reason: {f_reason}")
        # --- End Robust Finish Reason Check ---

        # --- START: Handle Thinking/Reasoning Parts ---
        # We iterate parts to safely extract only valid text, ignoring 'thought' blocks
        # which can break JSON parsing.
        full_text_parts = []
        
        if candidate.content and candidate.content.parts:
            for part in candidate.content.parts:
                try:
                    # In v1.52.0, part.text exists if it is a text part. 
                    # If it is a thought part, accessing text might be None or imply checking part.thought
                    if part.text:
                        full_text_parts.append(part.text)
                except Exception:
                    # If any attribute access fails, assume it's a non-text part
                    continue
        
        raw_response_text = "".join(full_text_parts)
        
        if not raw_response_text:
            raise ValueError("Model response contained candidates but no extractable text (only thoughts/empty).")
        # --- END: Handle Thinking/Reasoning Parts ---

        # Clean Markdown code blocks if present
        if raw_response_text.startswith("```json"):
            raw_response_text = raw_response_text.replace("```json", "").replace("```", "")
        elif raw_response_text.startswith("```"):
            raw_response_text = raw_response_text.replace("```", "")

        try:
            response_json = json.loads(raw_response_text)
        except json.JSONDecodeError as e:
            logger.error(f"Failed JSON Text: {raw_response_text}") 
            raise ValueError(f"Failed to parse model response as JSON: {str(e).split(':')[0]}")
        
        return response_json

    async def generate_validated_json_response(
        self, 
        prompt: str, 
        json_schema: Dict[str, Any], 
        gcs_uris: List[str] = None,
        request_context_log: str = "Generic AI Request",
        model_override: Optional[str] = None,
        max_retries: int = None,
        cached_content: Optional[str] = None
    ) -> Dict[str, Any]:

        """
        Generates a JSON response from the AI model using google-genai SDK.

        If `cached_content` (an explicit context-cache resource name from
        `create_context_cache`) is given, it is attached to the request so the model reuses
        the cached system instruction + grounding corpus instead of re-sending it.
        """

        retries = max_retries if max_retries is not None else API_MAX_RETRIES
        model_to_use = model_override if model_override else GROUND_TRUTH_MODEL

        try:
            # Prepare configuration (includes system_instruction unless a cache supplies it)
            use_thinking = True if model_to_use == GROUND_TRUTH_MODEL_PRO else False
            gen_config = self._prepare_generation_config(json_schema, use_thinking=use_thinking, cached_content=cached_content)
        except ValueError as e:
            logger.error(f"[{request_context_log}] Configuration failed. Cannot proceed with AI request: {e}")
            raise

        # Construct Content Parts
        # The new SDK allows mixing strings and types.Part objects
        contents = []
        
        # Add GCS Files if present
        if gcs_uris:
            for uri in gcs_uris:
                # Syntax: types.Part.from_uri(file_uri=..., mime_type=...)
                contents.append(types.Part.from_uri(file_uri=uri, mime_type="application/pdf"))
            if self.config.is_test_mode:
                logger.debug(f"Attaching {len(gcs_uris)} GCS files to the prompt.")

        # Add the text prompt
        contents.append(prompt)

        for attempt in range(retries):
            try:
                logger.debug(f"[{request_context_log}] Attempt {attempt + 1}/{retries}: Calling Gemini model '{model_to_use}'...")
                
                # max logging
                # logger.debug(f"raw prompt: {contents}")

                # Asynchronous Generation call via .aio accessor
                response = await self.client.aio.models.generate_content(
                    model=model_to_use,
                    contents=contents,
                    config=gen_config,
                )
                # max logging
                # logger.debug(f"raw response JSON: {response}")
                response_json = self._process_response(response)

                validate(instance=response_json, schema=json_schema)

                logger.info(f"[{request_context_log}] Successfully generated and validated JSON on attempt {attempt + 1}.")
                return response_json

            except (errors.ClientError, ValueError, TypeError, ValidationError, httpx.ConnectError, httpx.TimeoutException) as e:
                # errors.ClientError covers most API-level issues in the new SDK
                # httpx.ConnectError and httpx.TimeoutException cover transient network/timeout issues
                wait_time = 2 ** attempt
                if attempt == retries - 1:
                    logger.critical(f"[{request_context_log}] AI generation failed after all {retries} retries.", exc_info=True)
                    raise

                error_msg = str(e)
                log_message = f"[{request_context_log}] Attempt {attempt + 1} failed. Retrying in {wait_time}s..."

                if isinstance(e, errors.ClientError):
                    logger.warning(f"[{request_context_log}] API Error: {e}. Retrying in {wait_time}s...")
                elif isinstance(e, ValidationError):
                    clean_msg = e.message.split('\n')[0] if '\n' in e.message else e.message
                    logger.warning(f"[{request_context_log}] Schema validation failed: '{clean_msg}'. Retrying in {wait_time}s...")
                else:
                    logger.warning(f"[{request_context_log}] Processing error: {error_msg}. Retrying in {wait_time}s...")

                await asyncio.sleep(wait_time)

            except Exception as e:
                logger.error(f"[{request_context_log}] Unexpected, non-retryable error: {type(e).__name__}: {e}", exc_info=True)
                raise