import json
import math
from pathlib import Path
from statistics import mean, median


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    PROJECT_ROOT
    / "evaluation"
    / "benchmark_results.json"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "evaluation"
    / "benchmark_results_reevaluated.json"
)


# ---------------------------------------------------------
# Normalize row
# ---------------------------------------------------------

def normalize_row(row):
    """
    Convert different SQL row formats into a list of values.

    Actual pipeline result example:
        {"total_orders": 99441}

    Ground-truth result example:
        [99441]

    Both become:
        [99441]
    """

    if isinstance(row, dict):
        return list(row.values())

    if isinstance(row, (list, tuple)):
        return list(row)

    return [row]


# ---------------------------------------------------------
# Compare individual values
# ---------------------------------------------------------

def values_equal(actual_value, expected_value):
    """
    Compare SQL result values.

    Numeric values use tolerance so that valid rounded
    results such as:

        4.16

    can match:

        4.155716524320005
    """

    # Handle numeric values
    if isinstance(actual_value, (int, float)) and isinstance(
        expected_value, (int, float)
    ):

        # Handle NaN values
        if isinstance(actual_value, float) and math.isnan(actual_value):
            return (
                isinstance(expected_value, float)
                and math.isnan(expected_value)
            )

        if isinstance(expected_value, float) and math.isnan(expected_value):
            return False

        return math.isclose(
            actual_value,
            expected_value,
            rel_tol=1e-4,
            abs_tol=0.01
        )

    # Handle everything else as strings
    return str(actual_value) == str(expected_value)


# ---------------------------------------------------------
# Compare rows
# ---------------------------------------------------------

def rows_equal(actual_rows, expected_rows):
    """
    Compare actual SQL results with expected SQL results.

    Column aliases are ignored.

    Row order is preserved because ORDER BY is part of
    the benchmark questions.
    """

    if actual_rows is None or expected_rows is None:
        return False

    if len(actual_rows) != len(expected_rows):
        return False

    for actual_row, expected_row in zip(
        actual_rows,
        expected_rows
    ):

        actual_values = normalize_row(actual_row)
        expected_values = normalize_row(expected_row)

        if len(actual_values) != len(expected_values):
            return False

        for actual_value, expected_value in zip(
            actual_values,
            expected_values
        ):

            if not values_equal(
                actual_value,
                expected_value
            ):
                return False

    return True


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    print("=" * 70)
    print("NL-SQL QUERIER - BENCHMARK RE-EVALUATION")
    print("=" * 70)

    # -----------------------------------------------------
    # Check input file
    # -----------------------------------------------------

    if not INPUT_FILE.exists():

        raise FileNotFoundError(
            f"Benchmark results not found:\n{INPUT_FILE}"
        )

    # -----------------------------------------------------
    # Load previous benchmark
    # -----------------------------------------------------

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        benchmark_data = json.load(file)

    results = benchmark_data.get(
        "results",
        []
    )

    if not results:
        raise ValueError(
            "No benchmark results found in benchmark_results.json"
        )

    print(
        f"\nExisting results loaded: {len(results)}"
    )

    # -----------------------------------------------------
    # Re-evaluate every result
    # -----------------------------------------------------

    correct_count = 0
    completed_count = 0
    completed_without_correction = 0
    completed_with_correction = 0

    response_times = []

    for result in results:

        status = result.get("status")

        actual_rows = result.get(
            "actual_rows"
        )

        expected_rows = result.get(
            "expected_rows"
        )

        correction_attempts = result.get(
            "correction_attempts",
            0
        )

        # ---------------------------------------------
        # Recalculate correctness
        # ---------------------------------------------

        if status == "completed":

            completed_count += 1

            final_result_correct = rows_equal(
                actual_rows,
                expected_rows
            )

        else:

            final_result_correct = False

        # ---------------------------------------------
        # Update result
        # ---------------------------------------------

        result["final_result_correct"] = (
            final_result_correct
        )

        # ---------------------------------------------
        # Count metrics
        # ---------------------------------------------

        if final_result_correct:
            correct_count += 1

        if status == "completed":

            if correction_attempts == 0:

                completed_without_correction += 1

            else:

                completed_with_correction += 1

        # ---------------------------------------------
        # Response time
        # ---------------------------------------------

        response_time = result.get(
            "response_time_seconds"
        )

        if response_time is not None:

            response_times.append(
                response_time
            )

        # ---------------------------------------------
        # Print result
        # ---------------------------------------------

        result_label = (
            "CORRECT"
            if final_result_correct
            else "INCORRECT"
        )

        print(
            f"{result.get('id', 'UNKNOWN')}: "
            f"{result_label}"
        )

    # -----------------------------------------------------
    # Calculate metrics
    # -----------------------------------------------------

    total_questions = len(results)

    if total_questions > 0:

        final_result_accuracy = (
            correct_count
            / total_questions
            * 100
        )

        pipeline_success_rate = (
            completed_count
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
    # Create new summary
    # -----------------------------------------------------

    summary = {
        "total_questions": total_questions,

        "pipeline_successful": completed_count,

        "final_results_correct": correct_count,

        "final_result_accuracy_percent": round(
            final_result_accuracy,
            2
        ),

        "completed_without_correction": (
            completed_without_correction
        ),

        "completed_with_correction": (
            completed_with_correction
        ),

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
    # Create output
    # -----------------------------------------------------

    reevaluated_data = {
        "summary": summary,
        "results": results
    }

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            reevaluated_data,
            file,
            indent=2,
            ensure_ascii=False
        )

    # -----------------------------------------------------
    # Display final metrics
    # -----------------------------------------------------

    print("\n")
    print("=" * 70)
    print("RE-EVALUATION COMPLETE")
    print("=" * 70)

    print(
        f"Total questions: "
        f"{total_questions}"
    )

    print(
        f"Pipeline successful: "
        f"{completed_count}/{total_questions}"
    )

    print(
        f"Final results correct: "
        f"{correct_count}/{total_questions}"
    )

    print(
        f"Final result accuracy: "
        f"{final_result_accuracy:.2f}%"
    )

    print(
        f"Completed without correction: "
        f"{completed_without_correction}/"
        f"{total_questions}"
    )

    print(
        f"No-correction rate: "
        f"{no_correction_rate:.2f}%"
    )

    print(
        f"Completed with correction: "
        f"{completed_with_correction}/"
        f"{total_questions}"
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
        f"\nRe-evaluated results saved to:\n"
        f"{OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()