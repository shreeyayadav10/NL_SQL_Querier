"""
database.py

Creates and manages the SQLite database connection.
"""

from sqlalchemy import create_engine, event

from app.database.config import DATABASE_PATH


DATABASE_URL = f"sqlite:///{DATABASE_PATH}"


engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True
)


@event.listens_for(engine, "connect")
def enable_sqlite_foreign_keys(dbapi_connection, connection_record):
    """
    Enable foreign key enforcement for every SQLite connection.

    SQLite does not automatically enforce foreign keys unless this
    setting is enabled for each connection.
    """

    cursor = dbapi_connection.cursor()

    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.close()