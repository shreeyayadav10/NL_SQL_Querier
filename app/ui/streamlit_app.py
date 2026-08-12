"""
streamlit_app.py

AI Business Intelligence Assistant.

Presentation layer only.

Flow:
    User Question
        ↓
    QueryService
        ↓
    NL → SQL Pipeline
        ↓
    Result + Analytics Metadata
        ↓
    Streamlit Dashboard
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# APPLICATION IMPORTS
# ============================================================

from app.ui import components
from app.ui import styles
from app.ui.question_bank import QUESTION_BANK
from app.ui.query_service import QueryService


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Olist AI Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# GLOBAL STYLES
# ============================================================

styles.apply_styles()


# ============================================================
# SESSION STATE
# ============================================================

def initialize_session_state() -> None:
    """Initialize all application state."""

    defaults = {
        "query_service": None,
        "history": [],
        "last_result": None,
        "selected_question": "",
        "question_category": list(QUESTION_BANK.keys())[0]
        if QUESTION_BANK
        else "",
        "question_selector": "",
        "show_sql": True,
    }

    for key, value in defaults.items():

        if key not in st.session_state:
            st.session_state[key] = value

    if st.session_state.query_service is None:

        with st.spinner("Initializing analytics engine..."):

            st.session_state.query_service = QueryService()


initialize_session_state()


# ============================================================
# HELPERS
# ============================================================

def set_question(question: str) -> None:
    """Set the current question."""

    st.session_state.selected_question = question


def clear_current_query() -> None:
    """Clear the active question and result."""

    st.session_state.selected_question = ""
    st.session_state.last_result = None


def add_to_history(
    question: str,
    result: dict,
) -> None:
    """Add a query result to recent history."""

    history_item = {
        "question": question,
        "result": result,
    }

    st.session_state.history.append(history_item)

    # Keep only the latest 20 queries.
    st.session_state.history = (
        st.session_state.history[-20:]
    )


def run_question(question: str) -> None:
    """Execute a question through QueryService."""

    question = question.strip()

    if not question:
        st.warning("Enter a business question first.")
        return

    with st.spinner(
        "Analyzing your question and generating SQL..."
    ):

        try:

            result = (
                st.session_state.query_service
                .execute(question)
            )

        except Exception as error:

            result = {
                "success": False,
                "error": str(error),
                "question": question,
            }

    st.session_state.last_result = result

    add_to_history(
        question,
        result,
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    components.render_sidebar_header()

    st.divider()

    # --------------------------------------------------------
    # ANALYTICS EXPLORER
    # --------------------------------------------------------

    st.markdown(
        "### Explore Analytics"
    )

    st.caption(
        "Choose a business area and start with a ready-made question."
    )

    categories = list(
        QUESTION_BANK.keys()
    )

    if categories:

        selected_category = st.selectbox(
            "Category",
            categories,
            key="question_category",
        )

        questions = QUESTION_BANK.get(
            selected_category,
            [],
        )

        if questions:

            selected_question = st.selectbox(
                "Suggested question",
                questions,
                key="question_selector",
            )

            if st.button(
                "Use this question",
                use_container_width=True,
            ):

                set_question(
                    selected_question
                )

                st.rerun()

    # --------------------------------------------------------
    # QUICK STATS
    # --------------------------------------------------------

    st.divider()

    st.markdown(
        "### Workspace"
    )

    history_count = len(
        st.session_state.history
    )

    st.metric(
        "Queries analyzed",
        history_count,
    )

    # --------------------------------------------------------
    # RECENT HISTORY
    # --------------------------------------------------------

    st.divider()

    st.markdown(
        "### Recent Queries"
    )

    history = st.session_state.history

    if not history:

        st.caption(
            "Your recent questions will appear here."
        )

    else:

        recent_items = list(
            reversed(
                history[-6:]
            )
        )

        for index, item in enumerate(
            recent_items
        ):

            question_text = item.get(
                "question",
                "Unnamed query",
            )

            if len(question_text) > 55:

                question_text = (
                    question_text[:55]
                    + "..."
                )

            if st.button(
                question_text,
                key=f"history_{index}",
                use_container_width=True,
            ):

                st.session_state.selected_question = (
                    item["question"]
                )

                st.session_state.last_result = (
                    item["result"]
                )

                st.rerun()

    # --------------------------------------------------------
    # CLEAR HISTORY
    # --------------------------------------------------------

    st.divider()

    if st.button(
        "Clear History",
        use_container_width=True,
    ):

        st.session_state.history = []

        st.rerun()


# ============================================================
# HERO
# ============================================================

components.render_hero()


# ============================================================
# QUERY WORKSPACE
# ============================================================

st.markdown(
    "## Ask your data"
)

st.caption(
    "Turn natural-language business questions into SQL-powered analytics."
)


# ============================================================
# QUESTION INPUT
# ============================================================

question = st.text_area(
    "Business question",
    value=st.session_state.selected_question,
    placeholder=(
        "Examples:\n"
        "• Which states have the highest number of orders?\n"
        "• What is the average review score?\n"
        "• Which payment type is used most often?\n"
        "• What are the top product categories by revenue?"
    ),
    height=120,
    label_visibility="collapsed",
)


# ============================================================
# QUERY CONTROLS
# ============================================================

control_1, control_2, control_3, control_4 = st.columns(
    [2.2, 1, 1, 1.2]
)


with control_1:

    run_analysis = st.button(
        "Run Analysis",
        type="primary",
        use_container_width=True,
    )


with control_2:

    clear_button = st.button(
        "Clear",
        use_container_width=True,
    )


with control_3:

    st.session_state.show_sql = st.toggle(
        "Show SQL",
        value=st.session_state.show_sql,
    )


with control_4:

    if st.button(
        "Example",
        use_container_width=True,
    ):

        if categories:

            first_category = categories[0]

            first_questions = QUESTION_BANK.get(
                first_category,
                [],
            )

            if first_questions:

                set_question(
                    first_questions[0]
                )

                st.rerun()


# ============================================================
# CLEAR ACTIVE QUERY
# ============================================================

if clear_button:

    clear_current_query()

    st.rerun()


# ============================================================
# EXECUTE
# ============================================================

if run_analysis:

    run_question(
        question
    )


# ============================================================
# RESULT AREA
# ============================================================

result = st.session_state.last_result


if result is not None:

    st.divider()

    # ========================================================
    # FAILED QUERY
    # ========================================================

    if not result.get(
        "success",
        False,
    ):

        components.render_error(
            result.get(
                "error",
                "Query execution failed.",
            )
        )

    # ========================================================
    # SUCCESSFUL QUERY
    # ========================================================

    else:

        components.render_success_status()

        columns = result.get(
            "columns",
            [],
        )

        rows = result.get(
            "rows",
            [],
        )

        row_count = result.get(
            "row_count",
            0,
        )

        execution_time = result.get(
            "execution_time_ms",
            0,
        )

        formatted_result = result.get(
            "formatted_result",
            {},
        )

        summary = result.get(
            "summary",
            "",
        )

        # ====================================================
        # RESULT HEADER
        # ====================================================

        st.markdown(
            "## Analysis Result"
        )

        if summary:

            st.caption(
                summary
            )

        # ====================================================
        # KPI METRICS
        # ====================================================

        components.render_query_metrics(
            row_count=row_count,
            execution_time=execution_time,
            column_count=len(columns),
        )

        # ====================================================
        # SQL
        # ====================================================

        if st.session_state.show_sql:

            with st.expander(
                "Generated SQL",
                expanded=False,
            ):

                components.render_sql(
                    result.get(
                        "sql",
                        "",
                    )
                )

        # ====================================================
        # DATA RESULT
        # ====================================================

        if rows:

            dataframe = pd.DataFrame(
                rows
            )

            st.markdown(
                "### Data"
            )

            st.dataframe(
                dataframe,
                use_container_width=True,
                hide_index=True,
            )

            # =================================================
            # EXPORT
            # =================================================

            export_col1, export_col2 = st.columns(
                [1, 5]
            )

            with export_col1:

                csv_data = dataframe.to_csv(
                    index=False
                ).encode("utf-8")

                st.download_button(
                    "Download CSV",
                    data=csv_data,
                    file_name="olist_analysis.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

            # =================================================
            # ADVANCED RESULT INFORMATION
            # =================================================

            if formatted_result:

                with st.expander(
                    "Result Details",
                    expanded=False,
                ):

                    detail_col1, detail_col2 = st.columns(
                        2
                    )

                    with detail_col1:

                        st.write(
                            "Result Type"
                        )

                        st.code(
                            str(
                                formatted_result.get(
                                    "result_type",
                                    "table",
                                )
                            )
                        )

                    with detail_col2:

                        st.write(
                            "Rows Returned"
                        )

                        st.code(
                            str(row_count)
                        )

                    statistics = formatted_result.get(
                        "statistics"
                    )

                    if statistics:

                        st.write(
                            "Column Statistics"
                        )

                        st.json(
                            statistics
                        )

            # =================================================
            # VISUALIZATION
            # =================================================

            st.markdown(
                "### Visualization"
            )

            components.render_visualization(
                result
            )

        else:

            components.render_empty_result()


# ============================================================
# EMPTY WORKSPACE
# ============================================================

else:

    components.render_suggestion_section(
        QUESTION_BANK
    )


# ============================================================
# FOOTER
# ============================================================

components.render_footer()