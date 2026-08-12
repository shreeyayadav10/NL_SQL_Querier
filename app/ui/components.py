"""
components.py

Reusable Streamlit presentation components for the
Olist AI Business Intelligence Assistant.

Presentation layer only.

The component layer accepts results from:
    QueryService
    QueryPipeline
    ResultFormatter
    VisualizationSelector

It is intentionally defensive so small changes in the
backend result structure do not break the Streamlit UI.
"""

from __future__ import annotations

from typing import Any

import pandas as pd
import streamlit as st


# ============================================================
# HERO
# ============================================================

def render_hero() -> None:
    """Render the main application hero."""

    st.markdown(
        "### AI-POWERED BUSINESS INTELLIGENCE"
    )

    st.title(
        "Ask your data. Get answers."
    )

    st.caption(
        "Transform natural-language business questions "
        "into validated SQL, database results, insights, "
        "and interactive visualizations."
    )

    st.success(
        "Analytics Engine Online",
        icon="🟢",
    )


# ============================================================
# SIDEBAR
# ============================================================

def render_sidebar_header() -> None:
    """Render sidebar branding."""

    st.title("Olist Intelligence")

    st.caption(
        "Natural-language analytics for customers, "
        "orders, products, payments, reviews, "
        "delivery and sales."
    )

    st.divider()


# ============================================================
# SUCCESS
# ============================================================

def render_success_status() -> None:
    """Render successful query status."""

    st.success(
        "Query executed successfully",
        icon="🟢",
    )


# ============================================================
# ERROR
# ============================================================

def render_error(error: str | Exception | None) -> None:
    """Render query error."""

    st.error("Query execution failed")

    if error:
        st.caption(str(error))


# ============================================================
# QUERY METRICS
# ============================================================

def render_query_metrics(
    row_count: int | None,
    execution_time: float | None,
    column_count: int | None,
) -> None:
    """Render query execution metrics."""

    row_count = int(row_count or 0)
    execution_time = float(execution_time or 0.0)
    column_count = int(column_count or 0)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Rows Returned",
            f"{row_count:,}",
        )

    with col2:
        st.metric(
            "Execution Time",
            f"{execution_time:.2f} ms",
        )

    with col3:
        st.metric(
            "Columns",
            f"{column_count:,}",
        )


# ============================================================
# SQL
# ============================================================

def render_sql(sql: str | None) -> None:
    """Display generated SQL."""

    if not sql:
        return

    with st.expander(
        "Generated SQL",
        expanded=False,
    ):
        st.code(
            str(sql).strip(),
            language="sql",
        )


# ============================================================
# RESULT NORMALIZATION
# ============================================================

def _get_formatted_result(
    result: dict[str, Any],
) -> dict[str, Any]:
    """
    Extract the formatted result.

    Supports:

        result["formatted_result"]

    and also a result that is already formatted.
    """

    formatted = result.get("formatted_result")

    if isinstance(formatted, dict):
        return formatted

    return result


def _get_rows(
    result: dict[str, Any],
) -> list[dict[str, Any]]:
    """Extract result rows from any supported result structure."""

    formatted = _get_formatted_result(result)

    rows = formatted.get("rows")

    if isinstance(rows, list):
        return [
            row
            for row in rows
            if isinstance(row, dict)
        ]

    rows = result.get("rows")

    if isinstance(rows, list):
        return [
            row
            for row in rows
            if isinstance(row, dict)
        ]

    return []


def _get_columns(
    result: dict[str, Any],
) -> list[str]:
    """Extract result columns."""

    formatted = _get_formatted_result(result)

    columns = formatted.get("columns")

    if isinstance(columns, list):
        return [
            str(column)
            for column in columns
        ]

    columns = result.get("columns")

    if isinstance(columns, list):
        return [
            str(column)
            for column in columns
        ]

    rows = _get_rows(result)

    if rows:
        return list(rows[0].keys())

    return []


def _build_dataframe(
    result: dict[str, Any],
) -> pd.DataFrame:
    """Build a DataFrame from the result."""

    rows = _get_rows(result)

    if not rows:
        return pd.DataFrame()

    dataframe = pd.DataFrame(rows)

    columns = _get_columns(result)

    if columns:
        valid_columns = [
            column
            for column in columns
            if column in dataframe.columns
        ]

        if valid_columns:
            dataframe = dataframe[valid_columns]

    return dataframe


