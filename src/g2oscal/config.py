import os
import sys
import logging
from pathlib import Path

# --- Path anchors ---
# Resolve everything against fixed anchors so the pipeline runs regardless of the
# current working directory: prompts/schemas live next to this file, data dirs
# live at the repo root (this file is at <repo>/src/g2oscal/config.py).
PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parents[1]

# --- Environment Variable Loading ---
TEST_MODE = os.environ.get("TEST", "false").lower() == 'true'
GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
# Vertex AI region (env-overridable; was hardcoded to us-central1 in the old SDK init).
REGION = os.environ.get("REGION", "us-central1")

# --- Local I/O configuration (replaces the old GCS bucket plumbing) ---
# Source PDFs are read from these directories (':'-separated, env-overridable).
# Relative entries resolve against the repo root.
_DEFAULT_SOURCE_DIRS = [
    REPO_ROOT / "BS_GK_OSCAL_JSON_DATA" / "Benutzerdefinierte_Bausteine",
    REPO_ROOT / "data",
]

def _resolve_dir(value: str) -> Path:
    p = Path(value).expanduser()
    return p if p.is_absolute() else (REPO_ROOT / p)

_env_source_dirs = os.environ.get("SOURCE_DIRS")
if _env_source_dirs:
    SOURCE_DIRS = [_resolve_dir(d) for d in _env_source_dirs.split(os.pathsep) if d.strip()]
else:
    SOURCE_DIRS = _DEFAULT_SOURCE_DIRS

# Where the merged catalog is written.
# - OUTPUT_FILE: write to this exact path (used by the two-pass run_local.sh to
#   produce the fixed canonical catalog names). Takes precedence when set.
# - OUTPUT_DIR: otherwise a timestamped file is written here (git-ignored).
_output_file = os.environ.get("OUTPUT_FILE")
OUTPUT_FILE = _resolve_dir(_output_file) if _output_file else None
OUTPUT_DIR = _resolve_dir(os.environ.get("OUTPUT_DIR", "data/output"))

# Optional existing catalog to merge into. If unset, a fresh catalog is created.
_existing = os.environ.get("EXISTING_JSON_PATH")
EXISTING_JSON_PATH = _resolve_dir(_existing) if _existing else None

# --- Static Configuration (prompts/schemas ship with the package) ---
DISCOVERY_ENRICHMENT_PROMPT_FILE = str(PACKAGE_DIR / "prompt_discovery_enrichment.txt")
GENERATION_PROMPT_FILE = str(PACKAGE_DIR / "prompt_generation.txt")
OSCAL_SCHEMA_FILE = str(PACKAGE_DIR / "bsi_gk_2023_oscal_schema.json")
DISCOVERY_ENRICHMENT_STUB_SCHEMA_FILE = str(PACKAGE_DIR / "discovery_enrichment_stub_schema.json")
GENERATION_STUB_SCHEMA_FILE = str(PACKAGE_DIR / "generation_stub_schema.json")

# --- Concurrency & Retry Config ---
CONCURRENT_REQUEST_LIMIT = 5
MAX_RETRIES = 5


class _AppConfig:
    """Object-style view of the config consumed by AiClient (google-genai)."""
    gcp_project_id = GCP_PROJECT_ID
    region = REGION
    is_test_mode = TEST_MODE


# Singleton consumed by ai_client.AiClient via `from config import app_config`.
app_config = _AppConfig()

def validate_env_vars():
    """Validates that the required configuration is present.

    Vertex AI still backs the model calls, so GCP_PROJECT_ID remains mandatory.
    At least one existing source directory must contain the input PDFs.
    """
    if not GCP_PROJECT_ID:
        sys.exit("FATAL: Missing required environment variable: GCP_PROJECT_ID.")

    existing_dirs = [d for d in SOURCE_DIRS if d.is_dir()]
    if not existing_dirs:
        listed = ", ".join(str(d) for d in SOURCE_DIRS)
        sys.exit(f"FATAL: None of the configured source directories exist: {listed}.")

def setup_logging():
    """Configures the root logger based on the TEST_MODE setting."""
    log_level = logging.DEBUG if TEST_MODE else logging.INFO
    logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stdout)

    # Unconditionally suppress verbose logs from underlying libraries in all modes.
    # We are interested in our application's logs, not the HTTP connection details.
    noisy_loggers = [
        "google.auth",
        "google.api_core.bidi",
        "google.api_core.client_options",
        "google.api_core.gapic_v1",
        "urllib3.connectionpool"
    ]
    for logger_name in noisy_loggers:
        logging.getLogger(logger_name).setLevel(logging.WARNING)

    # Use a logger specific to this module for the initialization message.
    logging.getLogger(__name__).info(f"Logging initialized. TEST_MODE={TEST_MODE}")

# Validate required configuration on import
validate_env_vars()
