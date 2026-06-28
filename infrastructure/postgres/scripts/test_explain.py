from infrastructure.postgres.scripts.common.db import get_connection
from infrastructure.postgres.scripts.observability.services.optimization_pipeline_service import (
    OptimizationPipelineService,
)
from infrastructure.postgres.scripts.workload.query_catalog import (
    QueryCatalog,
)


def main():

    connection = get_connection()

    service = OptimizationPipelineService(connection)

    # query = Query(
    #     id="TEST001",
    #     name="Explain Test",
    #     category=QueryCategory.SEQUENTIAL_SCAN,
    #     difficulty=Difficulty.EASY,
    #     expected_issue=ExpectedIssue.SEQUENTIAL_SCAN,
    #     description="Simple sequential scan test.",
    #     expected_fix="Create an index on frequently filtered columns.",
    #     sql="""
    #     SELECT *
    #     FROM products;
    #     """,
    # )

    query = QueryCatalog.get_query("JOIN001")

    plan, findings = service.optimize(query)

    # print(plan)

    # print()

    # for finding in findings:
    #     print(finding)

    connection.close()


if __name__ == "__main__":
    main()
