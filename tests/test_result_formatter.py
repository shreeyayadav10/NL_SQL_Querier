from app.results.result_formatter import ResultFormatter


def test_scalar_result():
    formatter = ResultFormatter()

    result = formatter.format(
        columns=['order_count'],
        rows=[{'order_count': 54011}],
        row_count=1,
        execution_time_ms=4.03,
    )

    assert result['result_type'] == 'scalar'
    assert result['has_results'] is True
    assert result['row_count'] == 1


def test_table_result():
    formatter = ResultFormatter()

    result = formatter.format(
        columns=['customer_state', 'order_count'],
        rows=[
            {'customer_state': 'SP', 'order_count': 41746},
            {'customer_state': 'RJ', 'order_count': 12852},
            {'customer_state': 'MG', 'order_count': 11635},
        ],
        row_count=3,
        execution_time_ms=7.42,
    )

    assert result['result_type'] == 'table'
    assert result['has_results'] is True
    assert result['row_count'] == 3


def test_chart_data():
    formatter = ResultFormatter()

    result = formatter.format(
        columns=['customer_state', 'order_count'],
        rows=[
            {'customer_state': 'SP', 'order_count': 41746},
            {'customer_state': 'RJ', 'order_count': 12852},
            {'customer_state': 'MG', 'order_count': 11635},
        ],
        row_count=3,
        execution_time_ms=7.42,
    )

    chart_data = formatter.get_chart_data(result)

    assert chart_data['supported'] is True
    assert chart_data['x_column'] == 'customer_state'
    assert chart_data['y_column'] == 'order_count'


def test_empty_result():
    formatter = ResultFormatter()

    result = formatter.format(
        columns=[],
        rows=[],
        row_count=0,
        execution_time_ms=2.10,
    )

    assert result['result_type'] == 'empty'
    assert result['has_results'] is False
