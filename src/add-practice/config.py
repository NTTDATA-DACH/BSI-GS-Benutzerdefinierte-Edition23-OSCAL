import logging
import os
import sys

from dotenv import load_dotenv

# Load environment variables from .env file for local development
load_dotenv()

# --- Core GCP Settings ---
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
BUCKET_NAME = os.getenv("BUCKET_NAME")

# --- I/O Configuration ---
SOURCE_PREFIX = os.getenv("SOURCE_PREFIX")
OUTPUT_PREFIX = os.getenv("OUTPUT_PREFIX")
EXISTING_JSON_GCS_PATH = os.getenv("EXISTING_JSON_GCS_PATH")

# --- Operational Settings ---
TEST_MODE = os.getenv("TEST", "false").lower() == "true"
TOKEN_LIMIT_PER_BATCH = int(os.getenv("TOKEN_LIMIT_PER_BATCH", "6000"))

def validate_env_vars():
    """Validates that all required environment variables are set."""
    required_vars = {
        "GCP_PROJECT_ID": GCP_PROJECT_ID,
        "BUCKET_NAME": BUCKET_NAME,
        "OUTPUT_PREFIX": OUTPUT_PREFIX,
        "EXISTING_JSON_GCS_PATH": EXISTING_JSON_GCS_PATH,
    }
    missing_vars = [key for key, value in required_vars.items() if not value]
    if missing_vars:
        logging.basicConfig(level=logging.ERROR)
        error_message = f"Missing required environment variables: {', '.join(missing_vars)}"
        logging.error(error_message)
        sys.exit(error_message)


def setup_logging():
    """Configures the root logger based on the TEST_MODE setting."""
    base_level = logging.INFO
    # Detailed step-by-step logs at DEBUG in TEST_MODE, INFO in production.
    verbose_level = logging.DEBUG if TEST_MODE else logging.INFO

    logging.basicConfig(
        level=base_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
    )

    # Set the more verbose level for our application's logger
    app_logger = logging.getLogger("__main__")
    app_logger.setLevel(verbose_level)
    logging.getLogger("gemini_utils").setLevel(verbose_level)

    # Suppress verbose logs from third-party libraries in production
    if not TEST_MODE:
        logging.info("Production mode: Suppressing verbose logs from third-party libraries.")
        logging.getLogger("google").setLevel(logging.WARNING)
        logging.getLogger("google.auth").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.getLogger("google.api_core").setLevel(logging.WARNING)

    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized. TEST_MODE={TEST_MODE}. Base Level={logging.getLevelName(base_level)}, App Verbose Level={logging.getLevelName(verbose_level)}")


# Validate variables on import
validate_env_vars()