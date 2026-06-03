import asyncio
import json
import logging
import os
from datetime import datetime, timezone
from itertools import chain

from jsonschema import validate, ValidationError

from config import (
    BUCKET_NAME,
    EXISTING_JSON_GCS_PATH,
    OUTPUT_PREFIX,
    TOKEN_LIMIT_PER_BATCH,
    TEST_MODE,
    setup_logging,
)
from gcs_utils import read_json_from_gcs, write_json_to_gcs
from gemini_utils import generate_practices_for_batch, MAX_CONCURRENT_REQUESTS

# Initialize logging as the first step
setup_logging()
logger = logging.getLogger(__name__)


def load_json_schema(schema_path: str) -> dict:
    """Loads a JSON schema from a local file."""
    try:
        with open(schema_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.critical(f"Schema file not found at: {schema_path}", exc_info=TEST_MODE)
        raise
    except json.JSONDecodeError:
        logger.critical(f"Invalid JSON in schema file: {schema_path}", exc_info=TEST_MODE)
        raise


def find_all_controls(catalog: dict) -> list[dict]:
    """Recursively finds all controls in the catalog data."""
    controls = []
    
    def recurse(obj):
        if isinstance(obj, dict):
            if "controls" in obj and isinstance(obj["controls"], list):
                controls.extend(obj["controls"])
            for key, value in obj.items():
                recurse(value)
        elif isinstance(obj, list):
            for item in obj:
                recurse(item)

    recurse(catalog)
    return controls


def create_control_batches(controls: list[dict]) -> list[list[dict]]:
    """
    Groups controls into batches, ensuring each batch is under the token limit.

    Args:
        controls: A list of all control objects.

    Returns:
        A list of lists, where each inner list is a batch of controls.
    """
    batches = []
    current_batch = []
    current_tokens = 0
    prompt_overhead_tokens = 1000

    for control in controls:
        control_stub = {"id": control.get("id"), "title": control.get("title")}
        item_tokens = len(json.dumps(control_stub)) // 2

        if current_batch and (current_tokens + item_tokens + prompt_overhead_tokens) > TOKEN_LIMIT_PER_BATCH:
            batches.append(current_batch)
            current_batch, current_tokens = [], 0
        current_batch.append(control)
        current_tokens += item_tokens
    if current_batch:
        batches.append(current_batch)
    logger.info(f"Created {len(batches)} batches from {len(controls)} controls.")
    return batches

async def main():
    """Main function to orchestrate the data processing pipeline."""
    logger.info("Starting the practice generation process.")

    result_schema = load_json_schema("schemas/catalog.schema.json")
    catalog_data = await read_json_from_gcs(BUCKET_NAME, EXISTING_JSON_GCS_PATH)

    if not catalog_data:
        logger.critical("Failed to load catalog data from GCS. Aborting process.")
        return

    all_controls = find_all_controls(catalog_data)
    logger.info(f"Found {len(all_controls)} total controls to process.")

    if TEST_MODE:
        limit = 3
        all_controls = all_controls[:limit]
        logger.warning(f"TEST_MODE is active. Processing only the first {len(all_controls)} controls.")

    control_batches = create_control_batches(all_controls)
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    tasks = []

    async def process_batch_with_semaphore(batch):
        async with semaphore:
            return await generate_practices_for_batch(batch)

    for batch in control_batches:
        tasks.append(process_batch_with_semaphore(batch))
        
    batch_results = await asyncio.gather(*tasks)
    results = list(chain.from_iterable(batch_results))

    # Map results back to controls by id, NOT by position: the model may
    # reorder or drop items, and a positional zip would silently write a
    # control's practice/CIA/class onto the wrong control (issues.md #3).
    results_by_id = {}
    for generated_data in results:
        if not generated_data:
            continue
        gen_id = generated_data.get("id")
        if not gen_id:
            logger.warning("Skipping a generated result with no 'id'.")
            continue
        if gen_id in results_by_id:
            logger.warning(f"Duplicate generated result for control id '{gen_id}'. Keeping the first.")
            continue
        results_by_id[gen_id] = generated_data

    updated_controls_count = 0
    props_ns = "https://www.bsi.bund.de/ns/grundschutz"
    props_to_manage = ["practice", "effective_on_c", "effective_on_i", "effective_on_a"]

    for control in all_controls:
        generated_data = results_by_id.get(control.get("id"))
        if generated_data:
            # Update the control's class directly
            control["class"] = generated_data["class"]
            
            if "props" not in control:
                control["props"] = []
            
            # Remove existing props to ensure idempotency
            control["props"] = [p for p in control["props"] if p.get("name") not in props_to_manage]
            
            # Add the new 'practice' prop
            control["props"].append({
                "name": "practice",
                "value": generated_data["practice"],
                "ns": props_ns
            })
            
            # Add the new CIA props
            control["props"].append({
                "name": "effective_on_c",
                "value": str(generated_data["effective_on_c"]).lower(),
                "ns": props_ns
            })
            control["props"].append({
                "name": "effective_on_i",
                "value": str(generated_data["effective_on_i"]).lower(),
                "ns": props_ns
            })
            control["props"].append({
                "name": "effective_on_a",
                "value": str(generated_data["effective_on_a"]).lower(),
                "ns": props_ns
            })
            
            updated_controls_count += 1
            logger.debug(f"Updated control {control.get('id')} with new class and props.")

    logger.info(f"Successfully generated and added data for {updated_controls_count}/{len(all_controls)} controls.")

    catalog_data["catalog"]["metadata"]["last-modified"] = datetime.now(timezone.utc).isoformat()
    
    try:
        validate(instance=catalog_data, schema=result_schema)
        logger.info("Final catalog validation successful.")
    except ValidationError as e:
        logger.error(f"Final catalog validation failed: {e.message}", exc_info=TEST_MODE)
    
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    base_filename = os.path.basename(EXISTING_JSON_GCS_PATH).replace('.json', '')
    output_filename = f"{base_filename}_with_practices_{timestamp}.json"
    output_path = os.path.join(OUTPUT_PREFIX, output_filename)

    await write_json_to_gcs(BUCKET_NAME, output_path, catalog_data)
    logger.info(f"Practice generation process finished. Updated catalog saved to: gs://{BUCKET_NAME}/{output_path}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.critical(f"An unhandled exception occurred in main: {e}", exc_info=TEST_MODE)