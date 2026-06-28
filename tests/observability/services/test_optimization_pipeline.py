from infrastructure.postgres.scripts.common.db import (
    get_connection,
)
from infrastructure.postgres.scripts.observability.services.optimization_pipeline_service import (
    OptimizationPipelineService,
)
from infrastructure.postgres.scripts.workload.query_catalog import (
    QueryCatalog,
)


def test_pipeline_execution():

    connection = get_connection()

    try:

        service = OptimizationPipelineService(connection)

        query = QueryCatalog.get_queries()[0]

        plan, findings = service.optimize(query)

        assert plan is not None
        assert plan.node_type != ""

        assert isinstance(findings, list)

    finally:
        connection.close()