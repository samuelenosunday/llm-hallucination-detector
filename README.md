# LLM Hallucination Detector

A Python tool that checks LLM claims against a **verified knowledge base** and flags them as:

- **SUPPORTED** — a matching fact exists in the knowledge base
- **CONTRADICTED** — a fact in the knowledge base contradicts the claim
- **UNKNOWN** — no matching or contradicting fact exists

Built for AI trainers, evaluators, and QA reviewers who need to catch hallucinations in LLM outputs at scale.

---

## What It Does

Given a claim and a knowledge base of verified facts, the tool:

1. **Direct lookup** — checks whether the claim is present verbatim in the KB
2. **Entity overlap** — finds KB facts about the same subject + predicate
3. **Contradiction detection** — flags claims that conflict with a known fact

Each claim gets:
- A **verdict** (SUPPORTED / CONTRADICTED / UNKNOWN)
- A **confidence score** (0–1)
- The **matched KB entry** (so reviewers can adjudicate)

---

## Why I Built This

Hallucination detection is the #1 pain point in LLM deployment. Models confidently state falsehoods — wrong capitals, fabricated citations, inverted historical facts — and human reviewers have to catch them.

This tool automates the first pass. It doesn't replace human review (some hallucinations require nuance the tool can't handle), but it flags the obvious ones instantly, so reviewers can focus on ambiguous cases.

It pairs with my [LLM Response Evaluator](https://github.com/samuelenosunday/llm-response-evaluator) — that tool scores output quality; this one verifies factual accuracy.

---

## Data Format

### Knowledge base (`sample_knowledge.csv`)

| Column | Example |
|---|---|
| `subject` | "capital of Nigeria" |
| `predicate` | "is" |
| `object` | "Abuja" |
| `source` | "CIA World Factbook" |

### Claims (`sample_claims.csv`)

| Column | Example |
|---|---|
| `claim_id` | "C-001" |
| `subject` | "capital of Nigeria" |
| `predicate` | "is" |
| `object` | "Abuja" |

---

## How to Run It

    python detect.py

Optional: pass custom files

    python detect.py sample_knowledge.csv sample_claims.csv

---

## Output Example

The tool prints a report to the console:

- Total claims checked
- Per-claim verdict with confidence
- Summary counts (supported, contradicted, unknown)
- Per-claim matched KB entry (for CONTRADICTED and SUPPORTED)

Example verdict for a claim "The capital of Nigeria is Lagos":

- **CONTRADICTED** (confidence: 0.95)
- Matched KB fact: "capital of Nigeria | is | Abuja"

---

## Files in This Repo

| File | Purpose |
|---|---|
| `detect.py` | Main detection script |
| `sample_knowledge.csv` | 30 verified facts (capitals, presidents, science) |
| `sample_claims.csv` | 15 claims (true, false, ambiguous) |
| `README.md` | This documentation |

---

## Tech Stack

- **Language:** Python 3
- **Dependencies:** None (standard library only)
- **Data format:** CSV

---

## Limitations

- **Rule-based matching**, not semantic inference — it detects contradictions on *structured* facts, not free-text claims.
- **Knowledge base scope** — the tool only catches claims that overlap with the KB. Real-world deployment requires a much larger KB (or external APIs like Wikipedia/Wikidata).
- **Aliases and paraphrasing** — if the KB says "USA" and the claim says "United States," the tool may miss the match. A production system would need synonym resolution.
- **Not a replacement for human review** — this is a first-pass screen. Ambiguous cases should always go to a human adjudicator.

---

## Future Improvements

- Add Wikipedia API integration for broader coverage
- Add synonym/alias resolution (e.g., USA ↔ United States)
- Add support for date-based claims ("X happened in 1999")
- Add batch mode for processing full LLM output logs
- Fine-tune a small classifier on (claim, KB fact) pairs

---

## About the Author

**Samuel Eno Sunday** — AI Training Specialist & LLM Quality Analyst

- LinkedIn: [linkedin.com/in/samuelenosunday001](https://www.linkedin.com/in/samuelenosunday001/)
- GitHub: [github.com/samuelenosunday](https://github.com/samuelenosunday)
- Email: samuelenosunday@gmail.com

*Open to remote contract, part-time, and project-based AI training roles.*
