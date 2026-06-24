# AGENTS.md

## Project context

This is a RAG Evaluation Lab portfolio project. It demonstrates a small Retrieval-Augmented Generation Q&A app with automated quality evaluation using RAGAS, DeepEval, pytest, and GitHub Actions.

## Before pushing changes

Run the pre-push review skill.

## Required checks

Run:

```bash
pytest tests/
python eval/generate_eval_results.py
python eval/evaluate_with_ragas.py
python eval/summarize_results.py

## Pre-push review

When the user says `/pre-push-review`, `prepush`, or “run the pre-push review”, use the skill located at:

.agents/skills/pre-push-review/SKILL.md

Follow its checklist exactly and summarize:
- Files changed
- Checks run
- Results
- Risks
- Recommended next action