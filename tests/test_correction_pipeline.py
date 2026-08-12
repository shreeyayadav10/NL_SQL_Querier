from unittest.mock import MagicMock, patch

from app.pipeline.query_pipeline import QueryPipeline


CORRECTED_SQL = """
SELECT COUNT(*) AS order_count
FROM orders
WHERE order_purchase_timestamp >= '2018-01-01'
  AND order_purchase_timestamp < '2019-01-01'
"""


def create_pipeline():
    """
    Create QueryPipeline with the LLM corrector mocked.

    SQL validation and SQLite execution remain real.
    """

    with patch(
        "app.pipeline.query_pipeline.SQLGenerator"
    ) as mock_generator_class, patch(
        "app.pipeline.query_pipeline.SQLCorrector"
    ) as mock_corrector_class:

        generator = MagicMock()

        generator.generate.return_value = CORRECTED_SQL

        mock_generator_class.return_value = generator

        corrector = MagicMock()

        corrector.correct.return_value = CORRECTED_SQL

        mock_corrector_class.return_value = corrector

        pipeline = QueryPipeline()

        return pipeline


def test_correction_pipeline_fixes_invalid_table():

    pipeline = create_pipeline()

    question = "How many orders were placed in 2018?"

    broken_sql = """
    SELECT COUNT(*) AS order_count
    FROM order_table
    WHERE order_purchase_timestamp >= '2018-01-01'
      AND order_purchase_timestamp < '2019-01-01'
    """

    error_message = (
        "Query references unknown table(s): order_table"
    )

    corrected_sql = pipeline.sql_corrector.correct(
        question=question,
        failed_sql=broken_sql,
        error_message=error_message,
    )

    assert corrected_sql is not None
    assert isinstance(corrected_sql, str)
    assert corrected_sql.strip() != ""

    assert "order_table" not in corrected_sql.lower()
    assert "orders" in corrected_sql.lower()


def test_correction_pipeline_validates_corrected_sql():

    pipeline = create_pipeline()

    question = "How many orders were placed in 2018?"

    broken_sql = """
    SELECT COUNT(*) AS order_count
    FROM order_table
    WHERE order_purchase_timestamp >= '2018-01-01'
      AND order_purchase_timestamp < '2019-01-01'
    """

    error_message = (
        "Query references unknown table(s): order_table"
    )

    corrected_sql = pipeline.sql_corrector.correct(
        question=question,
        failed_sql=broken_sql,
        error_message=error_message,
    )

    validation = pipeline.validator.validate(
        corrected_sql
    )

    assert validation.is_valid is True
    assert validation.sql is not None
    assert validation.sql.strip() != ""


def test_correction_pipeline_executes_corrected_sql():

    pipeline = create_pipeline()

    question = "How many orders were placed in 2018?"

    broken_sql = """
    SELECT COUNT(*) AS order_count
    FROM order_table
    WHERE order_purchase_timestamp >= '2018-01-01'
      AND order_purchase_timestamp < '2019-01-01'
    """

    error_message = (
        "Query references unknown table(s): order_table"
    )

    corrected_sql = pipeline.sql_corrector.correct(
        question=question,
        failed_sql=broken_sql,
        error_message=error_message,
    )

    validation = pipeline.validator.validate(
        corrected_sql
    )

    assert validation.is_valid is True

    result = pipeline.executor.execute(
        validation.sql
    )

    assert result.success is True
    assert result.row_count == 1
    assert result.columns
    assert result.rows


def test_correction_pipeline_returns_numeric_order_count():

    pipeline = create_pipeline()

    question = "How many orders were placed in 2018?"

    broken_sql = """
    SELECT COUNT(*) AS order_count
    FROM order_table
    WHERE order_purchase_timestamp >= '2018-01-01'
      AND order_purchase_timestamp < '2019-01-01'
    """

    error_message = (
        "Query references unknown table(s): order_table"
    )

    corrected_sql = pipeline.sql_corrector.correct(
        question=question,
        failed_sql=broken_sql,
        error_message=error_message,
    )

    validation = pipeline.validator.validate(
        corrected_sql
    )

    assert validation.is_valid is True

    result = pipeline.executor.execute(
        validation.sql
    )

    assert result.success is True
    assert result.rows

    order_count = result.rows[0]["order_count"]

    assert isinstance(
        order_count,
        (int, float),
    )

    assert order_count > 0