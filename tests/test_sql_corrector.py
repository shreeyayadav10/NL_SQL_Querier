from unittest.mock import MagicMock

from app.correction.sql_corrector import SQLCorrector


SCHEMA = """
TABLE: orders

COLUMNS:
- order_id: TEXT [PRIMARY KEY]
- customer_id: TEXT
- order_status: TEXT
- order_purchase_timestamp: TEXT

TABLE: customers

COLUMNS:
- customer_id: TEXT [PRIMARY KEY]
- customer_unique_id: TEXT
- customer_zip_code_prefix: INTEGER
- customer_city: TEXT
- customer_state: TEXT
"""


def create_corrector():
    corrector = SQLCorrector(schema=SCHEMA)

    fake_response = MagicMock()

    fake_response.choices[0].message.content = """
SELECT COUNT(*) AS order_count
FROM orders
WHERE order_purchase_timestamp >= '2018-01-01'
  AND order_purchase_timestamp < '2019-01-01'
"""

    corrector.client.chat.completions.create = MagicMock(
        return_value=fake_response
    )

    return corrector


def test_sql_corrector_returns_sql():
    corrector = create_corrector()

    corrected_sql = corrector.correct(
        question="How many orders were placed in 2018?",
        failed_sql="""
        SELECT COUNT(*)
        FROM order_table
        WHERE order_purchase_timestamp >= '2018-01-01'
        """,
        error_message="no such table: order_table",
    )

    assert corrected_sql is not None
    assert isinstance(corrected_sql, str)
    assert corrected_sql.strip() != ""


def test_sql_corrector_removes_invalid_table():
    corrector = create_corrector()

    corrected_sql = corrector.correct(
        question="How many orders were placed in 2018?",
        failed_sql="""
        SELECT COUNT(*)
        FROM order_table
        WHERE order_purchase_timestamp >= '2018-01-01'
        """,
        error_message="no such table: order_table",
    )

    normalized_sql = corrected_sql.lower()

    assert "order_table" not in normalized_sql
    assert "orders" in normalized_sql


def test_sql_corrector_generates_select_query():
    corrector = create_corrector()

    corrected_sql = corrector.correct(
        question="How many orders were placed in 2018?",
        failed_sql="""
        SELECT COUNT(*)
        FROM order_table
        WHERE order_purchase_timestamp >= '2018-01-01'
        """,
        error_message="no such table: order_table",
    )

    normalized_sql = corrected_sql.strip().lower()

    assert normalized_sql.startswith("select")


def test_sql_corrector_preserves_required_column():
    corrector = create_corrector()

    corrected_sql = corrector.correct(
        question="How many orders were placed in 2018?",
        failed_sql="""
        SELECT COUNT(*)
        FROM order_table
        WHERE order_purchase_timestamp >= '2018-01-01'
        """,
        error_message="no such table: order_table",
    )

    normalized_sql = corrected_sql.lower()

    assert "order_purchase_timestamp" in normalized_sql


def test_sql_corrector_does_not_generate_dangerous_sql():
    corrector = create_corrector()

    corrected_sql = corrector.correct(
        question="How many orders were placed in 2018?",
        failed_sql="""
        SELECT COUNT(*)
        FROM order_table
        WHERE order_purchase_timestamp >= '2018-01-01'
        """,
        error_message="no such table: order_table",
    )

    normalized_sql = corrected_sql.strip().lower()

    dangerous_commands = (
        "delete",
        "drop",
        "update",
        "insert",
        "alter",
        "create",
        "truncate",
        "attach",
        "pragma",
    )

    for command in dangerous_commands:
        assert not normalized_sql.startswith(command)


def test_sql_corrector_calls_llm():
    corrector = create_corrector()

    corrector.correct(
        question="How many orders were placed in 2018?",
        failed_sql="""
        SELECT COUNT(*)
        FROM order_table
        """,
        error_message="no such table: order_table",
    )

    corrector.client.chat.completions.create.assert_called_once()