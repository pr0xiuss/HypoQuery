from backend.optimization.analysis.parsers.predicate_parser import (
    PredicateParser,
)


def test_extract_single_column():

    parser = PredicateParser()

    columns = parser.extract_columns(
        "(customer_id = 5)",
    )

    assert columns == [
        "customer_id",
    ]


def test_extract_multiple_columns():

    parser = PredicateParser()

    columns = parser.extract_columns(
        "((customer_id = 5) AND (status = 1))",
    )

    assert columns == [
        "customer_id",
        "status",
    ]


def test_extract_join_columns():

    parser = PredicateParser()

    columns = parser.extract_columns(
        "(customer_id = order_id)",
    )

    assert columns == [
        "customer_id",
        "order_id",
    ]


def test_ignore_string_literals():

    parser = PredicateParser()

    columns = parser.extract_columns(
        "(status = 'ACTIVE')",
    )

    assert columns == [
        "status",
    ]


def test_ignore_type_casts():

    parser = PredicateParser()

    columns = parser.extract_columns(
        "((email)::text = 'abc')",
    )

    assert columns == [
        "email",
    ]


def test_ignore_function_names():

    parser = PredicateParser()

    columns = parser.extract_columns(
        "(lower(email) = 'abc')",
    )

    assert columns == [
        "email",
    ]


def test_remove_duplicates():

    parser = PredicateParser()

    columns = parser.extract_columns(
        "((customer_id = 5) OR (customer_id = 10))",
    )

    assert columns == [
        "customer_id",
    ]


def test_empty_predicate():

    parser = PredicateParser()

    assert parser.extract_columns(
        None,
    ) == []

    assert parser.extract_columns(
        "",
    ) == []