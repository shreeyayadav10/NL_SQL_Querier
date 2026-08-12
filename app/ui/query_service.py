"""
query_service.py

Application service connecting:

Question
    ↓
Query Pipeline
    ↓
Result Formatting
    ↓
Visualization
    ↓
Business Insights
"""

from __future__ import annotations

from app.analytics.insight_engine import InsightEngine
from app.pipeline.query_pipeline import QueryPipeline
from app.results.result_formatter import ResultFormatter
from app.visualization.visualization_selector import (
    VisualizationSelector,
)


class QueryService:
    """
    High-level application service used by Streamlit.

    This service guarantees that the UI receives:
    - formatted_result
    - columns
    - rows
    - chart_data
    - visualization
    - insights
    """

    def __init__(self) -> None:
        self.pipeline = QueryPipeline()
        self.result_formatter = ResultFormatter()
        self.visualization_selector = VisualizationSelector()
        self.insight_engine = InsightEngine()

    def execute(self, question: str) -> dict:
        """Execute a natural-language business question."""

        question = question.strip()

        if not question:
            return {
                "success": False,
                "error": "Please enter a business question.",
            }

        # ----------------------------------------------------
        # NL → SQL → validation → execution
        # ----------------------------------------------------

        pipeline_result = self.pipeline.run(question)

        if not pipeline_result.get("success", False):
            return pipeline_result

        # ----------------------------------------------------
        # Get formatted result
        # ----------------------------------------------------

        formatted_result = pipeline_result.get(
            "formatted_result"
        )

        if not isinstance(formatted_result, dict):
            formatted_result = {}

        # ----------------------------------------------------
        # If formatted result exists, use it as the
        # authoritative source for visualization.
        # ----------------------------------------------------

        columns = formatted_result.get(
            "columns",
            pipeline_result.get("columns", []),
        )

        rows = formatted_result.get(
            "rows",
            pipeline_result.get("rows", []),
        )

        row_count = formatted_result.get(
            "row_count",
            len(rows),
        )

        execution_time_ms = formatted_result.get(
            "execution_time_ms",
            pipeline_result.get(
                "execution_time_ms",
                0.0,
            ),
        )

        # ----------------------------------------------------
        # Build formatted result if pipeline did not provide it
        # ----------------------------------------------------

        if not formatted_result and columns:
            formatted_result = self.result_formatter.format(
                columns=columns,
                rows=rows,
                row_count=row_count,
                execution_time_ms=execution_time_ms,
            )

        # ----------------------------------------------------
        # CHART DATA
        #
        # This is the important fix.
        #
        # Never depend only on pipeline_result["chart_data"].
        # Generate it from the actual formatted SQL result.
        # ----------------------------------------------------

        chart_data = formatted_result.get(
            "chart_data"
        )

        if not isinstance(chart_data, dict):
            chart_data = {}

        if not chart_data.get("supported", False):
            chart_data = self.result_formatter.get_chart_data(
                formatted_result
            )

        # ----------------------------------------------------
        # Visualization selection
        # ----------------------------------------------------

        visualization = pipeline_result.get(
            "visualization",
            {},
        )

        if not isinstance(visualization, dict):
            visualization = {}

        # Keep the existing selector available without making
        # visualization a hard dependency for chart rendering.
        if not visualization:
            try:
                visualization = self.visualization_selector.select(
                    formatted_result
                )
            except (AttributeError, TypeError):
                visualization = {}

        # ----------------------------------------------------
        # Business insights
        # ----------------------------------------------------

        insights = self.insight_engine.generate(
            question=question,
            result={
                **pipeline_result,
                "formatted_result": formatted_result,
                "columns": columns,
                "rows": rows,
                "chart_data": chart_data,
            },
        )

        # ----------------------------------------------------
        # IMPORTANT:
        # Flatten the result for the Streamlit UI.
        # ----------------------------------------------------

        return {
            **pipeline_result,

            "success": True,

            "formatted_result": formatted_result,

            "columns": columns,
            "rows": rows,

            "row_count": row_count,
            "execution_time_ms": execution_time_ms,

            "chart_data": chart_data,

            "visualization": visualization,

            "insights": insights,
        }

    def execute_query(
        self,
        question: str,
    ) -> dict:
        """Backward-compatible alias."""

        return self.execute(question)
