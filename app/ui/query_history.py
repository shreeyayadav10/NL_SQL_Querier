"""
query_history.py

Stores recent NL-to-SQL queries during the application session.
"""

from datetime import datetime
from typing import Any


class QueryHistory:
    """Manage recent query executions."""

    def __init__(self, max_items: int = 50) -> None:
        self.max_items = max_items
        self._history: list[dict[str, Any]] = []

    def add(
        self,
        question: str,
        sql: str,
        result: dict[str, Any],
        visualization: dict[str, Any],
    ) -> None:
        """Add a completed query to history."""

        item = {
            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "question": question,
            "sql": sql,
            "result": result,
            "visualization": visualization,
        }

        self._history.insert(0, item)

        if len(self._history) > self.max_items:
            self._history = self._history[:self.max_items]

    def get_all(self) -> list[dict[str, Any]]:
        """Return all stored queries."""

        return self._history.copy()

    def clear(self) -> None:
        """Clear query history."""

        self._history.clear()

    def count(self) -> int:
        """Return number of stored queries."""

        return len(self._history)