# ============================================================
# VISUALIZATION
# ============================================================

def render_visualization(
    result: dict[str, Any] | None,
) -> None:
    """
    Render a visualization from a query result.

    The function supports all current project contracts:

    1. result["chart_data"]
    2. result["visualization"]
    3. result["formatted_result"]["chart_data"]
    4. result["columns"] + result["rows"]
    5. result["formatted_result"]["columns"]
       + result["formatted_result"]["rows"]

    Therefore the UI does not depend on chart_data being
    explicitly attached by the pipeline.
    """

    if not result:
        st.info(
            "No result available for visualization."
        )
        return

    if not isinstance(result, dict):
        st.info(
            "Invalid result received for visualization."
        )
        return

    formatted = _get_formatted_result(result)

    # --------------------------------------------------------
    # Get explicit visualization metadata
    # --------------------------------------------------------

    chart_data = result.get("chart_data")

    if not isinstance(chart_data, dict):
        chart_data = {}

    if not chart_data:
        nested_chart_data = formatted.get(
            "chart_data"
        )

        if isinstance(
            nested_chart_data,
            dict,
        ):
            chart_data = nested_chart_data

    visualization = result.get(
        "visualization"
    )

    if not isinstance(
        visualization,
        dict,
    ):
        visualization = {}

    # --------------------------------------------------------
    # Extract explicit metadata
    # --------------------------------------------------------

    x_column = chart_data.get(
        "x_column"
    )

    y_column = chart_data.get(
        "y_column"
    )

    chart_type = chart_data.get(
        "chart_type",
        chart_data.get(
            "type",
            "bar",
        ),
    )

    x_values = chart_data.get(
        "x",
        [],
    )

    y_values = chart_data.get(
        "y",
        [],
    )

    # VisualizationSelector may use a different contract.
    if not x_column:
        x_column = visualization.get(
            "x_column"
        )

    if not y_column:
        y_column = visualization.get(
            "y_column"
        )

    if visualization.get("type"):
        chart_type = visualization.get(
            "type"
        )

    if visualization.get("chart_type"):
        chart_type = visualization.get(
            "chart_type"
        )

    # --------------------------------------------------------
    # Build DataFrame from actual result
    # --------------------------------------------------------

    dataframe = _build_dataframe(
        result
    )

    if dataframe.empty:
        st.info(
            "No chart data is available."
        )
        return

    # --------------------------------------------------------
    # Automatic fallback
    #
    # This is the important part.
    #
    # Even if the backend returns only:
    #
    # columns = ["customer_state", "order_count"]
    # rows = [...]
    #
    # the UI will automatically identify:
    #
    # X = customer_state
    # Y = order_count
    # --------------------------------------------------------

    if (
        not x_column
        or not y_column
    ):

        columns = list(
            dataframe.columns
        )

        if len(columns) >= 2:

            # First column is normally the category/time axis.
            candidate_x = columns[0]

            # Prefer the first numeric column after X.
            candidate_y = None

            for column in columns[1:]:

                numeric_values = pd.to_numeric(
                    dataframe[column],
                    errors="coerce",
                )

                if numeric_values.notna().any():
                    candidate_y = column
                    break

            if candidate_y is not None:

                x_column = candidate_x
                y_column = candidate_y

                # Ranking/grouped results naturally use bars.
                chart_type = "bar"

    # --------------------------------------------------------
    # Final validation
    # --------------------------------------------------------

    if not x_column:
        st.info(
            "Chart X-axis column is unavailable."
        )
        return

    if not y_column:
        st.info(
            "Chart Y-axis column is unavailable."
        )
        return

    if (
        x_column not in dataframe.columns
        or y_column not in dataframe.columns
    ):
        st.info(
            "The selected chart columns are not present "
            "in the query result."
        )
        return

    # --------------------------------------------------------
    # Prepare chart data
    # --------------------------------------------------------

    chart_dataframe = dataframe[
        [x_column, y_column]
    ].copy()

    chart_dataframe = chart_dataframe.dropna(
        subset=[
            x_column,
            y_column,
        ]
    )

    if chart_dataframe.empty:
        st.info(
            "No chart data is available."
        )
        return

    # Convert Y to numeric.
    chart_dataframe[y_column] = pd.to_numeric(
        chart_dataframe[y_column],
        errors="coerce",
    )

    chart_dataframe = chart_dataframe.dropna(
        subset=[
            y_column,
        ]
    )

    if chart_dataframe.empty:
        st.info(
            "The selected metric contains no numeric values."
        )
        return

    # --------------------------------------------------------
    # Normalize chart type names
    # --------------------------------------------------------

    chart_type = str(
        chart_type or "bar"
    ).lower().strip()

    chart_type_map = {
        "bar_chart": "bar",
        "line_chart": "line",
        "area_chart": "area",
        "horizontal_bar": "bar",
        "column": "bar",
    }

    chart_type = chart_type_map.get(
        chart_type,
        chart_type,
    )

    # --------------------------------------------------------
    # Visualization title
    # --------------------------------------------------------

    st.markdown(
        "#### Interactive Visualization"
    )

    # --------------------------------------------------------
    # BAR
    # --------------------------------------------------------

    if chart_type == "bar":

        chart_dataframe = (
            chart_dataframe
            .set_index(x_column)
        )

        st.bar_chart(
            chart_dataframe[y_column],
            use_container_width=True,
        )

    # --------------------------------------------------------
    # LINE
    # --------------------------------------------------------

    elif chart_type == "line":

        chart_dataframe = (
            chart_dataframe
            .set_index(x_column)
        )

        st.line_chart(
            chart_dataframe[y_column],
            use_container_width=True,
        )

    # --------------------------------------------------------
    # AREA
    # --------------------------------------------------------

    elif chart_type == "area":

        chart_dataframe = (
            chart_dataframe
            .set_index(x_column)
        )

        st.area_chart(
            chart_dataframe[y_column],
            use_container_width=True,
        )

    # --------------------------------------------------------
    # SCATTER
    # --------------------------------------------------------

    elif chart_type == "scatter":

        st.scatter_chart(
            chart_dataframe,
            x=x_column,
            y=y_column,
            use_container_width=True,
        )

    # --------------------------------------------------------
    # PIE
    # --------------------------------------------------------

    elif chart_type == "pie":

        try:

            import plotly.express as px

            figure = px.pie(
                chart_dataframe,
                names=x_column,
                values=y_column,
                hole=0.35,
            )

            st.plotly_chart(
                figure,
                use_container_width=True,
            )

        except ImportError:

            # Plotly is optional.
            chart_dataframe = (
                chart_dataframe
                .set_index(x_column)
            )

            st.bar_chart(
                chart_dataframe[y_column],
                use_container_width=True,
            )

    # --------------------------------------------------------
    # SAFE DEFAULT
    # --------------------------------------------------------

    else:

        chart_dataframe = (
            chart_dataframe
            .set_index(x_column)
        )

        st.bar_chart(
            chart_dataframe[y_column],
            use_container_width=True,
        )

    st.caption(
        f"{chart_type.title()} chart • "
        f"{x_column} vs {y_column}"
    )


