import json
import sqlite3
import time
from pathlib import Path
from statistics import mean, median

from app.pipeline.query_pipeline import QueryPipeline


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

QUESTIONS_FILE = PROJECT_ROOT / "evaluation" / "benchmark_questions.json"
GROUND_TRUTH_FILES = [
    PROJECT_ROOT / "evaluation" / "ground_truth_easy.json",
    PROJECT_ROOT / "evaluation" / "ground_truth_medium.json",
    PROJECT_ROOT / "evaluation" / "ground_truth_complex.json",
]

DATABASE_PATH = PROJECT_ROOT / "data" / "sqlite" / "olist.db"
OUTPUT_FILE = PROJECT_ROOT / "evaluation" / "benchmark_results.json"


# ---------------------------------------------------------
# Load JSON
# ---------------------------------------------------------

def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


# ---------------------------------------------------------
# Load benchmark questions
# ---------------------------------------------------------

def load_questions():
    data = load_json(QUESTIONS_FILE)

    if isinstance(data, dict):
        questions = data.get("questions", [])

        if not questions:
            questions = data.get("benchmark_questions", [])

        return questions

    return data


# ---------------------------------------------------------
# Load ground truth
# ---------------------------------------------------------

def load_ground_truth():
    ground_truth = {}

    for file_path in GROUND_TRUTH_FILES:
        data = load_json(file_path)

        for entry in data:
            question_id = entry.get("id")

            if question_id:
                ground_truth[question_id] = entry

    return ground_truth


# ---------------------------------------------------------
# Normalize row values
# ---------------------------------------------------------

def normalize_row(row):
    """
    Converts database rows into a comparable list of values.

    SQLExecutor returns rows as dictionaries:
        {"total_orders": 99441}

    Ground-truth SQLite execution returns rows as tuples:
        (99441,)

    Both become:
        [99441]
    """

    if isinstance(row, dict):
        return list(row.values())

    if isinstance(row, (list, tuple)):
        return list(row)

    return [row]


# ---------------------------------------------------------
# Compare two values
# ---------------------------------------------------------

def values_equal(actual_value, expected_value):
    """
    Compare individual SQL result values.

    Numeric values are compared using a small tolerance.
    Everything else is compared as strings.
    """

    if isinstance(actual_value, (int, float)) and isinstance(
        expected_value, (int, float)
    ):
        return abs(actual_value - expected_value) <= 1e-6

    return str(actual_value) == str(expected_value)


# ---------------------------------------------------------
# Compare SQL result rows
# ---------------------------------------------------------

def rows_equal(actual_rows, expected_rows):
    """
    Compare SQL result rows while ignoring column aliases.

    Example:

    Actual:
        [{"total_orders": 99441}]

    Expected:
        [[99441]]

    These should be considered equal.
    """

    if len(actual_rows) != len(expected_rows):
        return False

    for actual_row, expected_row in zip(actual_rows, expected_rows):

        actual_values = normalize_row(actual_row)
        expected_values = normalize_row(expected_row)

        if len(actual_values) != len(expected_values):
            return False

        for actual_value, expected_value in zip(
            actual_values,
            expected_values
        ):
            if not values_equal(actual_value, expected_value):
                return False

    return True


# ---------------------------------------------------------
# Execute ground-truth SQL
# ---------------------------------------------------------

def execute_expected_sql(connection, sql):
    cursor = connection.cursor()

    cursor.execute(sql)

    rows = cursor.fetchall()

    return [list(row) for row in rows]


# ---------------------------------------------------------
# Main benchmark
# ---------------------------------------------------------

