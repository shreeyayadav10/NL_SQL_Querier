"""
config.py

This file stores all project paths and database configuration.
Keeping paths in one place makes the project easier to maintain.
"""

from pathlib import Path

# -----------------------------
# Project Root Directory
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# -----------------------------
# Data Directories
# -----------------------------
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

DATABASE_DIR = PROJECT_ROOT / "data" / "sqlite"

# -----------------------------
# Database File
# -----------------------------
DATABASE_PATH = DATABASE_DIR / "olist.db"

# -----------------------------
# Dataset Files
# -----------------------------
CUSTOMERS_FILE = RAW_DATA_DIR / "olist_customers_dataset.csv"

ORDERS_FILE = RAW_DATA_DIR / "olist_orders_dataset.csv"

ORDER_ITEMS_FILE = RAW_DATA_DIR / "olist_order_items_dataset.csv"

PAYMENTS_FILE = RAW_DATA_DIR / "olist_order_payments_dataset.csv"

REVIEWS_FILE = RAW_DATA_DIR / "olist_order_reviews_dataset.csv"

PRODUCTS_FILE = RAW_DATA_DIR / "olist_products_dataset.csv"

SELLERS_FILE = RAW_DATA_DIR / "olist_sellers_dataset.csv"

GEOLOCATION_FILE = RAW_DATA_DIR / "olist_geolocation_dataset.csv"

CATEGORY_TRANSLATION_FILE = (
    RAW_DATA_DIR / "product_category_name_translation.csv"
)