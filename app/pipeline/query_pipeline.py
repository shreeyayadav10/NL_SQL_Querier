"""
query_pipeline.py

Main orchestration layer for the NL-to-SQL system.

Pipeline:

Natural Language Question
        ↓
Schema Formatting
        ↓
SQL Generation
        ↓
SQL Validation
        ↓
SQL Execution
        ↓
Self-Correction (if execution/validation fails)
        ↓
Result Formatting
        ↓
Visualization Selection
        ↓
Final Response
"""

from pathlib import Path

from app.schema.schema_formatter import SchemaFormatter
from app.llm.sql_generator import SQLGenerator
from app.correction.sql_corrector import SQLCorrector
from app.validation.sql_validator import SQLValidator
from app.execution.sql_executor import SQLExecutor
from app.results.result_formatter import ResultFormatter
from app.visualization.visualization_selector import VisualizationSelector


class QueryPipeline:
    """
    Complete NL-to-SQL query pipeline.

    Converts a natural-language question into SQL,
    validates the SQL, executes it against SQLite,
    automatically corrects failed SQL when possible,
    formats the result, and selects an appropriate
    visualization.
    """

    def __init__(self) -> None:

        # ==================================================
        # 1. Build database schema context
        # ==================================================

        schema_formatter = SchemaFormatter()

        self.schema = schema_formatter.format_schema()

        # ==================================================
        # 2. Initialize SQL generator
        # ==================================================

        self.sql_generator = SQLGenerator(
            schema=self.schema
        )

        # ==================================================
        # 3. Initialize SQL validator
        # ==================================================

        self.validator = SQLValidator()

        # ==================================================
        # 4. Initialize SQL corrector
        # ==================================================

        self.sql_corrector = SQLCorrector(
            schema=self.schema
        )

        # ==================================================
        # 5. Initialize SQL executor
        # ==================================================

        database_path = Path(
            "data/sqlite/olist.db"
        )

        self.executor = SQLExecutor(
            database_path
        )

        # ==================================================
        # 6. Initialize result formatter
        # ==================================================

        self.result_formatter = ResultFormatter()

        # ==================================================
        # 7. Initialize visualization selector
        # ==================================================

        self.visualization_selector = VisualizationSelector()

        # ==================================================
        # 8. Maximum number of correction attempts
        # ==================================================

        self.max_correction_attempts = 2

    # ======================================================
    # Public pipeline
    # ======================================================

    def run(self, question: str) -> dict:
        """
        Run the complete NL-to-SQL pipeline.

        Includes automatic SQL self-correction when
        validation or execution fails.
        """

        # ==================================================
        # STEP 1 — Generate SQL
        # ==================================================

        try:
            sql = self.sql_generator.generate(
                question
            )

        except Exception as error:

            return {
                "success": False,
                "stage": "generation",
                "question": question,
                "sql": None,
                "error": str(error),
            }

        # ==================================================
        # STEP 2 — Validate SQL
        # ==================================================

        validation = self.validator.validate(
            sql
        )

        # --------------------------------------------------
        # If validation fails, try automatic correction
        # --------------------------------------------------

        correction_attempt = 0

        while (
            not validation.is_valid
            and correction_attempt < self.max_correction_attempts
        ):

            correction_attempt += 1

            try:
                corrected_sql = self.sql_corrector.correct(
                    question=question,
                    failed_sql=sql,
                    error_message=validation.error,
                )

            except Exception as error:

                return {
                    "success": False,
                    "stage": "correction",
                    "question": question,
                    "sql": sql,
                    "error": str(error),
                }

            if not corrected_sql:
                break

            sql = corrected_sql

            validation = self.validator.validate(
                sql
            )

        # --------------------------------------------------
        # Validation still failed
        # --------------------------------------------------

        if not validation.is_valid:

            return {
                "success": False,
                "stage": "validation",
                "question": question,
                "sql": sql,
                "error": validation.error,
            }

        # ==================================================
        # STEP 3 — Execute SQL
        # ==================================================

        result = self.executor.execute(
            validation.sql
        )

        # ==================================================
        # STEP 4 — Self-correction after execution failure
        # ==================================================

        correction_attempt = 0

        while (
            not result.success
            and correction_attempt < self.max_correction_attempts
        ):

            correction_attempt += 1

            try:
                corrected_sql = self.sql_corrector.correct(
                    question=question,
                    failed_sql=validation.sql,
                    error_message=result.error or "SQL execution failed",
                )

            except Exception as error:

                return {
                    "success": False,
                    "stage": "correction",
                    "question": question,
                    "sql": validation.sql,
                    "error": str(error),
                }

            if not corrected_sql:
                break

            # ----------------------------------------------
            # Revalidate corrected SQL
            # ----------------------------------------------

            corrected_validation = self.validator.validate(
                corrected_sql
            )

            if not corrected_validation.is_valid:

                validation = corrected_validation
                result = None

                continue

            # ----------------------------------------------
            # Execute corrected SQL
            # ----------------------------------------------

            validation = corrected_validation

            result = self.executor.execute(
                validation.sql
            )

        # --------------------------------------------------
        # Execution still failed
        # --------------------------------------------------

        if result is None or not result.success:

            error_message = (
                result.error
                if result is not None
                else validation.error
            )

            return {
                "success": False,
                "stage": "execution",
                "question": question,
                "sql": validation.sql,
                "error": error_message,
            }

        # ==================================================
        # STEP 5 — Format result
        # ==================================================

        formatted_result = self.result_formatter.format(
            columns=result.columns,
            rows=result.rows,
            row_count=result.row_count,
            execution_time_ms=result.execution_time_ms,
        )

        # ==================================================
        # STEP 6 — Generate human-readable summary
        # ==================================================

        summary = self.result_formatter.get_summary(
            formatted_result
        )

        # ==================================================
        # STEP 7 — Prepare chart data
        # ==================================================

        chart_data = self.result_formatter.get_chart_data(
            formatted_result
        )

        # ==================================================
        # STEP 8 — Select visualization
        # ==================================================

        visualization = self.visualization_selector.select(
            columns=formatted_result["columns"],
            rows=formatted_result["rows"],
            result_type=formatted_result["result_type"],
        )

        # ==================================================
        # STEP 9 — Return complete response
        # ==================================================

        return {
            "success": True,
            "stage": "completed",
            "question": question,

            # ----------------------------------------------
            # SQL
            # ----------------------------------------------

            "sql": validation.sql,

            # ----------------------------------------------
            # Raw execution result
            # ----------------------------------------------

            "columns": result.columns,
            "rows": result.rows,
            "row_count": result.row_count,
            "execution_time_ms": result.execution_time_ms,

            # ----------------------------------------------
            # Formatted result
            # ----------------------------------------------

            "formatted_result": formatted_result,

            # ----------------------------------------------
            # Human-readable summary
            # ----------------------------------------------

            "summary": summary,

            # ----------------------------------------------
            # Chart-ready data
            # ----------------------------------------------

            "chart_data": chart_data,

            # ----------------------------------------------
            # Visualization recommendation
            # ----------------------------------------------

            "visualization": visualization,

            # ----------------------------------------------
            # Pipeline metadata
            # ----------------------------------------------

            "correction_attempts": correction_attempt,
        }