#!/usr/bin/env bash
#
# run_local.sh — build both BSI Grundschutz OSCAL catalogs locally (no GCS).
#
# Two passes, run in order:
#
#   Pass 1 ("ohne"):  PDFs in   data/
#                     -> BS_GK_OSCAL_JSON_DATA/BSI_GS_OSCAL_current_2023.json
#                     (fresh standard catalog)
#
#   Pass 2 ("mit"):   PDFs in   BS_GK_OSCAL_JSON_DATA/Benutzerdefinierte_Bausteine/
#                     merged on top of pass 1's result
#                     -> BS_GK_OSCAL_JSON_DATA/BSI_GS_OSCAL_current_2023_benutzerdefinierte.json
#                     (standard + benutzerdefinierte Bausteine)
#
# Drop the standard 2023 Baustein PDFs into data/ before running. If data/ is
# empty, pass 1 writes nothing and leaves the existing current_2023.json in
# place, so pass 2 still merges the custom Bausteine onto that existing base.
#
# The model calls run on Vertex AI, so GCP_PROJECT_ID and application default
# credentials are required.
#
# Usage:
#   GCP_PROJECT_ID=my-project ./run_local.sh            # full run
#   GCP_PROJECT_ID=my-project TEST=true ./run_local.sh  # quick smoke test
#
set -euo pipefail

# Resolve repo layout from this script's location.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

DATA_DIR="${REPO_ROOT}/BS_GK_OSCAL_JSON_DATA"
STANDARD_CATALOG="${DATA_DIR}/BSI_GS_OSCAL_current_2023.json"
CUSTOM_CATALOG="${DATA_DIR}/BSI_GS_OSCAL_current_2023_benutzerdefinierte.json"
CUSTOM_PDF_DIR="${DATA_DIR}/Benutzerdefinierte_Bausteine"

# --- Required config -------------------------------------------------------
if [[ -z "${GCP_PROJECT_ID:-}" ]]; then
  echo "FATAL: set GCP_PROJECT_ID (e.g. GCP_PROJECT_ID=my-project ./run_local.sh)" >&2
  exit 1
fi
export GCP_PROJECT_ID
export REGION="${REGION:-us-central1}"
export TEST="${TEST:-false}"

# --- Local data directories ------------------------------------------------
# data/ is the git-ignored drop-zone for the standard 2023 Baustein PDFs.
mkdir -p "${REPO_ROOT}/data"

# --- Vertex AI credentials check ------------------------------------------
if ! gcloud auth application-default print-access-token >/dev/null 2>&1; then
  echo "No application default credentials found. Run:" >&2
  echo "    gcloud auth application-default login" >&2
  exit 1
fi

# --- Dependencies ----------------------------------------------------------
if ! python -c "import google.genai, jsonschema" >/dev/null 2>&1; then
  echo "Installing Python dependencies..."
  pip install -r "${SCRIPT_DIR}/requirements.txt"
fi

cd "${SCRIPT_DIR}"

# --- Pass 1: standard catalog from data/ (without custom Bausteine) ---------
echo "=== Pass 1/2: standard catalog (data/ -> $(basename "${STANDARD_CATALOG}")) ==="
SOURCE_DIRS="${REPO_ROOT}/data" \
OUTPUT_FILE="${STANDARD_CATALOG}" \
  python main.py

# --- Pass 2: add custom Bausteine on top of the standard catalog -----------
echo "=== Pass 2/2: + benutzerdefinierte (${CUSTOM_PDF_DIR} -> $(basename "${CUSTOM_CATALOG}")) ==="
SOURCE_DIRS="${CUSTOM_PDF_DIR}" \
EXISTING_JSON_PATH="${STANDARD_CATALOG}" \
OUTPUT_FILE="${CUSTOM_CATALOG}" \
  python main.py

echo "=== Done ==="
echo "  ohne custom: ${STANDARD_CATALOG}"
echo "  mit  custom: ${CUSTOM_CATALOG}"
