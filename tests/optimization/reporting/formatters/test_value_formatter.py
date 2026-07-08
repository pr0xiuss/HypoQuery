from backend.optimization.reporting.formatters.value_formatter import (
    ValueFormatter,
)


def test_percentage():

    formatter = ValueFormatter()

    assert (
        formatter.percentage(
            82.345,
        )
        == "82.3%"
    )


def test_score():

    formatter = ValueFormatter()

    assert (
        formatter.score(
            91.678,
        )
        == "91.7"
    )


def test_boolean():

    formatter = ValueFormatter()

    assert formatter.boolean(True) == "Yes"

    assert formatter.boolean(False) == "No"