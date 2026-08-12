"""
database_health.py

Runs a complete health check on the Olist SQLite database.

Checks:
1. Database connection
2. Required tables
3. Expected row counts
4. Foreign-key integrity
5. Orphan records
6. Required indexes
7. Metadata records
"""

from sqlalchemy import inspect, text

from app.database.database import engine
from app.database.validate_database import EXPECTED_ROW_COUNTS


REQUIRED_TABLES = {
    "customers",
    "orders",
    "order_items",
    "payments",
    "reviews",
    "products",
    "sellers",
    "geolocation",
    "category_translation",
    "dataset_metadata",
}


REQUIRED_INDEXES = {
    "orders": {
        "idx_orders_customer_id",
        "idx_orders_status",
        "idx_orders_purchase_timestamp",
    },
    "order_items": {
        "idx_order_items_order_id",
        "idx_order_items_product_id",
        "idx_order_items_seller_id",
    },
    "payments": {
        "idx_payments_order_id",
        "idx_payments_payment_type",
    },
    "reviews": {
        "idx_reviews_order_id",
        "idx_reviews_review_score",
    },
    "products": {
        "idx_products_category",
    },
    "customers": {
        "idx_customers_state",
        "idx_customers_city",
    },
    "sellers": {
        "idx_sellers_state",
        "idx_sellers_city",
    },
    "geolocation": {
        "idx_geolocation_zip",
    },
    "category_translation": {
        "idx_translation_english",
    },
}


def check_connection():

    try:

        with engine.connect() as connection:

            connection.execute(text("SELECT 1"))

        return True

    except Exception:

        return False


def check_tables():

    inspector = inspect(engine)

    actual_tables = set(
        inspector.get_table_names()
    )

    return REQUIRED_TABLES.issubset(actual_tables)


def check_row_counts():

    with engine.connect() as connection:

        for table_name, expected_count in EXPECTED_ROW_COUNTS.items():

            result = connection.execute(
                text(
                    f"SELECT COUNT(*) FROM {table_name}"
                )
            )

            actual_count = result.scalar()

            if actual_count != expected_count:
                return False

    return True


def check_foreign_keys():

    with engine.connect() as connection:

        result = connection.execute(
            text("PRAGMA foreign_key_check")
        )

        violations = result.fetchall()

    return len(violations) == 0


def check_orphan_records():

    checks = [

        """
        SELECT COUNT(*)
        FROM orders o
        LEFT JOIN customers c
            ON o.customer_id = c.customer_id
        WHERE c.customer_id IS NULL
        """,

        """
        SELECT COUNT(*)
        FROM order_items oi
        LEFT JOIN orders o
            ON oi.order_id = o.order_id
        WHERE o.order_id IS NULL
        """,

        """
        SELECT COUNT(*)
        FROM order_items oi
        LEFT JOIN products p
            ON oi.product_id = p.product_id
        WHERE p.product_id IS NULL
        """,

        """
        SELECT COUNT(*)
        FROM order_items oi
        LEFT JOIN sellers s
            ON oi.seller_id = s.seller_id
        WHERE s.seller_id IS NULL
        """,

        """
        SELECT COUNT(*)
        FROM payments p
        LEFT JOIN orders o
            ON p.order_id = o.order_id
        WHERE o.order_id IS NULL
        """,

        """
        SELECT COUNT(*)
        FROM reviews r
        LEFT JOIN orders o
            ON r.order_id = o.order_id
        WHERE o.order_id IS NULL
        """
    ]

    with engine.connect() as connection:

        for query in checks:

            result = connection.execute(
                text(query)
            )

            orphan_count = result.scalar()

            if orphan_count != 0:
                return False

    return True


def check_indexes():

    inspector = inspect(engine)

    for table_name, required_indexes in REQUIRED_INDEXES.items():

        actual_indexes = {
            index["name"]
            for index in inspector.get_indexes(table_name)
        }

        if not required_indexes.issubset(actual_indexes):
            return False

    return True


def check_metadata():

    with engine.connect() as connection:

        result = connection.execute(
            text(
                """
                SELECT COUNT(*)
                FROM dataset_metadata
                """
            )
        )

        metadata_count = result.scalar()

    return metadata_count == len(EXPECTED_ROW_COUNTS)


def run_health_check():

    print()
    print("=" * 60)
    print("OLIST DATABASE HEALTH REPORT")
    print("=" * 60)

    checks = {
        "Database Connection": check_connection(),
        "Required Tables": check_tables(),
        "Row Counts": check_row_counts(),
        "Foreign Keys": check_foreign_keys(),
        "Orphan Records": check_orphan_records(),
        "Indexes": check_indexes(),
        "Metadata": check_metadata(),
    }

    print()

    for check_name, passed in checks.items():

        status = "PASS" if passed else "FAIL"

        print(
            f"{status:<6} | {check_name}"
        )

    print()
    print("=" * 60)

    database_is_healthy = all(
        checks.values()
    )

    if database_is_healthy:

        print("Overall Status: HEALTHY")

    else:

        print("Overall Status: UNHEALTHY")

    print("=" * 60)

    return database_is_healthy


if __name__ == "__main__":

    run_health_check()