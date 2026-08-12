"""
schema_inspector.py

Extracts metadata from the SQLite database that will later
be supplied to the LLM for NL-to-SQL generation.

Information extracted:
- Tables
- Columns
- Data Types
- Primary Keys
- Foreign Keys
- Representative Sample Values
"""

from pathlib import Path
from typing import Any

from sqlalchemy import create_engine, inspect, text


class SchemaInspector:
    """
    Reads the SQLite database schema and returns
    structured metadata for the LLM.
    """

    # Tables that should not be exposed to the LLM.
    IGNORED_TABLES = {
        "dataset_metadata",
    }

    # Columns where sample values are generally not useful.
    SAMPLE_SKIP_KEYWORDS = (
        "id",
        "timestamp",
        "date",
        "message",
        "comment",
        "description",
    )

    def __init__(self) -> None:

        database_path = (
            Path(__file__).resolve()
            .parents[2]
            / "data"
            / "sqlite"
            / "olist.db"
        )

        if not database_path.exists():
            raise FileNotFoundError(
                f"Database not found: {database_path}"
            )

        database_url = (
            f"sqlite:///{database_path}"
        )

        self.engine = create_engine(
            database_url
        )

        self.inspector = inspect(
            self.engine
        )

    def get_tables(self) -> list[str]:
        """
        Return all user-facing database tables.
        """

        tables = self.inspector.get_table_names()

        return sorted(
            [
                table
                for table in tables
                if table not in self.IGNORED_TABLES
            ]
        )

    def get_columns(
        self,
        table_name: str,
    ) -> list[dict[str, Any]]:
        """
        Return metadata for all columns
        in a table.
        """

        columns = self.inspector.get_columns(
            table_name
        )

        return [
            {
                "name": column["name"],
                "type": str(column["type"]),
                "nullable": column["nullable"],
            }
            for column in columns
        ]

    def get_primary_keys(
        self,
        table_name: str,
    ) -> list[str]:
        """
        Return primary-key columns.
        """

        primary_key = (
            self.inspector.get_pk_constraint(
                table_name
            )
        )

        return primary_key.get(
            "constrained_columns",
            [],
        )

    def get_foreign_keys(
        self,
        table_name: str,
    ) -> list[dict[str, Any]]:
        """
        Return foreign-key relationships.
        """

        foreign_keys = (
            self.inspector.get_foreign_keys(
                table_name
            )
        )

        relationships = []

        for foreign_key in foreign_keys:

            relationships.append(
                {
                    "columns": foreign_key[
                        "constrained_columns"
                    ],
                    "referred_table": foreign_key[
                        "referred_table"
                    ],
                    "referred_columns": foreign_key[
                        "referred_columns"
                    ],
                }
            )

        return relationships

    def should_collect_samples(
        self,
        column_name: str,
    ) -> bool:
        """
        Decide whether sample values are useful
        for a column.
        """

        column_name = column_name.lower()

        return not any(
            keyword in column_name
            for keyword in self.SAMPLE_SKIP_KEYWORDS
        )

    def get_sample_values(
        self,
        table_name: str,
        column_name: str,
        limit: int = 5,
    ) -> list[Any]:
        """
        Return representative sample values.
        """

        if not self.should_collect_samples(
            column_name
        ):
            return []

        query = text(
            f"""
            SELECT DISTINCT "{column_name}"
            FROM "{table_name}"
            WHERE "{column_name}" IS NOT NULL
            LIMIT :limit
            """
        )

        with self.engine.connect() as connection:

            result = connection.execute(
                query,
                {"limit": limit},
            )

            values = [
                row[0]
                for row in result.fetchall()
            ]

        return values

    def inspect_database(
        self,
    ) -> dict[str, Any]:
        """
        Build a structured representation
        of the database.
        """

        database_schema = {}

        for table_name in self.get_tables():

            columns = self.get_columns(
                table_name
            )

            for column in columns:

                column["sample_values"] = (
                    self.get_sample_values(
                        table_name,
                        column["name"],
                    )
                )

            database_schema[table_name] = {
                "columns": columns,
                "primary_keys": (
                    self.get_primary_keys(
                        table_name
                    )
                ),
                "foreign_keys": (
                    self.get_foreign_keys(
                        table_name
                    )
                ),
            }

        return database_schema


if __name__ == "__main__":

    inspector = SchemaInspector()

    schema = inspector.inspect_database()

    print(
        f"Tables found: {len(schema)}"
    )

    for table_name in schema:
        print(
            f" - {table_name}"
        )