"""
validate_database.py

Validates the integrity and expected structure of the Olist
SQLite database.
"""

from sqlalchemy import text

from app.database.database import engine
from app.utils.logger import get_logger


logger = get_logger(__name__)


EXPECTED_ROW_COUNTS = {
    "customers": 99_441,
    "orders": 99_441,
    "order_items": 112_650,
    "payments": 103_886,
    "reviews": 99_224,
    "products": 32_951,
    "sellers": 3_095,
    "geolocation": 738_332,
    "category_translation": 71,
}


def get_row_count(connection, table_name):
    """
    Return the number of rows in a table.
    """

    result = connection.execute(
        text(f"SELECT COUNT(*) FROM {table_name}")
    )

    return result.scalar()


def validate_row_counts(connection):
    """
    Compare actual table row counts with expected counts.
    """

    logger.info("Validating row counts...")

    all_counts_valid = True

    for table_name, expected_count in EXPECTED_ROW_COUNTS.items():

        actual_count = get_row_count(
            connection,
            table_name
        )

        if actual_count == expected_count:

            print(
                f"PASS | {table_name:<25} "
                f"{actual_count:>10,} rows"
            )

        else:

            print(
                f"FAIL | {table_name:<25} "
                f"Expected: {expected_count:,} | "
                f"Actual: {actual_count:,}"
            )

            all_counts_valid = False

    return all_counts_valid


def validate_foreign_keys(connection):
    """
    Check for orphan records across important relationships.
    """

    logger.info("Validating foreign-key relationships...")

    checks = {

        "orders → customers": """
            SELECT COUNT(*)
            FROM orders o
            LEFT JOIN customers c
                ON o.customer_id = c.customer_id
            WHERE c.customer_id IS NULL
        """,

        "order_items → orders": """
            SELECT COUNT(*)
            FROM order_items oi
            LEFT JOIN orders o
                ON oi.order_id = o.order_id
            WHERE o.order_id IS NULL
        """,

        "order_items → products": """
            SELECT COUNT(*)
            FROM order_items oi
            LEFT JOIN products p
                ON oi.product_id = p.product_id
            WHERE p.product_id IS NULL
        """,

        "order_items → sellers": """
            SELECT COUNT(*)
            FROM order_items oi
            LEFT JOIN sellers s
                ON oi.seller_id = s.seller_id
            WHERE s.seller_id IS NULL
        """,

        "payments → orders": """
            SELECT COUNT(*)
            FROM payments p
            LEFT JOIN orders o
                ON p.order_id = o.order_id
            WHERE o.order_id IS NULL
        """,

        "reviews → orders": """
            SELECT COUNT(*)
            FROM reviews r
            LEFT JOIN orders o
                ON r.order_id = o.order_id
            WHERE o.order_id IS NULL
        """
    }

    all_relationships_valid = True

    for relationship_name, query in checks.items():

        result = connection.execute(
            text(query)
        )

        orphan_count = result.scalar()

        if orphan_count == 0:

            print(
                f"PASS | {relationship_name:<30} "
                f"No orphan records"
            )

        else:

            print(
                f"FAIL | {relationship_name:<30} "
                f"{orphan_count:,} orphan records"
            )

            all_relationships_valid = False

    return all_relationships_valid


def validate_database():

    print("\n")
    print("=" * 70)
    print("OLIST DATABASE VALIDATION")
    print("=" * 70)

    with engine.connect() as connection:

        row_counts_valid = validate_row_counts(
            connection
        )

        print()

        relationships_valid = validate_foreign_keys(
            connection
        )

    print()
    print("=" * 70)

    if row_counts_valid and relationships_valid:

        print("DATABASE VALIDATION PASSED")

        logger.info(
            "All database validation checks passed."
        )

        return True

    print("DATABASE VALIDATION FAILED")

    logger.error(
        "One or more database validation checks failed."
    )

    return False


if __name__ == "__main__":

    validate_database()