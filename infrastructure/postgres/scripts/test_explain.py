from infrastructure.postgres.scripts.common.db import get_connection
from infrastructure.postgres.scripts.models.enums import (
    Difficulty,
    ExpectedIssue,
    QueryCategory,
)
from infrastructure.postgres.scripts.models.query import Query
from infrastructure.postgres.scripts.observability.services.optimization_pipeline_service import (
    OptimizationPipelineService,
)


def main():

    connection = get_connection()

    service = OptimizationPipelineService(connection)

    query = Query(
        id="TEST001",
        name="Explain Test",
        category=QueryCategory.SEQUENTIAL_SCAN,
        difficulty=Difficulty.EASY,
        expected_issue=ExpectedIssue.SEQUENTIAL_SCAN,
        sql="""
        SELECT *
        FROM products;
        """,
    )

    plan, findings = service.optimize(query)

    print(plan)

    print()

    for finding in findings:
        print(finding)

    connection.close()


if __name__ == "__main__":
    main()