#!/usr/bin/env python3
"""compare_pdf_json_counts.py

Compares the number of unique requirements found in BSI IT-Grundschutz source PDFs 
(by extracting text and matching canonical requirement IDs) with the actual 
control count in the generated OSCAL JSON catalogs.

Useful for verifying completeness and identifying truncated/dropped requirements.
"""
import sys
import os
import re
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple

try:
    import pypdf
except ImportError:
    print("Error: pypdf library is required. Run 'pip install pypdf' first.", file=sys.stderr)
    sys.exit(1)


def parse_baustein_id(filename: str) -> str:
    """Parses Baustein ID from filename (e.g. 'APP.1.1 Office-Produkte...' -> 'APP.1.1')"""
    return filename.split()[0]


def extract_requirements_from_pdf(pdf_path: Path, baustein_id: str) -> Set[str]:
    """Extracts unique requirement IDs from the PDF text using regex."""
    try:
        reader = pypdf.PdfReader(str(pdf_path))
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        
        # BSI requirements always use the pattern <Baustein-ID>.A<Number>
        # e.g. APP.1.1.A1, SYS.1.8.A12
        pattern = rf"\b{re.escape(baustein_id)}\.A\d+\b"
        matches = re.findall(pattern, text)
        return set(matches)
    except Exception as e:
        print(f"Warning: Failed to parse PDF {pdf_path.name}: {e}", file=sys.stderr)
        return set()


def collect_catalog_bausteine(catalog_data: dict) -> Dict[str, Set[str]]:
    """Recursively collects all baustein groups and their control IDs from the catalog."""
    bausteine = {}

    def recurse(group):
        if group.get("class") == "baustein":
            b_id = group.get("id")
            # Collect control IDs (normalized to uppercase for comparison)
            ctrl_ids = {c.get("id").upper() for c in group.get("controls", []) if "id" in c}
            bausteine[b_id] = ctrl_ids
        for sub_g in group.get("groups", []):
            recurse(sub_g)

    catalog = catalog_data.get("catalog", {})
    for group in catalog.get("groups", []):
        recurse(group)
        
    return bausteine


def run_comparison(pdf_dir: Path, catalog_path: Path) -> List[Tuple[str, int, int, str, Set[str], Set[str]]]:
    """Runs the comparison between PDFs in pdf_dir and the OSCAL catalog."""
    if not catalog_path.exists():
        print(f"Catalog JSON not found at: {catalog_path}")
        return []

    with open(catalog_path, "r", encoding="utf-8") as f:
        catalog_data = json.load(f)

    catalog_bausteine = collect_catalog_bausteine(catalog_data)
    pdf_files = sorted(list(Path(pdf_dir).glob("*.pdf")))
    
    results = []
    
    for pdf_path in pdf_files:
        b_id = parse_baustein_id(pdf_path.name)
        # Extract unique requirements from PDF
        pdf_reqs = extract_requirements_from_pdf(pdf_path, b_id)
        # Map canonical PDF IDs to uppercase standard representation
        pdf_reqs_upper = {r.upper() for r in pdf_reqs}
        
        json_reqs = catalog_bausteine.get(b_id)
        
        if json_reqs is None:
            results.append((b_id, len(pdf_reqs), 0, "NOT_IN_JSON", pdf_reqs_upper, set()))
        else:
            if pdf_reqs_upper == json_reqs:
                status = "OK"
            else:
                status = "MISMATCH"
            results.append((b_id, len(pdf_reqs), len(json_reqs), status, pdf_reqs_upper, json_reqs))
            
    return results


def main():
    repo_root = Path(__file__).resolve().parents[2]
    
    # Default Paths
    std_pdf_dir = repo_root / "data"
    cust_pdf_dir = repo_root / "BS_GK_OSCAL_JSON_DATA" / "Benutzerdefinierte_Bausteine"
    
    std_catalog = repo_root / "BS_GK_OSCAL_JSON_DATA" / "BSI_GS_OSCAL_current_2023.json"
    cust_catalog = repo_root / "BS_GK_OSCAL_JSON_DATA" / "BSI_GS_OSCAL_current_2023_benutzerdefinierte.json"
    
    print("=" * 80)
    print(" OSCAL Catalog Requirements vs. PDF Source Verification Tool")
    print("=" * 80)
    
    # Check Standard Catalog
    print(f"\n--- Checking Standard Catalog ({std_catalog.name}) ---")
    if std_catalog.exists() and std_pdf_dir.exists():
        std_results = run_comparison(std_pdf_dir, std_catalog)
        print(f"{'Baustein ID':<15} | {'PDF Count':<10} | {'JSON Count':<10} | {'Status':<12}")
        print("-" * 55)
        mismatches = []
        for b_id, pdf_cnt, json_cnt, status, pdf_set, json_set in std_results:
            print(f"{b_id:<15} | {pdf_cnt:<10} | {json_cnt:<10} | {status:<12}")
            if status != "OK":
                mismatches.append((b_id, pdf_set, json_set, status))
        
        if mismatches:
            print("\nDetailed Mismatches:")
            for b_id, pdf_set, json_set, status in mismatches:
                print(f"\n  [ {b_id} ] - Status: {status}")
                if status == "NOT_IN_JSON":
                    print("    -> Baustein is completely missing from JSON catalog.")
                else:
                    missing_in_json = pdf_set - json_set
                    extra_in_json = json_set - pdf_set
                    if missing_in_json:
                        print(f"    - Missing in JSON ({len(missing_in_json)}): {sorted(list(missing_in_json))}")
                    if extra_in_json:
                        print(f"    - Extra in JSON ({len(extra_in_json)}): {sorted(list(extra_in_json))}")
    else:
        print("Standard catalog or standard PDF directory not found.")
        
    # Check Custom Catalog
    print(f"\n--- Checking Custom Catalog ({cust_catalog.name}) ---")
    if cust_catalog.exists() and cust_pdf_dir.exists():
        cust_results = run_comparison(cust_pdf_dir, cust_catalog)
        print(f"{'Baustein ID':<15} | {'PDF Count':<10} | {'JSON Count':<10} | {'Status':<12}")
        print("-" * 55)
        mismatches = []
        for b_id, pdf_cnt, json_cnt, status, pdf_set, json_set in cust_results:
            print(f"{b_id:<15} | {pdf_cnt:<10} | {json_cnt:<10} | {status:<12}")
            if status != "OK":
                mismatches.append((b_id, pdf_set, json_set, status))
                
        if mismatches:
            print("\nDetailed Mismatches:")
            for b_id, pdf_set, json_set, status in mismatches:
                print(f"\n  [ {b_id} ] - Status: {status}")
                if status == "NOT_IN_JSON":
                    print("    -> Baustein is completely missing from JSON catalog.")
                else:
                    missing_in_json = pdf_set - json_set
                    extra_in_json = json_set - pdf_set
                    if missing_in_json:
                        print(f"    - Missing in JSON ({len(missing_in_json)}): {sorted(list(missing_in_json))}")
                    if extra_in_json:
                        print(f"    - Extra in JSON ({len(extra_in_json)}): {sorted(list(extra_in_json))}")
    else:
        print("Custom catalog or custom PDF directory not found.")


if __name__ == "__main__":
    main()
