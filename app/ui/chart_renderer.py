"""
chart_renderer.py

Renders visualization instructions produced by
VisualizationSelector inside the Streamlit UI.

The renderer is intentionally separated from the selector:

VisualizationSelector
    -> decides WHAT chart should be used

ChartRenderer
    -> decides HOW that chart is rendered
"""

from typing import Any

import pandas as pd
import streamlit as st


class ChartRenderer:
    """
    Renders SQL results according to the visualization
    selected by VisualizationSelector.
    """

    def render(
        self,
        visualization: dict[str, Any],
        rows: list[dict[str, Any]],
        columns: list[str],
    ) -> None:
        """
        Render the selected visualization.
        """

        if not rows:
            self._render_empty()
            return

        chart_type = visualization.get("type")

        # --------------------------------------------------
        # Convert results into DataFrame
        # --------------------------------------------------

        dataframe = pd.DataFrame(rows)

        # --------------------------------------------------
        # Route visualization
        # --------------------------------------------------

        if chart_type == "metric":
            self._render_metric(
                dataframe,
                visualization,
            )

        elif chart_type == "bar_chart":
            self._render_bar_chart(
                dataframe,
                visualization,
            )

        elif chart_type == "horizontal_bar_chart":
            self._render_horizontal_bar_chart(
                dataframe,
                visualization,
            )

        elif chart_type == "line_chart":
            self._render_line_chart(
                dataframe,
                visualization,
            )

        elif chart_type == "area_chart":
            self._render_area_chart(
                dataframe,
                visualization,
            )

        elif chart_type == "pie_chart":
            self._render_pie_chart(
                dataframe,
                visualization,
            )

        elif chart_type == "scatter_chart":
            self._render_scatter_chart(
                dataframe,
                visualization,
            )

        elif chart_type == "grouped_bar_chart":
            self._render_grouped_bar_chart(
                dataframe,
                visualization,
            )

        elif chart_type == "multi_line_chart":
            self._render_multi_line_chart(
                dataframe,
                visualization,
            )

        elif chart_type == "table":
            self._render_table(dataframe)

        else:
            self._render_table(dataframe)

    # ======================================================
    # METRIC
    # ======================================================

    def _render_metric(
        self,
        dataframe: pd.DataFrame,
        visualization: dict[str, Any],
    ) -> None:
        """
        Render a single KPI/metric.
        """

        column = visualization.get("column")

        if not column:
            column = dataframe.columns[0]

        if column not in dataframe.columns:
            self._render_table(dataframe)
            return

        value = dataframe.iloc[0][column]

        formatted_value = self._format_value(value)

        st.metric(
            label=self._format_column_name(column),
            value=formatted_value,
        )

    # ======================================================
    # BAR CHART
    # ======================================================

    def _render_bar_chart(
        self,
        dataframe: pd.DataFrame,
        visualization: dict[str, Any],
    ) -> None:

        x_column = visualization.get("x_column")
        y_column = visualization.get("y_column")

        if not self._validate_columns(
            dataframe,
            x_column,
            y_column,
        ):
            return

        chart_data = dataframe[
            [x_column, y_column]
        ].copy()

        chart_data = chart_data.set_index(
            x_column
        )

        st.bar_chart(
            chart_data[
                y_column
            ]
        )

    # ======================================================
    # HORIZONTAL BAR CHART
    # ======================================================

    def _render_horizontal_bar_chart(
        self,
        dataframe: pd.DataFrame,
        visualization: dict[str, Any],
    ) -> None:

        x_column = visualization.get("x_column")
        y_column = visualization.get("y_column")

        if not self._validate_columns(
            dataframe,
            x_column,
            y_column,
        ):
            return

        chart_data = dataframe[
            [x_column, y_column]
        ].copy()

        chart_data = chart_data.sort_values(
            by=y_column,
            ascending=True,
        )

        chart_data = chart_data.set_index(
            x_column
        )

        st.bar_chart(
            chart_data[y_column],
            horizontal=True,
        )

    # ======================================================
    # LINE CHART
    # ======================================================

    def _render_line_chart(
        self,
        dataframe: pd.DataFrame,
        visualization: dict[str, Any],
    ) -> None:

        x_column = visualization.get("x_column")
        y_column = visualization.get("y_column")

        if not self._validate_columns(
            dataframe,
            x_column,
            y_column,
        ):
            return

        chart_data = dataframe[
            [x_column, y_column]
        ].copy()

        chart_data = self._prepare_time_data(
            chart_data,
            x_column,
        )

        chart_data = chart_data.set_index(
            x_column
        )

        st.line_chart(
            chart_data[y_column]
        )

    # ======================================================
    # AREA CHART
    # ======================================================

    def _render_area_chart(
        self,
        dataframe: pd.DataFrame,
        visualization: dict[str, Any],
    ) -> None:

        x_column = visualization.get("x_column")
        y_column = visualization.get("y_column")

        if not self._validate_columns(
            dataframe,
            x_column,
            y_column,
        ):
            return

        chart_data = dataframe[
            [x_column, y_column]
        ].copy()

        chart_data = self._prepare_time_data(
            chart_data,
            x_column,
        )

        chart_data = chart_data.set_index(
            x_column
        )

        st.area_chart(
            chart_data[y_column]
        )

    # ======================================================
    # PIE CHART
    # ======================================================

    def _render_pie_chart(
        self,
        dataframe: pd.DataFrame,
        visualization: dict[str, Any],
    ) -> None:

        x_column = visualization.get("x_column")
        y_column = visualization.get("y_column")

        if not self._validate_columns(
            dataframe,
            x_column,
            y_column,
        ):
            return

        chart_data = dataframe[
            [x_column, y_column]
        ].copy()

        chart_data = chart_data.set_index(
            x_column
        )

        st.bar_chart(
            chart_data[y_column]
        )

        st.caption(
            "Categorical distribution. "
            "The table below provides exact values."
        )

    # ======================================================
    # SCATTER CHART
    # ======================================================

    def _render_scatter_chart(
        self,
        dataframe: pd.DataFrame,
        visualization: dict[str, Any],
    ) -> None:

        x_column = visualization.get("x_column")
        y_column = visualization.get("y_column")

        if not self._validate_columns(
            dataframe,
            x_column,
            y_column,
        ):
            return

        chart_data = dataframe[
            [x_column, y_column]
        ].copy()

        st.scatter_chart(
            chart_data,
            x=x_column,
            y=y_column,
        )

    # ======================================================
    # GROUPED BAR CHART
    # ======================================================

    def _render_grouped_bar_chart(
        self,
        dataframe: pd.DataFrame,
        visualization: dict[str, Any],
    ) -> None:

        x_column = visualization.get("x_column")
        y_columns = visualization.get(
            "y_columns",
            [],
        )

        if not x_column:
            self._render_table(dataframe)
            return

        if x_column not in dataframe.columns:
            self._render_table(dataframe)
            return

        valid_y_columns = [
            column
            for column in y_columns
            if column in dataframe.columns
        ]

        if not valid_y_columns:
            self._render_table(dataframe)
            return

        chart_data = dataframe[
            [x_column] + valid_y_columns
        ].copy()

        chart_data = chart_data.set_index(
            x_column
        )

        st.bar_chart(
            chart_data
        )

    # ======================================================
    # MULTI-LINE CHART
    # ======================================================

    def _render_multi_line_chart(
        self,
        dataframe: pd.DataFrame,
        visualization: dict[str, Any],
    ) -> None:

        x_column = visualization.get("x_column")
        y_columns = visualization.get(
            "y_columns",
            [],
        )

        if not x_column:
            self._render_table(dataframe)
            return

        valid_y_columns = [
            column
            for column in y_columns
            if column in dataframe.columns
        ]

        if not valid_y_columns:
            self._render_table(dataframe)
            return

        chart_data = dataframe[
            [x_column] + valid_y_columns
        ].copy()

        chart_data = self._prepare_time_data(
            chart_data,
            x_column,
        )

        chart_data = chart_data.set_index(
            x_column
        )

        st.line_chart(
            chart_data[
                valid_y_columns
            ]
        )

    # ======================================================
    # TABLE
    # ======================================================

    def _render_table(
        self,
        dataframe: pd.DataFrame,
    ) -> None:

        st.dataframe(
            dataframe,
            use_container_width=True,
            hide_index=True,
        )

    # ======================================================
    # EMPTY
    # ======================================================

    def _render_empty(self) -> None:

        st.info(
            "No data was returned for this query."
        )

    # ======================================================
    # HELPERS
    # ======================================================

    def _validate_columns(
        self,
        dataframe: pd.DataFrame,
        *columns: str | None,
    ) -> bool:
        """
        Verify that requested columns exist.
        """

        valid_columns = [
            column
            for column in columns
            if column
        ]

        missing = [
            column
            for column in valid_columns
            if column not in dataframe.columns
        ]

        if missing:

            st.warning(
                "Unable to render visualization. "
                f"Missing columns: {', '.join(missing)}"
            )

            return False

        return True

    def _prepare_time_data(
        self,
        dataframe: pd.DataFrame,
        column: str,
    ) -> pd.DataFrame:
        """
        Prepare common time representations.
        """

        result = dataframe.copy()

        if "year" in column.lower():

            result[column] = pd.to_numeric(
                result[column],
                errors="coerce",
            )

            result = result.sort_values(
                by=column
            )

        elif (
            "date" in column.lower()
            or "time" in column.lower()
            or "timestamp" in column.lower()
        ):

            result[column] = pd.to_datetime(
                result[column],
                errors="coerce",
            )

            result = result.dropna(
                subset=[column]
            )

            result = result.sort_values(
                by=column
            )

        return result

    def _format_column_name(
        self,
        column: str,
    ) -> str:
        """
        Convert database-style column names
        into readable UI labels.
        """

        return (
            column
            .replace("_", " ")
            .strip()
            .title()
        )

    def _format_value(
        self,
        value: Any,
    ) -> str:
        """
        Format common numeric values for display.
        """

        if value is None:
            return "N/A"

        if isinstance(
            value,
            float,
        ):

            if value.is_integer():
                return f"{int(value):,}"

            return f"{value:,.2f}"

        if isinstance(
            value,
            int,
        ):

            return f"{value:,}"

        return str(value)


if __name__ == "__main__":

    print(
        "ChartRenderer loaded successfully."
    )