"""
powerbi_export.py

Exports query results into files that can be consumed
by Power BI or Tableau.
"""

from pathlib import Path
from typing import Any

import pandas as pd

from app.bi.dataset_builder import BIDatasetBuilder


class BIExporter:
    """
    Export query results into BI-compatible datasets.
    """

    def __init__(
        self,
        output_directory: str | Path = "exports/bi",
    ) -> None:

        self.output_directory = Path(
            output_directory
        )

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.dataset_builder = BIDatasetBuilder()

    def export_csv(
        self,
        columns: list[str],
        rows: list[dict[str, Any]],
        filename: str = "analysis_data.csv",
    ) -> Path:
        """
        Export query results as a Power BI-ready CSV file.
        """

        dataframe = self.dataset_builder.build(
            columns=columns,
            rows=rows,
        )

        output_path = (
            self.output_directory
            / filename
        )

        dataframe.to_csv(
            output_path,
            index=False,
        )

        return output_path

    def export_excel(
        self,
        columns: list[str],
        rows: list[dict[str, Any]],
        filename: str = "analysis_data.xlsx",
    ) -> Path:
        """
        Export query results as an Excel workbook.
        """

        dataframe = self.dataset_builder.build(
            columns=columns,
            rows=rows,
        )

        output_path = (
            self.output_directory
            / filename
        )

        dataframe.to_excel(
            output_path,
            index=False,
        )

        return output_path
