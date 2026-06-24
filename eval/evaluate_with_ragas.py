"""Evaluate generated RAG answers with RAGAS.

RAGAS versions evolve quickly. This script uses the common evaluate() API and
keeps the data conversion explicit so changes are easy to debug.
"""

from pathlib import Path
import json
import pandas as pd
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision

RESULTS_DIR = Path("eval/results")


def evaluate_with_ragas() -> pd.DataFrame:
    input_path = RESULTS_DIR / "generated_answers.csv"
    if not input_path.exists():
        raise FileNotFoundError("Run `python eval/generate_eval_results.py` first.")

    df = pd.read_csv(input_path)

    dataset = Dataset.from_dict(
        {
            "question": df["question"].tolist(),
            "answer": df["answer"].tolist(),
            "contexts": df["contexts"].apply(json.loads).tolist(),
            "ground_truth": df["ground_truth"].tolist(),
        }
    )

    result = evaluate(
        dataset=dataset,
        metrics=[faithfulness, answer_relevancy, context_precision],
    )

    result_df = result.to_pandas()
    output_path = RESULTS_DIR / "ragas_results.csv"
    result_df.to_csv(output_path, index=False)
    print(f"Saved RAGAS results to {output_path}")
    print(result_df)
    return result_df


if __name__ == "__main__":
    evaluate_with_ragas()
