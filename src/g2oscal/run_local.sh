#!/usr/bin/env bash
#
# run_local.sh — run the g2oscal pipeline against local PDFs (no GCS).
#
# Reads Baustein PDFs from:
#   - BS_GK_OSCAL_JSON_DATA/Benutzerdefinierte_Bausteine/   (committed sources)
#   - data/                                                 (your local drop-zone, git-ignored)
# and writes the merged OSCAL catalog to data/output/.
#
# The model calls still run on Vertex AI, so GCP_PROJECT_ID and application
# default credentials are required.
#
# Usage:
#   GCP_PROJECT_ID=my-project ./run_local.sh            # full run
#   GCP_PROJECT_ID=my-project TEST=true ./run_local.sh  # first 3 PDFs, 10% of reqs
#
set -euo pipefail

# Resolve repo layout from this script's location.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

# --- Required config -------------------------------------------------------
if [[ -z "${GCP_PROJECT_ID:-}" ]]; then
  echo "FATAL: set GCP_PROJECT_ID (e.g. GCP_PROJECT_ID=my-project ./run_local.sh)" >&2
  exit 1
fi
export GCP_PROJECT_ID
export REGION="${REGION:-us-central1}"
export TEST="${TEST:-false}"

# --- Local data directories ------------------------------------------------
# Ensure the git-ignored drop-zone and output directory exist.
mkdir -p "${REPO_ROOT}/data" "${REPO_ROOT}/data/output"

# --- Vertex AI credentials check ------------------------------------------
if ! gcloud auth application-default print-access-token >/dev/null 2>&1; then
  echo "No application default credentials found. Run:" >&2
  echo "    gcloud auth application-default login" >&2
  exit 1
fi

# --- Dependencies ----------------------------------------------------------
# Install once into the active environment; skip if already importable.
if ! python -c "import google.genai, jsonschema" >/dev/null 2>&1; then
  echo "Installing Python dependencies..."
  pip install -r "${SCRIPT_DIR}/requirements.txt"
fi

# --- Run -------------------------------------------------------------------
cd "${SCRIPT_DIR}"
echo "Running g2oscal pipeline (TEST=${TEST}, REGION=${REGION})..."
exec python main.py