def main():

    print("=" * 70)
    print("NL-SQL QUERIER - 40 QUESTION BENCHMARK")
    print("=" * 70)

    questions = load_questions()
    ground_truth = load_ground_truth()

    print(f"\nQuestions loaded: {len(questions)}")
    print(f"Ground-truth queries loaded: {len(ground_truth)}")

    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DATABASE_PATH}"
        )

    connection = sqlite3.connect(DATABASE_PATH)

    # Row factory is intentionally NOT enabled here.
    # Ground truth will therefore return tuples/lists.
    pipeline = QueryPipeline()

    results = []

    print("\nStarting benchmark...\n")

    for index, question_data in enumerate(questions, start=1):

        question_id = question_data["id"]
        question = question_data["question"]

        print("-" * 70)
        print(f"[{index}/{len(questions)}] {question_id}")
        print(f"Question: {question}")

        if question_id not in ground_truth:
            print("ERROR: Ground truth not found")
            continue

        expected_sql = ground_truth[question_id]["expected_sql"]

        # -------------------------------------------------
        # Execute expected SQL
        # -------------------------------------------------

        try:
            expected_rows = execute_expected_sql(
                connection,
                expected_sql
            )
        except Exception as error:
            print(f"Ground-truth SQL failed: {error}")

            results.append({
                "id": question_id,
                "question": question,
                "status": "ground_truth_error",
                "generated_sql": None,
                "expected_sql": expected_sql,
                "actual_rows": None,
                "expected_rows": None,
                "final_result_correct": False,
                "correction_attempts": None,
                "response_time_seconds": None,
                "error": str(error),
            })

            continue

        # -------------------------------------------------
        # Run actual NL-SQL pipeline
        # -------------------------------------------------

        start_time = time.perf_counter()

        try:
            pipeline_result = pipeline.run(question)

            response_time = time.perf_counter() - start_time

        except Exception as error:

            response_time = time.perf_counter() - start_time

            print(f"Pipeline error: {error}")

            results.append({
                "id": question_id,
                "question": question,
                "status": "pipeline_error",
                "generated_sql": None,
                "expected_sql": expected_sql,
                "actual_rows": None,
                "expected_rows": expected_rows,
                "final_result_correct": False,
                "correction_attempts": None,
                "response_time_seconds": round(
                    response_time,
                    4
                ),
                "error": str(error),
            })

            continue

        # -------------------------------------------------
        # Extract result
        # -------------------------------------------------

        success = pipeline_result.get("success", False)

        generated_sql = pipeline_result.get("sql")

        actual_rows = pipeline_result.get("rows", [])

        correction_attempts = pipeline_result.get(
            "correction_attempts",
            0
        )

        # -------------------------------------------------
        # Compare results
        # -------------------------------------------------

        if success:

            final_result_correct = rows_equal(
                actual_rows,
                expected_rows
            )

            status = "completed"

        else:

            final_result_correct = False

            status = "pipeline_failed"

        # -------------------------------------------------
        # Print result
        # -------------------------------------------------

        if final_result_correct:
            print("RESULT: CORRECT")
        else:
            print("RESULT: INCORRECT")

        print(
            f"Correction attempts: {correction_attempts}"
        )

        print(
            f"Response time: {response_time:.2f} seconds"
        )

        # -------------------------------------------------
        # Save result
        # -------------------------------------------------

        results.append({
            "id": question_id,
            "question": question,
            "status": status,
            "generated_sql": generated_sql,
            "expected_sql": expected_sql,
            "actual_rows": actual_rows,
            "expected_rows": expected_rows,
            "final_result_correct": final_result_correct,
            "correction_attempts": correction_attempts,
            "response_time_seconds": round(
                response_time,
                4
            ),
        })

    connection.close()

    # -----------------------------------------------------
    # Calculate metrics
    # -----------------------------------------------------

    total_questions = len(results)

    pipeline_successful = sum(
        1
        for result in results
        if result["status"] == "completed"
    )

    final_results_correct = sum(
        1
        for result in results
        if result["final_result_correct"]
    )

    completed_without_correction = sum(
        1
        for result in results
        if (
            result["status"] == "completed"
            and result["correction_attempts"] == 0
        )
    )

    completed_with_correction = sum(
        1
        for result in results
        if (
            result["status"] == "completed"
            and result["correction_attempts"] > 0
        )
    )

    response_times = [
        result["response_time_seconds"]
        for result in results
        if result["response_time_seconds"] is not None
    ]

    # -----------------------------------------------------
    # Percentages
    # -----------------------------------------------------

    if total_questions > 0:

        final_result_accuracy = (
            final_results_correct
            / total_questions
            * 100
        )

        pipeline_success_rate = (
            pipeline_successful
            / total_questions
            * 100
        )

        no_correction_rate = (
            completed_without_correction
            / total_questions
            * 100
        )

        correction_rate = (
            completed_with_correction
            / total_questions
            * 100
        )

    else:

        final_result_accuracy = 0
        pipeline_success_rate = 0
        no_correction_rate = 0
        correction_rate = 0

    # -----------------------------------------------------
    # Summary
    # -----------------------------------------------------

    summary = {
        "total_questions": total_questions,
        "pipeline_successful": pipeline_successful,
        "final_results_correct": final_results_correct,
        "final_result_accuracy_percent": round(
            final_result_accuracy,
            2
        ),
        "completed_without_correction": completed_without_correction,
        "completed_with_correction": completed_with_correction,
        "no_correction_rate_percent": round(
            no_correction_rate,
            2
        ),
        "correction_rate_percent": round(
            correction_rate,
            2
        ),
        "pipeline_success_rate_percent": round(
            pipeline_success_rate,
            2
        ),
        "average_response_time_seconds": round(
            mean(response_times),
            4
        ) if response_times else None,
        "median_response_time_seconds": round(
            median(response_times),
            4
        ) if response_times else None,
    }

    # -----------------------------------------------------
    # Final output
    # -----------------------------------------------------

    benchmark_output = {
        "summary": summary,
        "results": results,
    }

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            benchmark_output,
            file,
            indent=2,
            ensure_ascii=False
        )

    print("\n")
    print("=" * 70)
    print("BENCHMARK COMPLETE")
    print("=" * 70)

    print(
        f"Pipeline successful: "
        f"{pipeline_successful}/{total_questions}"
    )

    print(
        f"Final results correct: "
        f"{final_results_correct}/{total_questions}"
    )

    print(
        f"Final result accuracy: "
        f"{final_result_accuracy:.2f}%"
    )

    print(
        f"Completed without correction: "
        f"{completed_without_correction}/{total_questions}"
    )

    print(
        f"No-correction rate: "
        f"{no_correction_rate:.2f}%"
    )

    print(
        f"Completed with correction: "
        f"{completed_with_correction}/{total_questions}"
    )

    print(
        f"Correction rate: "
        f"{correction_rate:.2f}%"
    )

    if response_times:

        print(
            f"Average response time: "
            f"{mean(response_times):.2f} seconds"
        )

        print(
            f"Median response time: "
            f"{median(response_times):.2f} seconds"
        )

    print(
        f"\nResults saved to:\n{OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()