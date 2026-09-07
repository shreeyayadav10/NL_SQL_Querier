import json
import sqlite3


DATABASE_PATH = "data/sqlite/olist.db"
GROUND_TRUTH_PATH = "evaluation/ground_truth_medium.json"


def main():
    with open(GROUND_TRUTH_PATH, "r", encoding="utf-8") as file:
        questions = json.load(file)

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    print("=" * 60)
    print("MEDIUM BENCHMARK - GROUND TRUTH VERIFICATION")
    print("=" * 60)

    passed = 0
    failed = 0

    for item in questions:
        question_id = item["id"]
        question = item["question"]
        sql = item["expected_sql"]

        print(f"\n{question_id}: {question}")
        print(f"SQL: {sql}")

        try:
            cursor.execute(sql)
            result = cursor.fetchall()

            print("STATUS: PASS")
            print(f"RESULT: {result}")

            passed += 1

        except Exception as error:
            print("STATUS: FAIL")
            print(f"ERROR: {error}")

            failed += 1

    connection.close()

    print("\n" + "=" * 60)
    print("MEDIUM BENCHMARK SUMMARY")
    print("=" * 60)
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total:  {passed + failed}")

    print("\nVERIFICATION COMPLETE")


if __name__ == "__main__":
    main()