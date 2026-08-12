from unittest.mock import MagicMock, patch

from app.llm.sql_generator import SQLGenerator


SCHEMA = """
TABLE: orders

COLUMNS:

- order_id: TEXT [PRIMARY KEY]
- customer_id: TEXT
- order_status: TEXT
- order_purchase_timestamp: TEXT
- order_approved_at: TEXT
- order_delivered_carrier_date: TEXT
- order_delivered_customer_date: TEXT
- order_estimated_delivery_date: TEXT

RELATIONSHIPS:

- customer_id -> customers.customer_id

TABLE: customers

COLUMNS:

- customer_id: TEXT [PRIMARY KEY]
- customer_unique_id: TEXT
- customer_zip_code_prefix: INTEGER
- customer_city: TEXT
- customer_state: TEXT

TABLE: order_items

COLUMNS:

- order_id: TEXT
- order_item_id: INTEGER
- product_id: TEXT
- seller_id: TEXT
- shipping_limit_date: TEXT
- price: REAL
- freight_value: REAL

RELATIONSHIPS:

- order_id -> orders.order_id
- product_id -> products.product_id
- seller_id -> sellers.seller_id
"""


def create_generator():
    generator = SQLGenerator(schema=SCHEMA)

    fake_response = MagicMock()

    fake_response.choices[0].message.content = """
SELECT COUNT(*) AS order_count
FROM orders
WHERE order_purchase_timestamp >= '2018-01-01'
  AND order_purchase_timestamp < '2019-01-01'
"""

    return generator, fake_response


def test_sql_generator_returns_sql():

    generator, fake_response = create_generator()

    with patch.object(
        generator.client.chat.completions,
        "create",
        return_value=fake_response,
    ):

        question = "How many orders were placed in 2018?"

        sql = generator.generate(question)

    assert sql is not None
    assert isinstance(sql, str)
    assert sql.strip() != ""


def test_sql_generator_generates_select_query():

    generator, fake_response = create_generator()

    with patch.object(
        generator.client.chat.completions,
        "create",
        return_value=fake_response,
    ):

        question = "How many orders were placed in 2018?"

        sql = generator.generate(question)

    normalized_sql = sql.strip().lower()

    assert normalized_sql.startswith("select")
    assert "orders" in normalized_sql


def test_sql_generator_uses_order_purchase_timestamp():

    generator, fake_response = create_generator()

    with patch.object(
        generator.client.chat.completions,
        "create",
        return_value=fake_response,
    ):

        question = "How many orders were placed in 2018?"

        sql = generator.generate(question)

    normalized_sql = sql.lower()

    assert "order_purchase_timestamp" in normalized_sql


def test_sql_generator_does_not_generate_dangerous_sql():

    generator, fake_response = create_generator()

    with patch.object(
        generator.client.chat.completions,
        "create",
        return_value=fake_response,
    ):

        question = "How many orders were placed in 2018?"

        sql = generator.generate(question)

    normalized_sql = sql.strip().lower()

    assert not normalized_sql.startswith("delete")
    assert not normalized_sql.startswith("drop")
    assert not normalized_sql.startswith("update")
    assert not normalized_sql.startswith("insert")
    assert not normalized_sql.startswith("alter")