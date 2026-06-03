import sys
import json
import logging
import re
import uuid
import asyncio
from datetime import datetime, timezone

from jsonschema import validate, ValidationError

import config
import gcs_utils
from gemini_utils import process_baustein_pdf

# Initialize logging as the first step
config.setup_logging()
logger = logging.getLogger(__name__)

# --- Data Transformation & Assembly Functions ---
# Canonical BSI control id, e.g. "INF.5.A1", "SYS.1.2.3.A12". OSCAL ids are
# case-sensitive, so a slugified id ("inf-5-a1") silently breaks every
# reference to the control (issues.md #2/#12).
CONTROL_ID_PATTERN = re.compile(r"^[A-Z]+(\.[0-9A-Za-z]+)+\.A[0-9]+$")

def canonical_control_id(requirement_stub: dict) -> str:
    """Derive the canonical, case-sensitive control id for a requirement.

    The model occasionally normalises ids to slugs (lowercase, dots->hyphens).
    The canonical id always sits at the start of the ``title`` (e.g.
    "INF.5.A1 Planung ..."), so we prefer that and fall back to repairing the
    raw id (uppercase, hyphens->dots). Raises if the result is still malformed.
    """
    candidates = []
    title = (requirement_stub.get("title") or "").strip()
    if title:
        candidates.append(title.split()[0])
    raw_id = (requirement_stub.get("id") or "").strip()
    if raw_id:
        candidates.append(raw_id.replace("-", ".").upper())
    for candidate in candidates:
        if CONTROL_ID_PATTERN.match(candidate):
            return candidate
    raise ValueError(
        f"Cannot derive a canonical control id from id={raw_id!r} title={title!r}"
    )

# SIMPLIFIED: No longer needs a separate enrichment_data argument
def build_oscal_control(requirement_stub: dict, maturity_prose: dict) -> dict:
    control_id = canonical_control_id(requirement_stub)
    oscal_parts = []
    levels = [("Partial", "partial", "1"), ("Foundational", "foundational", "2"), ("Defined", "defined", "3"), ("Enhanced", "enhanced", "4"), ("Comprehensive", "comprehensive", "5")]
    for title_suffix, class_suffix, level_num in levels:
        statement = maturity_prose.get(f"level_{level_num}_statement")
        if statement:
            oscal_parts.append({
                "id": f"{control_id}-m{level_num}", "name": "maturity-level-description",
                "title": f"Maturity Level {level_num}: {title_suffix}", "class": f"maturity-level-{class_suffix}",
                "parts": [
                    {"name": "statement", "prose": statement},
                    {"name": "guidance", "prose": maturity_prose.get(f"level_{level_num}_guidance", "")},
                    {"name": "assessment-method", "prose": maturity_prose.get(f"level_{level_num}_assessment", "")}]})
    
    props_ns = "https://www.bsi.bund.de/ns/grundschutz"
    # Enrichment data is now part of the requirement_stub
    props = [
        {"name": "level", "value": requirement_stub.get('props', {}).get('level', 'N/A'), "ns": props_ns},
        {"name": "phase", "value": requirement_stub.get('props', {}).get('phase', 'N/A'), "ns": props_ns},
        {"name": "practice", "value": requirement_stub.get("practice"), "ns": props_ns},
        {"name": "effective_on_c", "value": str(requirement_stub.get("effective_on_c")).lower(), "ns": props_ns},
        {"name": "effective_on_i", "value": str(requirement_stub.get("effective_on_i")).lower(), "ns": props_ns},
        {"name": "effective_on_a", "value": str(requirement_stub.get("effective_on_a")).lower(), "ns": props_ns}
    ]
    
    return {
        "id": control_id, 
        "title": requirement_stub['title'], 
        "class": requirement_stub.get("class", "Technical"),
        "props": props,
        "parts": oscal_parts
    }

def load_existing_catalog(gcs_path, schema):
    if not gcs_path:
        logger.info("No existing JSON path provided. Starting with a fresh catalog.")
        return get_empty_catalog_structure()
    
    try:
        existing_catalog = gcs_utils.read_json_from_gcs(gcs_path)
        if existing_catalog is None:
            return get_empty_catalog_structure()
        validate(instance=existing_catalog, schema=schema)
        return existing_catalog
    except (json.JSONDecodeError, ValidationError) as e:
        logging.critical(f"FATAL: Existing JSON at {gcs_path} is invalid: {e}. Please fix.")
        sys.exit(1)

