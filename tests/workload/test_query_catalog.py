from infrastructure.postgres.scripts.workload.query_catalog import (
    QueryCatalog,
)


def test_load_queries():

    queries = QueryCatalog.get_queries()

    assert len(queries) > 0


def test_query_has_sql():

    queries = QueryCatalog.get_queries()

    assert queries[0].sql.strip() != ""


def test_query_has_metadata():

    query = QueryCatalog.get_queries()[0]

    assert query.id
    assert query.name
    assert query.category