# ============================================================
# RESULT TABLE
# ============================================================

def render_result_table(
    result: dict[str, Any] | None,
) -> None:
    """Render query rows as a Streamlit dataframe."""

    if not result:
        return

    dataframe = _build_dataframe(
        result
    )

    if dataframe.empty:
        return

    st.dataframe(
        dataframe,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# DOWNLOAD
# ============================================================

def render_download_button(
    rows: list[dict[str, Any]] | None,
) -> None:
    """Provide CSV download functionality."""

    if not rows:
        return

    dataframe = pd.DataFrame(
        rows
    )

    if dataframe.empty:
        return

    csv_data = dataframe.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download CSV",
        data=csv_data,
        file_name="olist_query_result.csv",
        mime="text/csv",
    )


# ============================================================
# EMPTY RESULT
# ============================================================

def render_empty_result() -> None:
    """Render empty result state."""

    st.info(
        "No results found. "
        "The query executed successfully, "
        "but returned no matching records."
    )


# ============================================================
# SUGGESTION SECTION
# ============================================================

def render_suggestion_section(
    question_bank: dict[str, list[str]],
) -> None:
    """
    Render suggested analytics questions.

    Selecting a question stores it in Streamlit session
    state and reruns the application.
    """

    st.subheader(
        "Explore your data"
    )

    st.caption(
        "Choose a business area and start with "
        "a ready-made analytics question."
    )

    if not question_bank:

        st.info(
            "No example questions are currently available."
        )

        return

    categories = list(
        question_bank.items()
    )

    for start in range(
        0,
        len(categories),
        3,
    ):

        current_categories = categories[
            start:start + 3
        ]

        columns = st.columns(
            len(current_categories)
        )

        for column, (
            category,
            questions,
        ) in zip(
            columns,
            current_categories,
        ):

            with column:

                st.markdown(
                    f"**{category}**"
                )

                if not questions:
                    st.caption(
                        "No questions available."
                    )
                    continue

                st.caption(
                    f"{len(questions)} questions"
                )

                for index, question in enumerate(
                    questions[:3]
                ):

                    button_key = (
                        f"suggestion_"
                        f"{start}_"
                        f"{index}_"
                        f"{category}"
                    )

                    if st.button(
                        question,
                        key=button_key,
                        use_container_width=True,
                    ):

                        st.session_state[
                            "selected_question"
                        ] = question

                        st.rerun()


