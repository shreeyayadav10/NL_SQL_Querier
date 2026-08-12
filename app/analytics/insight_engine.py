"""
insight_engine.py

Generates concise business insights from structured SQL results.

This module is intentionally independent from Streamlit and SQL
execution. It analyzes already-executed results.
"""

from __future__ import annotations

from typing import Any


class InsightEngine:
    """
    Converts structured query results into business-oriented insights.
    """

    def generate(
        self,
        question: str,
        result: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Generate insights from a completed query result.
        """

        if not result.get("success", False):
            return {
                "available": False,
                "title": "Insight unavailable",
                "message": "The query did not complete successfully.",
                "insights": [],
            }

        rows = result.get("rows", [])
        columns = result.get("columns", [])

        if not rows:
            return {
                "available": False,
                "title": "No insight available",
                "message": "The query returned no records.",
                "insights": [],
            }

        if len(rows) == 1 and len(columns) == 1:
            return self._scalar_insight(
                columns[0],
                rows[0].get(columns[0]),
            )

        if len(columns) == 2:
            return self._two_column_insight(
                columns,
                rows,
            )

        return self._table_insight(
            columns,
            rows,
        )

    # ========================================================
    # SCALAR
    # ========================================================

    def _scalar_insight(
        self,
        column: str,
        value: Any,
    ) -> dict[str, Any]:

        label = self._pretty(column)

        formatted_value = self._format_value(value)

        return {
            "available": True,
            "title": "Key Result",
            "message": f"{label} is {formatted_value}.",
            "insights": [
                {
                    "type": "metric",
                    "label": label,
                    "value": formatted_value,
                }
            ],
        }

    # ========================================================
    # TWO COLUMN
    # ========================================================

    def _two_column_insight(
        self,
        columns: list[str],
        rows: list[dict[str, Any]],
    ) -> dict[str, Any]:

        x_column = columns[0]
        y_column = columns[1]

        numeric_rows = []

        for row in rows:

            value = row.get(y_column)

            if isinstance(value, (int, float)):

                numeric_rows.append(
                    (
                        row.get(x_column),
                        value,
                    )
                )

        if not numeric_rows:

            return {
                "available": True,
                "title": "Data Overview",
                "message": (
                    f"{len(rows)} records were returned."
                ),
                "insights": [],
            }

        highest = max(
            numeric_rows,
            key=lambda item: item[1],
        )

        lowest = min(
            numeric_rows,
            key=lambda item: item[1],
        )

        total = sum(
            item[1]
            for item in numeric_rows
        )

        average = (
            total / len(numeric_rows)
        )

        highest_label = self._format_value(
            highest[0]
        )

        highest_value = self._format_value(
            highest[1]
        )

        lowest_label = self._format_value(
            lowest[0]
        )

        lowest_value = self._format_value(
            lowest[1]
        )

        return {
            "available": True,
            "title": "AI-Generated Insights",
            "message": (
                f"{self._pretty(x_column)} "
                f"with the highest "
                f"{self._pretty(y_column).lower()} "
                f"is {highest_label}, "
                f"with {highest_value}."
            ),
            "insights": [
                {
                    "type": "highest",
                    "label": "Highest",
                    "value": (
                        f"{highest_label} · "
                        f"{highest_value}"
                    ),
                },
                {
                    "type": "lowest",
                    "label": "Lowest",
                    "value": (
                        f"{lowest_label} · "
                        f"{lowest_value}"
                    ),
                },
                {
                    "type": "average",
                    "label": "Average",
                    "value": self._format_value(
                        average
                    ),
                },
                {
                    "type": "records",
                    "label": "Records analyzed",
                    "value": f"{len(rows):,}",
                },
            ],
        }

    # ========================================================
    # MULTI COLUMN
    # ========================================================

    def _table_insight(
        self,
        columns: list[str],
        rows: list[dict[str, Any]],
    ) -> dict[str, Any]:

        numeric_columns = []

        for column in columns:

            values = [
                row.get(column)
                for row in rows
            ]

            numeric_values = [
                value
                for value in values
                if isinstance(
                    value,
                    (int, float),
                )
            ]

            if numeric_values:
                numeric_columns.append(
                    (
                        column,
                        numeric_values,
                    )
                )

        insights = []

        for column, values in numeric_columns[:4]:

            insights.append(
                {
                    "type": "statistic",
                    "label": self._pretty(column),
                    "value": (
                        f"avg "
                        f"{self._format_value(sum(values) / len(values))}"
                    ),
                }
            )

        return {
            "available": True,
            "title": "AI-Generated Insights",
            "message": (
                f"{len(rows):,} records were analyzed "
                f"across {len(columns)} fields."
            ),
            "insights": insights,
        }

    # ========================================================
    # HELPERS
    # ========================================================

    @staticmethod
    def _pretty(value: str) -> str:

        return (
            value
            .replace("_", " ")
            .strip()
            .title()
        )

    @staticmethod
    def _format_value(value: Any) -> str:

        if value is None:
            return "N/A"

        if isinstance(value, float):

            if value.is_integer():
                return f"{int(value):,}"

            return f"{value:,.2f}"

        if isinstance(value, int):
            return f"{value:,}"

        return str(value)