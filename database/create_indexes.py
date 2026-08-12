"""
create_indexes.py

Creates indexes that improve the performance of common
joins, filters, and aggregations.
"""

from pathlib import Path

from sqlalchemy import text

from app.database.database import engine
from app.utils.logger import get_logger


logger = get_logger(__name__)


def create_indexes():

    index_file = Path(__file__).parent / "indexes.sql"

    with open(index_file, "r", encoding="utf-8") as file:
        index_sql = file.read()

    with engine.begin() as connection:

        for statement in index_sql.split(";"):

            statement = statement.strip()

            if statement:
                connection.execute(text(statement))

    logger.info("Database indexes created successfully.")


if __name__ == "__main__":
    create_indexes()