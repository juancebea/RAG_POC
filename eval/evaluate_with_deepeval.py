"""Evaluate generated RAG answers with DeepEval."""

from pathlib import Path
import json
import pandas as pd
from deepeval import evaluate
from deepeval.metrics import FaithfulnessMetric, AnswerRelevancyMetric, ContextualPrecisionMetric
from deepeval.test_case import LLMTestCase

RESULTS_DIR = Path("eval/results")


def build_test_cases(df: pd.DataFrame) -> list[LLMTestCase]:
    test_cases: list[LLMTestCase] = []

    for _, row in df.iterrows():
        test_cases.append(
            LLMTestCase(
                input=row["question"],
                actual_output=row["answer"],
                expected_output=row["ground_truth"],
                retrieval_context=json.loads(row["contexts"]),
            )
        )

    return test_cases


def evaluate_with_deepeval() -> None:
    input_path = RESULTS_DIR / "generated_answers.csv"
    if not input_path.exists():
        raise FileNotFoundError("Run `python eval/generate_eval_results.py` first.")

    df = pd.read_csv(input_path)
    test_cases = build_test_cases(df)

    metrics = [
        FaithfulnessMetric(threshold=0.7),
        AnswerRelevancyMetric(threshold=0.7),
        ContextualPrecisionMetric(threshold=0.7),
    ]

    evaluate(test_cases=test_cases, metrics=metrics)


if __name__ == "__main__":
    evaluate_with_deepeval()
