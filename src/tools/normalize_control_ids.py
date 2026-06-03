#!/usr/bin/env python3
"""Fix slugified control IDs in SYS.1.8 / INF.5 / INF.9 (issues.md #2 / #12).

The g2oscal pipeline occasionally let the model normalise control IDs to slugs
(lowercase, dots->hyphens) for these three Bausteine, e.g. ``inf-5-a1`` and
``sys.1.8.a1`` instead of the canonical, case-sensitive OSCAL tokens
``INF.5.A1`` / ``SYS.1.8.A1``. The canonical ID still lives in each control's
``title``. Because OSCAL ids are case-sensitive, every reference to these
controls by their canonical id silently fails to resolve.

These lowercase slug tokens never occur in any legitimate context (titles and
all other Bausteine use the canonical uppercase form), so a direct token
rewrite over the raw file text is safe and also fixes the machine-generated
prose ("...documentation for control inf-5-a1") in the component files.

Run from the repo root: ``python3 src/tools/normalize_control_ids.py``
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

# (pattern, replacement) — \1 captures the requirement number; any trailing
# maturity suffix (e.g. "-m1") is left untouched because the digit class is
# greedy and stops before the "-m".
SUBSTITUTIONS = [
    (re.compile(r"inf-5-a(\d+)"), r"INF.5.A\1"),
    (re.compile(r"inf-9-a(\d+)"), r"INF.9.A\1"),
    (re.compile(r"sys\.1\.8\.a(\d+)"), r"SYS.1.8.A\1"),
]

DATA_DIR = Path(__file__).resolve().parents[2] / "BS_GK_OSCAL_JSON_DATA"


def find_affected_files() -> list[Path]:
    out = subprocess.run(
        ["grep", "-rlE", r"inf-5-a[0-9]|inf-9-a[0-9]|sys\.1\.8\.a[0-9]", str(DATA_DIR)],
        capture_output=True, text=True, check=False,
    ).stdout
    return sorted(Path(p) for p in out.splitlines() if p)


def normalize(text: str) -> tuple[str, int]:
    total = 0
    for pattern, repl in SUBSTITUTIONS:
        text, n = pattern.subn(repl, text)
        total += n
    return text, total


def main() -> int:
    files = find_affected_files()
    if not files:
        print("No affected files found — nothing to do.")
        return 0
    grand_total = 0
    for path in files:
        original = path.read_text(encoding="utf-8")
        fixed, n = normalize(original)
        if n:
            path.write_text(fixed, encoding="utf-8")
            grand_total += n
            print(f"{n:5d}  {path.relative_to(DATA_DIR.parent)}")
    print(f"\nNormalized {grand_total} slugified token(s) across {len(files)} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
