from unittest.mock import MagicMock, patch

import pytest

from app.pipeline.query_pipeline import QueryPipeline


ORDERS_SQL = """
SELECT COUNT(*) AS order_count
FROM orders
WHERE order_purchase_timestamp >= '2018-01-01'
  AND order_purchase_timestamp < '2019-01-01'
"""


REVIEW_SQL = """
SELECT AVG(review_score) AS average_review_score
FROM reviews
"""


PAYMENT_SQL = """
SELECT payment_type, COUNT(*) AS payment_count
FROM payments
GROUP BY payment_type
ORDER BY payment_count DESC
LIMIT 1
"""


def mock_generator(question: str):
    """Return deterministic SQL without calling Groq."""

    generator = MagicMock()

    question_lower = question.lower()

    if "average review" in question_lower:
        sql = REVIEW_SQL

    elif "payment type" in question_lower:
        sql = PAYMENT_SQL

    else:
        sql = ORDERS_SQL

    generator.generate.return_value = sql

    return generator


@pytest.fixture
def pipeline():
    """
    Create QueryPipeline with the LLM components mocked.

    Database execution, validation, formatting, and visualization
    remain real.
    """

    with patch(
        "app.pipeline.query_pipeline.SQLGenerator"
    ) as mock_generator_class, patch(
        "app.pipeline.query_pipeline.SQLCorrector"
    ) as mock_corrector_class:

        mock_generator_instance = MagicMock()

        def generate(question):
            question_lower = question.lower()

            if "average review" in question_lower:
                return REVIEW_SQL

            if "payment type" in question_lower:
                return PAYMENT_SQL

            return ORDERS_SQL

        mock_generator_instance.generate.side_effect = generate

        mock_generator_class.return_value = (
            mock_generator_instance
        )

        mock_corrector_instance = MagicMock()

        mock_corrector_instance.correct.return_value = ORDERS_SQL

        mock_corrector_class.return_value = (
            mock_corrector_instance
        )

        yield QueryPipeline()


def test_query_pipeline_orders_2018(pipeline):

    result = pipeline.run(
        "How many orders were placed in 2018?"
    )

    assert result["success"] is True

    assert isinstance(result["sql"], str)
    assert result["sql"].strip() != ""

    assert isinstance(result["rows"], list)
    assert result["row_count"] >= 0

    assert "formatted_result" in result
    assert "summary" in result
    assert "chart_data" in result
    assert "visualization" in result

    assert isinstance(
        result["execution_time_ms"],
        (int, float),
    )


def test_query_pipeline_average_review_score(pipeline):

    result = pipeline.run(
        "What is the average review score?"
    )

    assert result["success"] is True

    assert isinstance(result["sql"], str)
    assert result["sql"].strip() != ""

    assert isinstance(result["rows"], list)
    assert result["row_count"] >= 0

    assert "reviews" in result["sql"].lower()


def test_query_pipeline_payment_type(pipeline):

    result = pipeline.run(
        "Which payment type was used most often?"
    )

    assert result["success"] is True

    assert isinstance(result["sql"], str)
    assert result["sql"].strip() != ""

    assert isinstance(result["rows"], list)
    assert result["row_count"] >= 0

    assert "payment" in result["sql"].lower()


def test_query_pipeline_returns_complete_response(pipeline):

    result = pipeline.run(
        "How many orders were placed in 2018?"
    )

    assert result["success"] is True

    expected_keys = {
        "success",
        "sql",
        "rows",
        "row_count",
        "execution_time_ms",
        "formatted_result",
        "summary",
        "chart_data",
        "visualization",
    }

    assert expected_keys.issubset(
        result.keys()
    )