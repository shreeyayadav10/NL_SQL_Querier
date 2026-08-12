"""
inspect_dataset.py

Reads every CSV file and displays basic information.

This helps us understand the dataset before loading it into SQLite.
"""

import pandas as pd

from app.database.config import *

from app.utils.logger import get_logger

logger = get_logger(__name__)

datasets = {
    "Customers": CUSTOMERS_FILE,
    "Orders": ORDERS_FILE,
    "Order Items": ORDER_ITEMS_FILE,
    "Payments": PAYMENTS_FILE,
    "Reviews": REVIEWS_FILE,
    "Products": PRODUCTS_FILE,
    "Sellers": SELLERS_FILE,
    "Geolocation": GEOLOCATION_FILE,
    "Category Translation": CATEGORY_TRANSLATION_FILE,
}

print("=" * 80)
print("OLIST DATASET INSPECTION")
print("=" * 80)

for dataset_name, file_path in datasets.items():

    logger.info(f"Reading {dataset_name}")

    dataframe = pd.read_csv(file_path)

    print(f"\nDataset : {dataset_name}")

    print("-" * 60)

    print(f"Rows : {dataframe.shape[0]}")

    print(f"Columns : {dataframe.shape[1]}")

    print("\nColumn Names")

    for column in dataframe.columns:
        print(f"   • {column}")

    print("\nMissing Values")

    print(dataframe.isnull().sum())

    print("\nDuplicate Rows")

    print(dataframe.duplicated().sum())

print("\nInspection Completed Successfully.")