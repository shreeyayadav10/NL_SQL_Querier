"""
load_data.py

Loads all Olist CSV files into the SQLite database.
"""

from app.database.config import (
    CUSTOMERS_FILE,
    ORDERS_FILE,
    ORDER_ITEMS_FILE,
    PAYMENTS_FILE,
    REVIEWS_FILE,
    PRODUCTS_FILE,
    SELLERS_FILE,
    GEOLOCATION_FILE,
    CATEGORY_TRANSLATION_FILE,
)

from app.database.loaders import (
    load_csv_to_table,
    update_metadata,
)

from app.utils.logger import get_logger


logger = get_logger(__name__)


def load_all_data():

    logger.info("Starting Olist data loading process.")

    # ---------------------------------------------------------
    # 1. Customers
    # ---------------------------------------------------------

    customers_count = load_csv_to_table(
        file_path=CUSTOMERS_FILE,
        table_name="customers"
    )

    update_metadata(
        "customers",
        customers_count
    )

    # ---------------------------------------------------------
    # 2. Orders
    # ---------------------------------------------------------

    orders_count = load_csv_to_table(
        file_path=ORDERS_FILE,
        table_name="orders",
        parse_dates=[
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ]
    )

    update_metadata(
        "orders",
        orders_count
    )

    # ---------------------------------------------------------
    # 3. Products
    # ---------------------------------------------------------

    products_count = load_csv_to_table(
        file_path=PRODUCTS_FILE,
        table_name="products"
    )

    update_metadata(
        "products",
        products_count
    )

    # ---------------------------------------------------------
    # 4. Sellers
    # ---------------------------------------------------------

    sellers_count = load_csv_to_table(
        file_path=SELLERS_FILE,
        table_name="sellers"
    )

    update_metadata(
        "sellers",
        sellers_count
    )

    # ---------------------------------------------------------
    # 5. Order Items
    # ---------------------------------------------------------

    order_items_count = load_csv_to_table(
        file_path=ORDER_ITEMS_FILE,
        table_name="order_items",
        parse_dates=[
            "shipping_limit_date"
        ]
    )

    update_metadata(
        "order_items",
        order_items_count
    )

    # ---------------------------------------------------------
    # 6. Payments
    # ---------------------------------------------------------

    payments_count = load_csv_to_table(
        file_path=PAYMENTS_FILE,
        table_name="payments"
    )

    update_metadata(
        "payments",
        payments_count
    )

    # ---------------------------------------------------------
    # 7. Reviews
    # ---------------------------------------------------------

    reviews_count = load_csv_to_table(
        file_path=REVIEWS_FILE,
        table_name="reviews",
        parse_dates=[
            "review_creation_date",
            "review_answer_timestamp"
        ]
    )

    update_metadata(
        "reviews",
        reviews_count
    )

    # ---------------------------------------------------------
    # 8. Geolocation
    # ---------------------------------------------------------

    geolocation_count = load_csv_to_table(
        file_path=GEOLOCATION_FILE,
        table_name="geolocation",
        remove_duplicates=True
    )

    update_metadata(
        "geolocation",
        geolocation_count
    )

    # ---------------------------------------------------------
    # 9. Category Translation
    # ---------------------------------------------------------

    translation_count = load_csv_to_table(
        file_path=CATEGORY_TRANSLATION_FILE,
        table_name="category_translation"
    )

    update_metadata(
        "category_translation",
        translation_count
    )

    logger.info(
        "Olist data loading completed successfully."
    )


if __name__ == "__main__":
    load_all_data()