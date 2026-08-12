"""
check_database.py

Checks database connectivity, tables, and row counts.
"""

from sqlalchemy import inspect, text

from app.database.database import engine


def check_database():

    inspector = inspect(engine)

    table_names = inspector.get_table_names()

    print("\nDatabase Connected Successfully.\n")

    print("Tables and Row Counts")
    print("=" * 50)

    with engine.connect() as connection:

        for table_name in table_names:

            result = connection.execute(
                text(
                    f"SELECT COUNT(*) FROM {table_name}"
                )
            )

            row_count = result.scalar()

            print(
                f"{table_name:<25} {row_count:>10,}"
            )


if __name__ == "__main__":
    check_database()