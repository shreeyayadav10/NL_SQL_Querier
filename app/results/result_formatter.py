"""
Result formatting layer for NL-SQL Querier.

Converts raw SQL execution results into a consistent structure
used by the UI, visualization layer, and tests.
"""

from __future__ import annotations

from typing import Any


class ResultFormatter:
    """Format SQL query results into a predictable application structure."""

    def format(
        self,
        columns: list[str] | None,
        rows: list[dict[str, Any]] | None,
        row_count: int | None = None,
        execution_time_ms: float | None = None,
    ) -> dict[str, Any]:
        """
        Format raw SQL execution results.

        Result types:
        - empty
        - scalar
        - table
        """

        columns = list(columns or [])
        rows = list(rows or [])

        actual_row_count = (
            len(rows)
            if row_count is None
            else row_count
        )

        # --------------------------------------------------
        # Empty result
        # --------------------------------------------------

        if actual_row_count == 0 or not rows:
            return {
                "result_type": "empty",
                "has_results": False,
                "row_count": 0,
                "column_count": len(columns),
                "columns": columns,
                "rows": [],
                "execution_time_ms": execution_time_ms,
                "data": [],
            }

        # --------------------------------------------------
        # Scalar result
        # --------------------------------------------------

        if (
            len(columns) == 1
            and actual_row_count == 1
        ):
            column = columns[0]
            value = rows[0].get(column)

            return {
                "result_type": "scalar",
                "has_results": True,
                "row_count": 1,
                "column_count": 1,
                "columns": columns,
                "rows": rows,
                "execution_time_ms": execution_time_ms,
                "value": value,
                "scalar_column": column,
                "data": rows,
            }

        # --------------------------------------------------
        # Normal table result
        # --------------------------------------------------

        return {
            "result_type": "table",
            "has_results": True,
            "row_count": actual_row_count,
            "column_count": len(columns),
            "columns": columns,
            "rows": rows,
            "execution_time_ms": execution_time_ms,
            "data": rows,
        }

    # ======================================================
    # SUMMARY
    # ======================================================

    def get_summary(
        self,
        result: dict[str, Any],
    ) -> str:
        """Return a human-readable summary."""

        result_type = result.get(
            "result_type",
            "unknown",
        )

        row_count = result.get(
            "row_count",
            0,
        )

        column_count = result.get(
            "column_count",
            0,
        )

        execution_time = result.get(
            "execution_time_ms",
        )

        if result_type == "empty":

            summary = "Query returned no results."

        elif result_type == "scalar":

            column = result.get(
                "scalar_column",
                "value",
            )

            value = result.get(
                "value",
            )

            summary = f"{column}: {value}"

        elif result_type == "table":

            summary = (
                f"Query returned "
                f"{row_count} row"
                f"{'' if row_count == 1 else 's'} "
                f"across "
                f"{column_count} column"
                f"{'' if column_count == 1 else 's'}."
            )

        else:

            summary = (
                f"Query returned "
                f"{row_count} row"
                f"{'' if row_count == 1 else 's'}."
            )

        if execution_time is not None:
            summary += (
                f" Execution time: "
                f"{execution_time:.2f} ms."
            )

        return summary

    # ======================================================
    # CHART DATA
    # ======================================================

    def get_chart_data(
        self,
        result: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Determine whether the result can be visualized.

        For a two-column result:

        first column  -> X axis
        second column -> Y axis
        """

        if not result.get("has_results"):

            return {
                "supported": False,
                "reason": (
                    "No results available "
                    "for visualization."
                ),
                "x_column": None,
                "y_column": None,
                "columns": [],
                "rows": [],
                "data": [],
            }

        columns = result.get(
            "columns",
            [],
        )

        rows = result.get(
            "rows",
            [],
        )

        if len(columns) < 2:

            return {
                "supported": False,
                "reason": (
                    "At least two columns "
                    "are required for visualization."
                ),
                "x_column": None,
                "y_column": None,
                "columns": columns,
                "rows": rows,
                "data": rows,
            }

        x_column = columns[0]
        y_column = columns[1]

        return {
            "supported": True,
            "x_column": x_column,
            "y_column": y_column,
            "columns": columns,
            "rows": rows,
            "data": rows,
        }