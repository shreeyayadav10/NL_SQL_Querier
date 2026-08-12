import pandas as pd

from app.bi.dataset_builder import BIDatasetBuilder
from app.bi.powerbi_export import BIExporter


def test_bi_dataset_builder_creates_dataframe():

    builder = BIDatasetBuilder()

    dataframe = builder.build(
        columns=[
            "customer_state",
            "order_count",
        ],
        rows=[
            {
                "customer_state": "SP",
                "order_count": 41746,
            },
            {
                "customer_state": "RJ",
                "order_count": 12852,
            },
        ],
    )

    assert isinstance(
        dataframe,
        pd.DataFrame,
    )

    assert len(dataframe) == 2

    assert list(dataframe.columns) == [
        "customer_state",
        "order_count",
    ]


def test_bi_dataset_builder_handles_empty_result():

    builder = BIDatasetBuilder()

    dataframe = builder.build(
        columns=[],
        rows=[],
    )

    assert dataframe.empty


def test_bi_dataset_builder_normalizes_columns():

    builder = BIDatasetBuilder()

    dataframe = builder.build(
        columns=[
            "Customer State",
            "Order-Count",
        ],
        rows=[
            {
                "Customer State": "SP",
                "Order-Count": 100,
            }
        ],
    )

    assert list(dataframe.columns) == [
        "customer_state",
        "order_count",
    ]


def test_powerbi_export_creates_csv(tmp_path):

    exporter = BIExporter(
        output_directory=tmp_path,
    )

    output_path = exporter.export_csv(
        columns=[
            "customer_state",
            "order_count",
        ],
        rows=[
            {
                "customer_state": "SP",
                "order_count": 41746,
            }
        ],
    )

    assert output_path.exists()
    assert output_path.suffix == ".csv"


def test_powerbi_export_creates_excel(tmp_path):

    exporter = BIExporter(
        output_directory=tmp_path,
    )

    output_path = exporter.export_excel(
        columns=[
            "customer_state",
            "order_count",
        ],
        rows=[
            {
                "customer_state": "SP",
                "order_count": 41746,
            }
        ],
    )

    assert output_path.exists()
    assert output_path.suffix == ".xlsx"
