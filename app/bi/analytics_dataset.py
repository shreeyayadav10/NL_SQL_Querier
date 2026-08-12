"""
analytics_dataset.py

Builds a Power BI-ready analytical dataset from the Olist SQLite database.
"""

from pathlib import Path
import sqlite3

import pandas as pd


class AnalyticsDatasetBuilder:
    """Build a denormalized analytical dataset for BI tools."""

    def __init__(
        self,
        database_path: str | Path = "data/sqlite/olist.db",
    ) -> None:
        self.database_path = Path(database_path)

    def build(self) -> pd.DataFrame:
        """Load and join the core Olist tables."""

        if not self.database_path.exists():
            raise FileNotFoundError(
                f"SQLite database not found: {self.database_path}"
            )

        query = """
        SELECT
            o.order_id,
            o.customer_id,
            c.customer_unique_id,
            c.customer_state,
            c.customer_city,

            o.order_status,
            o.order_purchase_timestamp,
            o.order_approved_at,
            o.order_delivered_customer_date,
            o.order_estimated_delivery_date,

            oi.order_item_id,
            oi.product_id,
            oi.seller_id,
            oi.price,
            oi.freight_value,

            p.product_category_name,

            pay.payment_type,
            pay.payment_installments,
            pay.payment_value,

            r.review_score

        FROM orders o

        LEFT JOIN customers c
            ON o.customer_id = c.customer_id

        LEFT JOIN order_items oi
            ON o.order_id = oi.order_id

        LEFT JOIN products p
            ON oi.product_id = p.product_id

        LEFT JOIN payments pay
            ON o.order_id = pay.order_id

        LEFT JOIN reviews r
            ON o.order_id = r.order_id
        """

        with sqlite3.connect(self.database_path) as connection:
            dataframe = pd.read_sql_query(
                query,
                connection,
            )

        return self._clean(dataframe)

    @staticmethod
    def _clean(dataframe: pd.DataFrame) -> pd.DataFrame:
        """Clean and prepare the dataset for Power BI."""

        dataframe = dataframe.copy()

        # Normalize column names.
        dataframe.columns = [
            str(column)
            .strip()
            .lower()
            .replace(" ", "_")
            .replace("-", "_")
            for column in dataframe.columns
        ]

        # Convert date columns.
        date_columns = [
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ]

        for column in date_columns:
            if column in dataframe.columns:
                dataframe[column] = pd.to_datetime(
                    dataframe[column],
                    errors="coerce",
                )

        # Create a simple purchase date for Power BI.
        if "order_purchase_timestamp" in dataframe.columns:
            dataframe["purchase_date"] = (
                dataframe["order_purchase_timestamp"]
                .dt.date
            )

        # Create purchase year/month fields.
        if "order_purchase_timestamp" in dataframe.columns:
            dataframe["purchase_year"] = (
                dataframe["order_purchase_timestamp"]
                .dt.year
            )

            dataframe["purchase_month"] = (
                dataframe["order_purchase_timestamp"]
                .dt.month
            )

            dataframe["purchase_month_name"] = (
                dataframe["order_purchase_timestamp"]
                .dt.strftime("%b")
            )

        # Clean category names.
        if "product_category_name" in dataframe.columns:
            dataframe["product_category_name"] = (
                dataframe["product_category_name"]
                .fillna("Unknown")
                .astype(str)
                .str.replace("_", " ", regex=False)
                .str.title()
            )

        # Numeric columns.
        numeric_columns = [
            "price",
            "freight_value",
            "payment_value",
            "payment_installments",
            "review_score",
        ]

        for column in numeric_columns:
            if column in dataframe.columns:
                dataframe[column] = pd.to_numeric(
                    dataframe[column],
                    errors="coerce",
                )

        return dataframe

    def export_csv(
        self,
        output_path: str | Path = "exports/bi/olist_analytics.csv",
    ) -> Path:
        """Build and export the analytical dataset."""

        output_path = Path(output_path)
        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        dataframe = self.build()

        dataframe.to_csv(
            output_path,
            index=False,
        )

        return output_path


def main() -> None:
    """Generate the Power BI dataset."""

    builder = AnalyticsDatasetBuilder()

    dataframe = builder.build()

    output_path = builder.export_csv()

    print("=" * 60)
    print("POWER BI ANALYTICS DATASET")
    print("=" * 60)
    print(f"Rows: {len(dataframe):,}")
    print(f"Columns: {len(dataframe.columns)}")
    print(f"Output: {output_path}")
    print()
    print("Columns:")
    
    for column in dataframe.columns:
        print(f"  - {column}")

    print("=" * 60)


if __name__ == "__main__":
    main()