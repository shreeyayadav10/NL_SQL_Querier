"""
dataset_builder.py

Converts NL-SQL query results into BI-ready tabular data.
"""

from typing import Any

import pandas as pd


class BIDatasetBuilder:
    """
    Builds clean datasets suitable for Power BI, Tableau,
    CSV export, or other BI tools.
    """

    def build(
        self,
        columns: list[str],
        rows: list[dict[str, Any]],
    ) -> pd.DataFrame:
        """
        Convert query columns and rows into a pandas DataFrame.
        """

        if not columns:
            return pd.DataFrame()

        if not rows:
            return pd.DataFrame(
                columns=columns
            )

        dataframe = pd.DataFrame(
            rows,
            columns=columns,
        )

        return self._clean(dataframe)

    def _clean(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Apply basic BI-friendly cleaning.
        """

        dataframe = dataframe.copy()

        # Remove completely empty columns.
        dataframe = dataframe.dropna(
            axis=1,
            how="all",
        )

        # Normalize column names.
        dataframe.columns = [
            self._normalize_column_name(
                column
            )
            for column in dataframe.columns
        ]

        # Convert datetime-like columns when possible.
        for column in dataframe.columns:

            if (
                "date" in column.lower()
                or "timestamp" in column.lower()
            ):
                converted = pd.to_datetime(
                    dataframe[column],
                    errors="coerce",
                )

                if converted.notna().any():
                    dataframe[column] = converted

        return dataframe

    @staticmethod
    def _normalize_column_name(
        column: str,
    ) -> str:
        """
        Convert database-style column names into
        BI-friendly names.
        """

        return (
            str(column)
            .strip()
            .lower()
            .replace(" ", "_")
            .replace("-", "_")
        )
