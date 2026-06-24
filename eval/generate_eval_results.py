"""Generate answers for the evaluation dataset using the RAG pipeline."""

from pathlib import Path
import json
import pandas as pd
from src.rag_pipeline import answer_question
from src.vector_store import load_vector_store

RESULTS_DIR = Path("eval/results")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def generate_eval_results() -> pd.DataFrame:
    test_set = pd.read_csv("eval/test_set.csv")
    vector_store = load_vector_store()
    rows = []

    for _, row in test_set.iterrows():
        result = answer_question(row["question"], vector_store=vector_store)
        rows.append(
            {
                "question": row["question"],
                "ground_truth": row["ground_truth"],
                "answer": result["answer"],
                "contexts": json.dumps(result["contexts"], ensure_ascii=False),
                "expected_source": row["expected_source"],
                "retrieved_sources": json.dumps(result["sources"], ensure_ascii=False),
                "type": row["type"],
            }
        )

    results = pd.DataFrame(rows)
    output_path = RESULTS_DIR / "generated_answers.csv"
    results.to_csv(output_path, index=False)
    print(f"Saved generated answers to {output_path}")
    return results


if __name__ == "__main__":
    generate_eval_results()
