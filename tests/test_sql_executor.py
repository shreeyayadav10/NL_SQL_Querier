from pathlib import Path

from app.execution.sql_executor import SQLExecutor


def test_sql_executor_count_orders_2018():
    database_path = Path("data/sqlite/olist.db")

    executor = SQLExecutor(database_path)

    sql = """
    SELECT COUNT(*) AS order_count
    FROM orders
    WHERE order_purchase_timestamp >= '2018-01-01'
      AND order_purchase_timestamp < '2019-01-01';
    """

    result = executor.execute(sql)

    assert result.success is True
    assert result.error is None

    assert "order_count" in result.columns
    assert result.row_count == 1

    assert len(result.rows) == 1
    assert result.rows[0]["order_count"] > 0

    assert result.execution_time_ms >= 0
