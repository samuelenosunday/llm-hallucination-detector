"""
LLM Hallucination Detector
==========================
Checks claims against a verified knowledge base and flags them as:
- SUPPORTED      (claim matches a KB fact)
- CONTRADICTED   (claim contradicts a KB fact)
- UNKNOWN        (no KB fact on this subject + predicate)

Author: Samuel Eno Sunday
License: MIT
"""

import csv
import sys
from pathlib import Path


# -------------------------------------------------------------
# NORMALIZATION
# -------------------------------------------------------------

def normalize(text):
    """Normalize a string for comparison: lowercase + strip whitespace."""
    return text.strip().lower()


# -------------------------------------------------------------
# LOADING
# -------------------------------------------------------------

def load_knowledge(csv_path):
    """
    Load the knowledge base into a dict keyed by (subject, predicate).
    Value is the object (fact).
    """
    kb = {}
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (normalize(row["subject"]), normalize(row["predicate"]))
            kb[key] = {
                "object": normalize(row["object"]),
                "source": row.get("source", ""),
            }
    return kb


def load_claims(csv_path):
    """Load claims as a list of dicts."""
    claims = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            claims.append({
                "claim_id": row["claim_id"],
                "subject": normalize(row["subject"]),
                "predicate": normalize(row["predicate"]),
                "object": normalize(row["object"]),
            })
    return claims


# -------------------------------------------------------------
# DETECTION LOGIC
# -------------------------------------------------------------

def check_claim(claim, kb):
    """
    Check a single claim against the knowledge base.
    Returns a dict with: verdict, confidence, matched_fact.
    """
    key = (claim["subject"], claim["predicate"])

    if key not in kb:
        return {
            "verdict": "UNKNOWN",
            "confidence": 0.0,
            "matched_fact": None,
            "source": None,
        }

    kb_fact = kb[key]

    if claim["object"] == kb_fact["object"]:
        return {
            "verdict": "SUPPORTED",
            "confidence": 1.0,
            "matched_fact": kb_fact["object"],
            "source": kb_fact["source"],
        }

    return {
        "verdict": "CONTRADICTED",
        "confidence": 1.0,
        "matched_fact": kb_fact["object"],
        "source": kb_fact["source"],
    }


# -------------------------------------------------------------
# REPORTING
# -------------------------------------------------------------

def print_report(claims, kb):
    """Run all claims and print a clean report."""
    print("=" * 60)
    print("LLM HALLUCINATION DETECTOR — REPORT")
    print("=" * 60)
    print(f"Total claims checked: {len(claims)}")
    print(f"Knowledge base size: {len(kb)} facts\n")

    counts = {"SUPPORTED": 0, "CONTRADICTED": 0, "UNKNOWN": 0}

    for claim in claims:
        result = check_claim(claim, kb)
        counts[result["verdict"]] += 1

        print(f"[{claim['claim_id']}] {claim['subject']} {claim['predicate']} {claim['object']}")
        print(f"  Verdict: {result['verdict']} (confidence: {result['confidence']:.2f})")

        if result["verdict"] == "CONTRADICTED":
            print(f"  KB says: {result['matched_fact']}  ({result['source']})")
        elif result["verdict"] == "SUPPORTED":
            print(f"  KB confirms: {result['matched_fact']}  ({result['source']})")
        else:
            print("  No matching fact in KB — cannot verify.")

        print()

    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"SUPPORTED:     {counts['SUPPORTED']}")
    print(f"CONTRADICTED:  {counts['CONTRADICTED']}")
    print(f"UNKNOWN:       {counts['UNKNOWN']}")
    print(f"Total:         {sum(counts.values())}")

    contradicted_pct = (
        (counts["CONTRADICTED"] / len(claims) * 100) if claims else 0
    )
    print(f"\nHallucination rate: {contradicted_pct:.1f}% "
          f"({counts['CONTRADICTED']}/{len(claims)} claims contradicted)")
    print("=" * 60)


# -------------------------------------------------------------
# ENTRY POINT
# -------------------------------------------------------------

def main():
    kb_path = "sample_knowledge.csv"
    claims_path = "sample_claims.csv"

    if len(sys.argv) > 2:
        kb_path = sys.argv[1]
        claims_path = sys.argv[2]

    if not Path(kb_path).exists():
        print(f"Error: Knowledge base not found -> {kb_path}")
        sys.exit(1)

    if not Path(claims_path).exists():
        print(f"Error: Claims file not found -> {claims_path}")
        sys.exit(1)

    print(f"Loading knowledge base from: {kb_path}")
    print(f"Loading claims from: {claims_path}\n")

    kb = load_knowledge(kb_path)
    claims = load_claims(claims_path)

    print_report(claims, kb)


if __name__ == "__main__":
    main()
