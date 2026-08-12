"""
check_indexes.py

Displays all indexes currently defined in the SQLite database.
"""

from sqlalchemy import inspect

from app.database.database import engine


def check_indexes():

    inspector = inspect(engine)

    print("\nDatabase Indexes")
    print("=" * 70)

    for table_name in inspector.get_table_names():

        indexes = inspector.get_indexes(table_name)

        if not indexes:
            continue

        print(f"\n{table_name}")

        for index in indexes:

            print(
                f"  ✓ {index['name']}"
            )


if __name__ == "__main__":
    check_indexes()