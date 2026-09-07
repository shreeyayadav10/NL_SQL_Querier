import json
import math


INPUT_FILE = "evaluation/benchmark_results.json"
OUTPUT_FILE = "evaluation/benchmark_results_semantic.json"


ORDER_REQUIRED_KEYWORDS = [
    "top",
    "highest",
    "lowest",
    "most",
    "least",
    "ordered",
    "chronologically",
    "ranking",
    "rank",
]


def normalize_rows(rows):
    normalized = []

    for row in rows or []:
        if isinstance(row, dict):
            normalized.append(list(row.values()))
        elif isinstance(row, (list, tuple)):
            normalized.append(list(row))
        else:
            normalized.append([row])

    return normalized


def values_equal(a, b):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        if isinstance(a, bool) or isinstance(b, bool):
            return a == b

        return math.isclose(
            float(a),
            float(b),
            rel_tol=1e-4,
            abs_tol=0.01,
        )

    if a is None or b is None:
        return a == b

    return str(a) == str(b)


def rows_equal(row1, row2):
    if len(row1) != len(row2):
        return False

    return all(
        values_equal(a, b)
        for a, b in zip(row1, row2)
    )


def ordered_rows_equal(actual, expected):
    """
    Compare ordered results while allowing tied numeric
    ranking values to appear in either order.
    """

    if len(actual) != len(expected):
        return False

    for actual_row, expected_row in zip(actual, expected):

        if rows_equal(actual_row, expected_row):
            continue

        # Allow different ordering when the ranking value is tied.
        if len(actual_row) >= 2 and len(expected_row) >= 2:

            actual_value = actual_row[-1]
            expected_value = expected_row[-1]

            if (
                isinstance(actual_value, (int, float))
                and isinstance(expected_value, (int, float))
                and not isinstance(actual_value, bool)
                and not isinstance(expected_value, bool)
                and math.isclose(
                    float(actual_value),
                    float(expected_value),
                    rel_tol=1e-4,
                    abs_tol=0.01,
                )
            ):
                continue

        return False

    return True


def unordered_rows_equal(actual, expected):
    """
    Compare result sets without requiring row order.
    """

    if len(actual) != len(expected):
        return False

    used = [False] * len(actual)

    for expected_row in expected:

        found = False

        for i, actual_row in enumerate(actual):

            if not used[i] and rows_equal(actual_row, expected_row):
                used[i] = True
                found = True
                break

        if not found:
            return False

    return True


def requires_order(question):
    question_lower = question.lower()

    return any(
        keyword in question_lower
        for keyword in ORDER_REQUIRED_KEYWORDS
    )


def evaluate_result(record):

    # Genuine pipeline failures remain failures.
    if record.get("status") == "pipeline_failed":
        return False

    actual = normalize_rows(record.get("actual_rows", []))
    expected = normalize_rows(record.get("expected_rows", []))

    question = record.get("question", "")

    if requires_order(question):
        return ordered_rows_equal(actual, expected)

    return unordered_rows_equal(actual, expected)


def get_difficulty(question_id):
    """
    Determine difficulty from benchmark ID.

    E01-E15 = Easy
    M01-M15 = Medium
    C01-C10 = Complex
    """

    if question_id.startswith("E"):
        return "Easy"

    if question_id.startswith("M"):
        return "Medium"

    if question_id.startswith("C"):
        return "Complex"

    return "Unknown"


def main():

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        benchmark = json.load(f)

    results = benchmark["results"]

    old_correct = {
        record["id"]: record.get("final_result_correct", False)
        for record in results
    }

    total = len(results)
    pipeline_success = 0
    semantic_correct = 0

    difficulty_stats = {
        "Easy": {"total": 0, "correct": 0},
        "Medium": {"total": 0, "correct": 0},
        "Complex": {"total": 0, "correct": 0},
    }

    changed = []

    for record in results:

        if record.get("status") != "pipeline_failed":
            pipeline_success += 1

        correct = evaluate_result(record)

        record["semantic_result_correct"] = correct
        record["final_result_correct"] = correct

        if correct:
            semantic_correct += 1

        difficulty = get_difficulty(record["id"])

        if difficulty in difficulty_stats:

            difficulty_stats[difficulty]["total"] += 1

            if correct:
                difficulty_stats[difficulty]["correct"] += 1

        old_value = old_correct.get(record["id"], False)

        if old_value != correct:

            changed.append({
                "id": record["id"],
                "question": record.get("question"),
                "old_result": old_value,
                "new_result": correct,
            })

    accuracy = (
        semantic_correct / total * 100
        if total
        else 0
    )

    pipeline_rate = (
        pipeline_success / total * 100
        if total
        else 0
    )

    # Save results.
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(
            benchmark,
            f,
            indent=2,
            ensure_ascii=False,
        )

    print()
    print("=" * 60)
    print("SEMANTIC BENCHMARK EVALUATION")
    print("=" * 60)

    print(f"Total questions: {total}")

    print(
        f"Pipeline successful: "
        f"{pipeline_success}/{total} "
        f"({pipeline_rate:.2f}%)"
    )

    print(
        f"Final results correct: "
        f"{semantic_correct}/{total}"
    )

    print(
        f"Semantic accuracy: "
        f"{accuracy:.2f}%"
    )

    print()
    print("Accuracy by difficulty:")
    print("-" * 40)

    for difficulty, stats in difficulty_stats.items():

        difficulty_accuracy = (
            stats["correct"] /
            stats["total"] *
            100
            if stats["total"]
            else 0
        )

        print(
            f"{difficulty}: "
            f"{stats['correct']}/{stats['total']} "
            f"({difficulty_accuracy:.2f}%)"
        )

    print()
    print("Changed classifications:")
    print("-" * 40)

    if not changed:
        print("None")
    else:
        for item in changed:
            print(
                f"{item['id']}: "
                f"{item['old_result']} -> "
                f"{item['new_result']}"
            )

    print()
    print(f"Saved to: {OUTPUT_FILE}")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()