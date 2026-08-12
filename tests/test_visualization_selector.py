from app.visualization.visualization_selector import VisualizationSelector


def test_metric():
    selector = VisualizationSelector()

    result = selector.select(
        columns=["order_count"],
        rows=[
            {"order_count": 54011}
        ],
        result_type="scalar",
    )

    assert result["type"] == "metric"


def test_bar_chart():
    selector = VisualizationSelector()

    result = selector.select(
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
        result_type="table",
    )

    assert result["type"] == "bar_chart"
    assert result["x_column"] == "customer_state"
    assert result["y_column"] == "order_count"


def test_line_chart():
    selector = VisualizationSelector()

    result = selector.select(
        columns=[
            "year",
            "order_count",
        ],
        rows=[
            {
                "year": "2017",
                "order_count": 45101,
            },
            {
                "year": "2018",
                "order_count": 54011,
            },
        ],
        result_type="table",
    )

    assert result["type"] == "line_chart"
    assert result["x_column"] == "year"
    assert result["y_column"] == "order_count"


def test_generic_table():
    selector = VisualizationSelector()

    result = selector.select(
        columns=[
            "customer_state",
            "order_count",
            "average_order_value",
        ],
        rows=[
            {
                "customer_state": "SP",
                "order_count": 41746,
                "average_order_value": 125.50,
            }
        ],
        result_type="table",
    )

    assert result["type"] == "table"


def test_empty_result():
    selector = VisualizationSelector()

    result = selector.select(
        columns=[],
        rows=[],
        result_type="empty",
    )

    assert result["type"] == "empty"
