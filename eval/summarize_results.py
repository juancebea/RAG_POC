"""Create a compact summary of evaluation results."""

from pathlib import Path
import pandas as pd

RESULTS_DIR = Path("eval/results")


def summarize_ragas() -> None:
    ragas_path = RESULTS_DIR / "ragas_results.csv"
    if not ragas_path.exists():
        print("No ragas_results.csv found. Skipping RAGAS summary.")
        return

    df = pd.read_csv(ragas_path)
    numeric_cols = df.select_dtypes(include="number").columns

    summary = df[numeric_cols].mean().reset_index()
    summary.columns = ["metric", "average_score"]

    output_path = RESULTS_DIR / "ragas_summary.csv"
    summary.to_csv(output_path, index=False)
    print(f"Saved RAGAS summary to {output_path}")
    print(summary)


if __name__ == "__main__":
    summarize_ragas()
