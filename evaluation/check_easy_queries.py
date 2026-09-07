import json
import sqlite3

DATABASE_PATH = "data/sqlite/olist.db"
GROUND_TRUTH_PATH = "evaluation/ground_truth_easy.json"


def main():
    with open(GROUND_TRUTH_PATH, "r", encoding="utf-8") as file:
        questions = json.load(file)

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    print("=" * 60)
    print("EASY BENCHMARK - GROUND TRUTH VERIFICATION")
    print("=" * 60)

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

        except Exception as error:
            print("STATUS: FAIL")
            print(f"ERROR: {error}")

    connection.close()

    print("\n" + "=" * 60)
    print("VERIFICATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()