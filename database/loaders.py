"""
loaders.py

Contains reusable functions for loading Olist CSV files
into the SQLite database.
"""

import time
from datetime import datetime

import pandas as pd
from sqlalchemy import text

from app.database.database import engine
from app.utils.logger import get_logger


logger = get_logger(__name__)


def load_csv_to_table(
    file_path,
    table_name,
    parse_dates=None,
    remove_duplicates=False
):
    """
    Load a CSV file into an existing SQLite table.

    Parameters
    ----------
    file_path:
        Location of the CSV file.

    table_name:
        Destination database table.

    parse_dates:
        Columns that should be converted to datetime.

    remove_duplicates:
        Whether exact duplicate rows should be removed.
    """

    start_time = time.time()

    logger.info(f"Loading {table_name}...")

    dataframe = pd.read_csv(
        file_path,
        parse_dates=parse_dates
    )

    original_row_count = len(dataframe)

    if remove_duplicates:

        dataframe = dataframe.drop_duplicates()

        removed_rows = original_row_count - len(dataframe)

        if removed_rows > 0:
            logger.info(
                f"Removed {removed_rows:,} duplicate rows "
                f"from {table_name}."
            )

    dataframe.to_sql(
        name=table_name,
        con=engine,
        if_exists="append",
        index=False,
        chunksize=5000
    )

    row_count = len(dataframe)

    loading_time = time.time() - start_time

    logger.info(
        f"Loaded {row_count:,} rows into {table_name} "
        f"in {loading_time:.2f} seconds."
    )

    return row_count


def update_metadata(table_name, row_count):
    """
    Store the row count and load timestamp for a table.
    """

    loaded_at = datetime.now().isoformat(timespec="seconds")

    with engine.begin() as connection:

        connection.execute(
            text(
                """
                INSERT OR REPLACE INTO dataset_metadata
                (
                    table_name,
                    total_rows,
                    loaded_at
                )
                VALUES
                (
                    :table_name,
                    :total_rows,
                    :loaded_at
                )
                """
            ),
            {
                "table_name": table_name,
                "total_rows": row_count,
                "loaded_at": loaded_at
            }
        )