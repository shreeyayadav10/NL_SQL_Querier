"""
create_database.py

Creates the SQLite database and all tables defined
in schema.sql.
"""

from pathlib import Path
from sqlalchemy import text

from app.database.database import engine
from app.utils.logger import get_logger

logger = get_logger(__name__)


def create_database():

    schema_file = (
        Path(__file__).parent / "schema.sql"
    )

    with open(schema_file, "r", encoding="utf-8") as file:
        schema_sql = file.read()

    with engine.begin() as connection:

        for statement in schema_sql.split(";"):

            statement = statement.strip()

            if statement:
                connection.execute(text(statement))

    logger.info("Database created successfully.")


if __name__ == "__main__":

    create_database()