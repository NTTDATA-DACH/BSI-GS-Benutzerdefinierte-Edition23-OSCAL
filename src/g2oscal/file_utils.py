"""Local-filesystem I/O for the g2oscal pipeline.

Replaces the former GCS-backed ``gcs_utils``: source PDFs are read from local
directories and the merged catalog is written to a local output directory.
"""
import json
import logging
from pathlib import Path
from typing import Iterable, List, Optional

logger = logging.getLogger(__name__)


def list_pdfs(source_dirs: Iterable[Path]) -> List[Path]:
    """Returns all ``*.pdf`` files across the given directories, sorted by name.

    Missing directories are skipped with a warning rather than failing the run.
    """
    pdfs: List[Path] = []
    for directory in source_dirs:
        directory = Path(directory)
        if not directory.is_dir():
            logger.warning(f"Source directory does not exist, skipping: {directory}")
            continue
        found = sorted(directory.glob("*.pdf"))
        logger.debug(f"Found {len(found)} PDF(s) in {directory}")
        pdfs.extend(found)
    return pdfs


def read_json(path: Path) -> Optional[dict]:
    """Reads and parses a JSON file, returning None if it does not exist."""
    path = Path(path)
    if not path.exists():
        logger.warning(f"File not found at {path}. Will start fresh.")
        return None
    logger.debug(f"Reading JSON from {path}...")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: dict) -> None:
    """Writes a dictionary to a JSON file, creating parent directories as needed."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    logger.debug(f"Writing JSON to {path}")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    logger.debug(f"Successfully wrote to {path}")