# ============================================================
# QUERY HISTORY
# ============================================================

def add_query_to_history(
    question: str,
    sql: str,
    row_count: int,
) -> None:
    """Store a successful query in session history."""

    if (
        "query_history"
        not in st.session_state
    ):
        st.session_state[
            "query_history"
        ] = []

    history_entry = {
        "question": question,
        "sql": sql,
        "row_count": int(
            row_count or 0
        ),
    }

    st.session_state[
        "query_history"
    ].insert(
        0,
        history_entry,
    )

    st.session_state[
        "query_history"
    ] = (
        st.session_state[
            "query_history"
        ][:20]
    )


def render_query_history() -> None:
    """Render previous queries."""

    history = st.session_state.get(
        "query_history",
        [],
    )

    if not history:
        return

    st.subheader(
        "Recent Queries"
    )

    for index, item in enumerate(
        history
    ):

        question = item.get(
            "question",
            "",
        )

        row_count = item.get(
            "row_count",
            0,
        )

        with st.expander(
            f"{index + 1}. {question}"
        ):

            st.caption(
                f"{row_count:,} rows returned"
            )

            sql = item.get(
                "sql",
                "",
            )

            if sql:
                st.code(
                    sql,
                    language="sql",
                )


# ============================================================
# FOOTER
# ============================================================

def render_footer() -> None:
    """Render application footer."""

    st.divider()

    st.caption(
        "AI Business Intelligence Assistant • "
        "Natural Language → SQL → Validation → "
        "Execution → Analytics"
    )

    st.caption(
        "Built with Python, SQL, LangChain, "
        "Streamlit and SQLite."
    )


# ============================================================
# HELPERS
# ============================================================

def _pretty_label(
    value: str,
) -> str:
    """Convert technical column name to readable text."""

    return (
        str(value)
        .replace("_", " ")
        .strip()
        .title()
    )


def _format_value(
    value: Any,
) -> str:
    """Format metric values."""

    if value is None:
        return "N/A"

    if isinstance(
        value,
        float,
    ):
        return f"{value:,.2f}"

    if isinstance(
        value,
        int,
    ):
        return f"{value:,}"

    return str(value)


# ============================================================
# OPTIONAL METRIC RESULT
# ============================================================

def render_scalar_result(
    rows: list[dict[str, Any]] | None,
) -> None:
    """Render a scalar query result as a metric."""

    if not rows:
        return

    first_row = rows[0]

    if not isinstance(
        first_row,
        dict,
    ) or not first_row:
        return

    column = next(
        iter(first_row)
    )

    value = first_row.get(
        column
    )

    st.metric(
        _pretty_label(column),
        _format_value(value),
    )