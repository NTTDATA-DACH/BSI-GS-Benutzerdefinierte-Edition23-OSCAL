import json
import logging

from config import (TEST_MODE, app_config,
                    DISCOVERY_ENRICHMENT_PROMPT_FILE, GENERATION_PROMPT_FILE,
                    DISCOVERY_ENRICHMENT_STUB_SCHEMA_FILE, GENERATION_STUB_SCHEMA_FILE)
from constants import GROUND_TRUTH_MODEL_PRO
from ai_client import AiClient

logger = logging.getLogger(__name__)

# --- Initialization ---
try:
    with open(DISCOVERY_ENRICHMENT_PROMPT_FILE, 'r', encoding='utf-8') as f: discovery_enrichment_prompt_text = f.read()
    with open(GENERATION_PROMPT_FILE, 'r', encoding='utf-8') as f: generation_prompt_template = f.read()
    with open(DISCOVERY_ENRICHMENT_STUB_SCHEMA_FILE, 'r', encoding='utf-8') as f: loaded_discovery_enrichment_schema = json.load(f)
    with open(GENERATION_STUB_SCHEMA_FILE, 'r', encoding='utf-8') as f: loaded_generation_schema = json.load(f)

    # Shared AI client (google-genai / Vertex). Handles retries, finish-reason
    # checks, thought-part filtering and JSON-schema validation internally.
    ai_client = AiClient(app_config)

except Exception as e:
    logging.critical(f"FATAL: Failed to initialize Gemini Utils: {e}", exc_info=True)
    raise

# --- Main Processing Logic ---
async def process_baustein_pdf(pdf_path, semaphore, build_oscal_control_func):
    """Orchestrates the two-stage generation process for a single Baustein PDF."""
    async with semaphore:
        pdf_name = pdf_path.name
        logging.info(f"Processing file: {pdf_name}")
        try:
            # STAGE 1: Combined Discovery & Enrichment
            logging.debug(f"Stage 1: Discovering & Enriching structure for {pdf_name}...")
            discovery_enrichment_data = await ai_client.generate_validated_json_response(
                prompt=discovery_enrichment_prompt_text,
                json_schema=loaded_discovery_enrichment_schema,
                pdf_paths=[str(pdf_path)],
                request_context_log=f"Discovery {pdf_name}",
                model_override=GROUND_TRUTH_MODEL_PRO,
            )

            requirements_to_process = discovery_enrichment_data.get('requirements_list', [])
            logging.info(f"  └─ Discovered {len(requirements_to_process)} requirements for {pdf_name}.")

            if TEST_MODE and requirements_to_process:
                slice_index = max(1, int(len(requirements_to_process) * 0.10))
                requirements_to_process = requirements_to_process[:slice_index]
                logging.debug(f"TEST MODE: Sliced requirements to {len(requirements_to_process)}.")

            if not requirements_to_process:
                # Stage 1 returning zero requirements is a discovery failure
                # (truncation, safety block, or model miss), not a success — a
                # Baustein with no Anforderungen must not be merged silently.
                raise ValueError(
                    f"Discovery stage returned no requirements for {pdf_name}; flagging for re-run."
                )

            # STAGE 2: Generation of Maturity Prose
            logging.debug(f"Stage 2: Generating maturity prose for {len(requirements_to_process)} requirements...")
            generation_batch_prompt = generation_prompt_template.format(REQUIREMENTS_JSON_BATCH=json.dumps(requirements_to_process, indent=2, ensure_ascii=False))
            generation_data = await ai_client.generate_validated_json_response(
                prompt=generation_batch_prompt,
                json_schema=loaded_generation_schema,
                request_context_log=f"Generation {pdf_name}",
                model_override=GROUND_TRUTH_MODEL_PRO,
            )
            logging.debug(f"Maturity prose generation successful.")

            # ASSEMBLY
            prose_map = {item['id']: item for item in generation_data.get('generated_requirements', [])}

            final_controls = []
            missing_ids = []
            for req_stub in requirements_to_process:
                req_id = req_stub['id']
                if req_id in prose_map:
                    # The stub itself now contains the enrichment data (class, practice, etc.)
                    final_controls.append(build_oscal_control_func(req_stub, prose_map[req_id]))
                else:
                    missing_ids.append(req_id)

            # Completeness gate: never write a Baustein with fewer Anforderungen
            # than were discovered. Fail loudly so it is counted as failed and
            # re-run, rather than silently merged as partial (issues.md #1/#2).
            if missing_ids:
                raise ValueError(
                    f"Generation stage incomplete: {len(missing_ids)}/{len(requirements_to_process)} "
                    f"requirements missing prose (e.g. {missing_ids[:5]}). Refusing to write a partial Baustein."
                )

            final_baustein_group = {
                "id": discovery_enrichment_data.get("baustein_id"), "title": discovery_enrichment_data.get("baustein_title"),
                "class": "baustein", "parts": discovery_enrichment_data.get("contextual_parts", []), "controls": final_controls
            }
            logging.info(f"  └─ Successfully finished processing {pdf_name}.")
            return discovery_enrichment_data.get("main_group_id"), final_baustein_group

        except Exception as e:
            logging.error(f"  └─ FAILED to process {pdf_name}. Error: {e}", exc_info=TEST_MODE)
            return None, None