def get_empty_catalog_structure():
    groups = [{"id": "ISMS", "title": "ISMS: Sicherheitsmanagement"}, {"id": "ORP", "title": "ORP: Organisation und Personal"}, {"id": "CON", "title": "CON: Konzeption und Vorgehensweise"}, {"id": "OPS", "title": "OPS: Betrieb"}, {"id": "DER", "title": "DER: Detektion und Reaktion"}, {"id": "APP", "title": "APP: Anwendungen"}, {"id": "SYS", "title": "SYS: IT-Systeme"}, {"id": "IND", "title": "IND: Industrielle IT"}, {"id": "NET", "title": "NET: Netze und Kommunikation"}, {"id": "INF", "title": "INF: Infrastruktur"}]
    return {"catalog": {"uuid": str(uuid.uuid4()), "metadata": {"title": "Gesamtkatalog BSI Grundschutz Kompendium", "last-modified": datetime.now(timezone.utc).isoformat(), "version": "1.0.0", "oscal-version": "1.1.2"}, "groups": [{"id": g["id"], "class": "layer", "title": g["title"], "groups": []} for g in groups]}}

def merge_results(new_results, base_catalog):
    logger.debug("Starting merge process...")
    main_groups_map = {g['id']: g for g in base_catalog['catalog']['groups']}
    for main_id, baustein in new_results:
        if not (main_id and baustein): continue
        b_id = baustein.get("id")
        if not b_id: 
            logger.warning("Skipping result with no baustein 'id'.")
            continue
        if main_id in main_groups_map:
            target = main_groups_map[main_id]
            idx = next((i for i, b in enumerate(target.get("groups", [])) if b.get("id") == b_id), -1)
            if idx != -1:
                logger.debug(f"Updating Baustein '{b_id}' in '{main_id}'.")
                target["groups"][idx] = baustein
            else:
                logger.debug(f"Adding new Baustein '{b_id}' to '{main_id}'.")
                target.setdefault("groups", []).append(baustein)
        else:
            logger.warning(f"Main Group ID '{main_id}' not in catalog. Skipping '{b_id}'.")
    
    for g in base_catalog['catalog']['groups']:
        if "groups" in g:
            g['groups'].sort(key=lambda x: x.get('id', ''))
            
    base_catalog["catalog"]["metadata"]["last-modified"] = datetime.now(timezone.utc).isoformat()
    return base_catalog

# --- Main Execution Orchestrator ---
async def main():
    logger.info(f"Job starting... [TEST_MODE={config.TEST_MODE}]")
    
    with open(config.OSCAL_SCHEMA_FILE, 'r', encoding='utf-8') as f: 
        loaded_oscal_schema = json.load(f)

    base_catalog = load_existing_catalog(config.EXISTING_JSON_GCS_PATH, loaded_oscal_schema)
    
    all_blobs = gcs_utils.list_blobs(prefix=config.SOURCE_PREFIX)
    files_to_process = [blob for blob in all_blobs if blob.name.lower().endswith('.pdf')]
    if not files_to_process:
        logger.warning(f"No PDF files found in gs://{config.BUCKET_NAME}/{config.SOURCE_PREFIX}. Exiting.")
        return
    
    if config.TEST_MODE: 
        files_to_process = files_to_process[:3]
        logger.warning(f"--- TEST MODE: Processing a maximum of {len(files_to_process)} files. ---")
    
    semaphore = asyncio.Semaphore(config.CONCURRENT_REQUEST_LIMIT)
    tasks = [process_baustein_pdf(blob, semaphore, build_oscal_control) for blob in files_to_process]
    
    all_results = await asyncio.gather(*tasks)
    successful_results = [res for res in all_results if res and res[0] and res[1]]
    
    final_catalog = merge_results(successful_results, base_catalog)

    try:
        logger.info("Validating final merged catalog against OSCAL schema...")
        validate(instance=final_catalog, schema=loaded_oscal_schema)
        logger.info("Final catalog validation successful.")
    except ValidationError as e:
        logging.critical(f"Final catalog validation FAILED: {e.message}. The output file may be non-compliant.", exc_info=config.TEST_MODE)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    output_filename = f"{config.FINAL_RESULT_PREFIX}MERGED_BSI_Catalog_{timestamp}.json"
    gcs_utils.write_json_to_gcs(output_filename, final_catalog)
    
    logger.info(f"Final catalog successfully written to: gs://{config.BUCKET_NAME}/{output_filename}")
    
    logger.info("--- Batch Job Summary ---")
    logger.info(f"Successfully processed: {len(successful_results)} file(s).")
    logger.info(f"Failed to process: {len(files_to_process) - len(successful_results)} file(s).")

if __name__ == "__main__":
    asyncio.run(main())