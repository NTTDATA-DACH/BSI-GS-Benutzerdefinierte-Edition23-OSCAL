"""Static constants for the g2oscal AI client.

Model IDs and tuning are env-overridable so newer models can be tried without
code changes (per symbiotic-coding-brief "no hardcoded configuration").
"""
import os
from pathlib import Path

_PACKAGE_DIR = Path(__file__).resolve().parent

# --- Models (Vertex AI / google-genai IDs) ---
# GROUND_TRUTH_MODEL_PRO: the high-capability model for hard extraction/generation
#   (Gemini 3.1 Pro preview — thinking is enabled for this model in the client).
# GROUND_TRUTH_MODEL: the fast model for lighter tasks (Gemini 3 Flash).
GROUND_TRUTH_MODEL_PRO = os.environ.get("MODEL_PRO", "gemini-3.1-pro-preview")
GROUND_TRUTH_MODEL = os.environ.get("MODEL_FLASH", "gemini-3-flash-preview")

# --- Generation tuning ---
API_MAX_OUTPUT_TOKEN = int(os.environ.get("API_MAX_OUTPUT_TOKEN", "65536"))
API_TEMPERATURE = float(os.environ.get("API_TEMPERATURE", "0.1"))
API_MAX_RETRIES = int(os.environ.get("API_MAX_RETRIES", "5"))

# --- System-prompt config consumed by AiClient.__init__ ---
PROMPT_CONFIG_PATH = os.environ.get("PROMPT_CONFIG_PATH", str(_PACKAGE_DIR / "prompt_config.json"))
