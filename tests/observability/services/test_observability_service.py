from infrastructure.postgres.scripts.common.db import (
    get_connection,
)
from infrastructure.postgres.scripts.observability.services.observability_service import (
    ObservabilityService,
)
from infrastructure.postgres.scripts.workload.query_catalog import (
    QueryCatalog,
)


def test_analyze_query():

    connection = get_connection()

    try:

        service = ObservabilityService(connection)

        query = QueryCatalog.get_queries()[0]

        plan, findings = service.analyze_query(query)

        assert plan is not None
        assert plan.node_type != ""
        assert isinstance(findings, list)

    finally:
        connection.close()