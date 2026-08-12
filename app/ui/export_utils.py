"""
export_utils.py

Utilities for exporting query results.
"""

from io import StringIO
import csv


def results_to_csv(
    columns: list[str],
    rows: list[dict],
) -> str:
    """
    Convert query results into CSV text.
    """

    if not columns:
        return ""

    buffer = StringIO()

    writer = csv.DictWriter(
        buffer,
        fieldnames=columns,
        extrasaction="ignore",
    )

    writer.writeheader()
    writer.writerows(rows)

    return buffer.getvalue()