# RAG Evaluation Lab

A small Retrieval-Augmented Generation Q&A app with an evaluation harness for measuring RAG quality using RAGAS, DeepEval, pytest, and GitHub Actions.

This project is designed as a portfolio piece for QA/SDET, automation, and AI testing roles. It shows not only how to build a small RAG app, but how to evaluate it systematically.

## What this project demonstrates

- Markdown document ingestion
- Text chunking strategy
- Vector search with ChromaDB
- RAG answer generation with LangChain and OpenAI
- Streamlit UI for interactive Q&A
- Evaluation dataset design
- RAGAS evaluation for faithfulness, context precision, and answer relevancy
- DeepEval evaluation for faithfulness and answer relevancy
- Deterministic pytest checks for retrieval and out-of-scope behavior
- GitHub Actions pipeline with artifacts

## Architecture

```text
User question
   ↓
Streamlit app or eval script
   ↓
Retriever searches ChromaDB
   ↓
Top-k chunks are injected into prompt
   ↓
LLM generates grounded answer
   ↓
RAGAS / DeepEval / pytest evaluate quality
```

## Why RAG evaluation matters

RAG systems can produce fluent answers that are not supported by the retrieved evidence. This project evaluates three important quality dimensions:

| Metric | What it checks |
|---|---|
| Faithfulness | Whether the answer is supported by the retrieved context |
| Context precision | Whether relevant retrieved chunks are ranked above irrelevant ones |
| Answer relevancy | Whether the answer actually addresses the question |

## Project structure

```text
rag-evaluation-lab/
  app/
    streamlit_app.py
  src/
    config.py
    ingest.py
    chunking.py
    vector_store.py
    rag_pipeline.py
    prompts.py
  docs/
    shafu_band_bio.md
    shafu_discography.md
    shafu_live_setup.md
    v13rnes_fest.md
    press_kit.md
  eval/
    test_set.csv
    generate_eval_results.py
    evaluate_with_ragas.py
    evaluate_with_deepeval.py
    summarize_results.py
    results/
  tests/
    conftest.py
    test_ingestion.py
    test_retrieval.py
    test_rag_pipeline.py
  .github/
    workflows/
      rag-eval.yml
  requirements.txt
  .env.example
```

## Setup

### 1. Create a virtual environment

```bash
python -m venv .venv
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Then add your API key:

```env
OPENAI_API_KEY=your_api_key_here
```

## Run the app

First ingest the documents:

```bash
python -m src.ingest
```

Then run Streamlit:

```bash
streamlit run app/streamlit_app.py
```

## Run the evaluation flow

```bash
python -m src.ingest
python eval/generate_eval_results.py
python eval/evaluate_with_ragas.py
python eval/evaluate_with_deepeval.py
python eval/summarize_results.py
```

Generated files are saved under:

```text
eval/results/
```

## Run deterministic tests

```bash
pytest tests/
```

## Evaluation dataset design

The dataset includes:

| Type | Purpose |
|---|---|
| factual | Validate direct fact retrieval |
| multi_hop | Validate synthesis across related facts |
| out_of_scope | Validate hallucination resistance |
| ambiguous | Validate grounded answers under unclear phrasing |

Example:

```csv
question,ground_truth,expected_source,type
Who are the members of Sha-Fu?,"Oni plays guitar, Xze plays bass, and Yorsh plays drums.",shafu_band_bio.md,factual
```

## Suggested portfolio explanation

> I built a small RAG Q&A application, but the focus was the evaluation layer. I designed a test set with factual, multi-hop, ambiguous, and out-of-scope questions, then measured faithfulness, context precision, and answer relevancy using RAGAS and DeepEval. I also added deterministic pytest checks and a GitHub Actions workflow so prompt, retrieval, and chunking changes can be evaluated continuously.

## Future improvements

- Add FastAPI endpoint
- Add Docker support
- Add reranking
- Add synthetic test-set generation
- Add threshold-based CI gates
- Add HTML evaluation report
- Add local embedding option for lower-cost runs
