"""
SQL execution layer.

This module executes validated, read-only SQL queries
against the Olist SQLite database.
"""

import sqlite3
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class QueryResult:
    """
    Stores the result of a database query.
    """

    success: bool
    columns: list[str] = field(default_factory=list)
    rows: list[dict[str, Any]] = field(default_factory=list)
    row_count: int = 0
    execution_time_ms: float = 0.0
    error: str | None = None


class SQLExecutor:
    """
    Executes validated SQL queries against SQLite.
    """

    def __init__(self, database_path: str | Path):
        self.database_path = Path(database_path)

    def execute(self, sql: str) -> QueryResult:
        """
        Execute a SQL query and return a structured result.
        """

        start_time = time.perf_counter()

        connection = None

        try:
            # -------------------------------------------------
            # Check that the database exists
            # -------------------------------------------------

            if not self.database_path.exists():
                return QueryResult(
                    success=False,
                    error=(
                        f"Database not found: "
                        f"{self.database_path}"
                    ),
                )

            # -------------------------------------------------
            # Connect to SQLite
            # -------------------------------------------------

            connection = sqlite3.connect(
                self.database_path
            )

            # Return rows as dictionaries.
            connection.row_factory = sqlite3.Row

            cursor = connection.cursor()

            # -------------------------------------------------
            # Execute query
            # -------------------------------------------------

            cursor.execute(sql)

            # -------------------------------------------------
            # Retrieve results
            # -------------------------------------------------

            rows = cursor.fetchall()

            columns = [
                description[0]
                for description in cursor.description
            ]

            formatted_rows = [
                dict(row)
                for row in rows
            ]

            execution_time = (
                time.perf_counter() - start_time
            ) * 1000

            return QueryResult(
                success=True,
                columns=columns,
                rows=formatted_rows,
                row_count=len(formatted_rows),
                execution_time_ms=round(
                    execution_time,
                    2,
                ),
            )

        except sqlite3.Error as exc:

            execution_time = (
                time.perf_counter() - start_time
            ) * 1000

            return QueryResult(
                success=False,
                execution_time_ms=round(
                    execution_time,
                    2,
                ),
                error=str(exc),
            )

        finally:

            if connection is not None:
                connection.close()


if __name__ == "__main__":
    print("SQL Executor module loaded successfully.")