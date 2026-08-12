from app.validation.sql_validator import SQLValidator


def test_valid_select():
    validator = SQLValidator()

    sql = """
    SELECT COUNT(*) AS order_count
    FROM orders
    WHERE order_purchase_timestamp >= '2018-01-01'
      AND order_purchase_timestamp < '2019-01-01';
    """

    result = validator.validate(sql)

    assert result.is_valid is True


def test_valid_join():
    validator = SQLValidator()

    sql = """
    SELECT
        c.customer_state,
        COUNT(o.order_id) AS order_count
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    GROUP BY c.customer_state
    ORDER BY order_count DESC;
    """

    result = validator.validate(sql)

    assert result.is_valid is True


def test_delete_is_rejected():
    validator = SQLValidator()

    result = validator.validate("""
        DELETE FROM orders;
    """)

    assert result.is_valid is False


def test_drop_is_rejected():
    validator = SQLValidator()

    result = validator.validate("""
        DROP TABLE orders;
    """)

    assert result.is_valid is False


def test_unknown_table_is_rejected():
    validator = SQLValidator()

    result = validator.validate("""
        SELECT *
        FROM employee_salary;
    """)

    assert result.is_valid is False


def test_multiple_statements_are_rejected():
    validator = SQLValidator()

    result = validator.validate("""
        SELECT COUNT(*) FROM orders;

        SELECT COUNT(*) FROM customers;
    """)

    assert result.is_valid is False
