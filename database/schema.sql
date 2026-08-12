-- ==========================================================
-- OLIST DATABASE SCHEMA
-- ==========================================================

PRAGMA foreign_keys = ON;

-------------------------------------------------------------
-- CUSTOMERS
-------------------------------------------------------------
CREATE TABLE IF NOT EXISTS customers (

    customer_id TEXT PRIMARY KEY,

    customer_unique_id TEXT NOT NULL,

    customer_zip_code_prefix INTEGER,

    customer_city TEXT,

    customer_state TEXT

);

-------------------------------------------------------------
-- ORDERS
-------------------------------------------------------------
CREATE TABLE IF NOT EXISTS orders (

    order_id TEXT PRIMARY KEY,

    customer_id TEXT NOT NULL,

    order_status TEXT,

    order_purchase_timestamp TEXT,

    order_approved_at TEXT,

    order_delivered_carrier_date TEXT,

    order_delivered_customer_date TEXT,

    order_estimated_delivery_date TEXT,

    FOREIGN KEY(customer_id)
        REFERENCES customers(customer_id)

);

-------------------------------------------------------------
-- PRODUCTS
-------------------------------------------------------------
CREATE TABLE IF NOT EXISTS products (

    product_id TEXT PRIMARY KEY,

    product_category_name TEXT,

    product_name_lenght REAL,

    product_description_lenght REAL,

    product_photos_qty REAL,

    product_weight_g REAL,

    product_length_cm REAL,

    product_height_cm REAL,

    product_width_cm REAL

);

-------------------------------------------------------------
-- SELLERS
-------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sellers (

    seller_id TEXT PRIMARY KEY,

    seller_zip_code_prefix INTEGER,

    seller_city TEXT,

    seller_state TEXT

);

-------------------------------------------------------------
-- ORDER ITEMS
-------------------------------------------------------------
CREATE TABLE IF NOT EXISTS order_items (

    order_id TEXT,

    order_item_id INTEGER,

    product_id TEXT,

    seller_id TEXT,

    shipping_limit_date TEXT,

    price REAL,

    freight_value REAL,

    PRIMARY KEY(order_id, order_item_id),

    FOREIGN KEY(order_id)
        REFERENCES orders(order_id),

    FOREIGN KEY(product_id)
        REFERENCES products(product_id),

    FOREIGN KEY(seller_id)
        REFERENCES sellers(seller_id)

);

-------------------------------------------------------------
-- PAYMENTS
-------------------------------------------------------------
CREATE TABLE IF NOT EXISTS payments (

    order_id TEXT,

    payment_sequential INTEGER,

    payment_type TEXT,

    payment_installments INTEGER,

    payment_value REAL,

    PRIMARY KEY(order_id, payment_sequential),

    FOREIGN KEY(order_id)
        REFERENCES orders(order_id)

);

-------------------------------------------------------------
-- REVIEWS
-------------------------------------------------------------
CREATE TABLE IF NOT EXISTS reviews (

    review_id TEXT,

    order_id TEXT,

    review_score INTEGER,

    review_comment_title TEXT,

    review_comment_message TEXT,

    review_creation_date TEXT,

    review_answer_timestamp TEXT,

    PRIMARY KEY(review_id, order_id),

    FOREIGN KEY(order_id)
        REFERENCES orders(order_id)

);

-------------------------------------------------------------
-- GEOLOCATION
-------------------------------------------------------------
CREATE TABLE IF NOT EXISTS geolocation (

    geolocation_zip_code_prefix INTEGER,

    geolocation_lat REAL,

    geolocation_lng REAL,

    geolocation_city TEXT,

    geolocation_state TEXT

);

-------------------------------------------------------------
-- CATEGORY TRANSLATION
-------------------------------------------------------------
CREATE TABLE IF NOT EXISTS category_translation (

    product_category_name TEXT PRIMARY KEY,

    product_category_name_english TEXT

);

-------------------------------------------------------------
-- DATASET METADATA
-------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dataset_metadata (

    table_name TEXT PRIMARY KEY,

    total_rows INTEGER,

    loaded_at TEXT

);