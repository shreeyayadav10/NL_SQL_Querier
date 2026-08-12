from typing import Any


class VisualizationSelector:
    """
    Selects the most appropriate visualization for SQL query results.

    Rules:
    - Empty result -> empty
    - Scalar result -> metric
    - Two columns with a time/year column + numeric column -> line_chart
    - Two columns with categorical column + numeric column -> bar_chart
    - More than two columns -> table
    """

    TIME_COLUMNS = {
        "year",
        "month",
        "date",
        "day",
        "week",
        "timestamp",
        "order_purchase_timestamp",
        "purchase_date",
    }

    def select(
        self,
        columns: list[str],
        rows: list[dict[str, Any]],
        result_type: str,
    ) -> dict[str, Any]:

        # --------------------------------------------------
        # Empty result
        # --------------------------------------------------
        if result_type == "empty" or not rows or not columns:
            return {
                "type": "empty"
            }

        # --------------------------------------------------
        # Scalar / metric
        # --------------------------------------------------
        if result_type == "scalar" or len(columns) == 1:
            return {
                "type": "metric",
                "column": columns[0],
            }

        # --------------------------------------------------
        # Two-column analytical result
        # --------------------------------------------------
        if len(columns) == 2:
            x_column = columns[0]
            y_column = columns[1]

            # Check whether the second column is numeric.
            numeric_y = self._is_numeric_column(rows, y_column)

            if numeric_y:
                # Time-series data -> line chart
                if self._is_time_column(x_column):
                    return {
                        "type": "line_chart",
                        "x_column": x_column,
                        "y_column": y_column,
                    }

                # Categorical + numeric -> bar chart
                return {
                    "type": "bar_chart",
                    "x_column": x_column,
                    "y_column": y_column,
                }

        # --------------------------------------------------
        # More complex result -> table
        # --------------------------------------------------
        return {
            "type": "table"
        }

    def _is_numeric_column(
        self,
        rows: list[dict[str, Any]],
        column: str,
    ) -> bool:
        """
        Check whether a column contains numeric values.
        """

        values = [
            row.get(column)
            for row in rows
            if row.get(column) is not None
        ]

        if not values:
            return False

        return all(
            isinstance(value, (int, float))
            and not isinstance(value, bool)
            for value in values
        )

    def _is_time_column(self, column: str) -> bool:
        """
        Determine whether a column represents time.
        """

        normalized = column.lower().strip()

        if normalized in self.TIME_COLUMNS:
            return True

        return any(
            keyword in normalized
            for keyword in (
                "_date",
                "_time",
                "date_",
                "time_",
                "timestamp",
            )
        )
