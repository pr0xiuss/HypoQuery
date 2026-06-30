from backend.execution.contracts.context import PipelineContext
from backend.execution.contracts.execution import PipelineExecution
from backend.execution.contracts.job import PipelineJob
from backend.execution.pipeline.executor import PipelineExecutor
from backend.optimization.pipeline.optimization_pipeline_builder import (
    OptimizationPipelineBuilder,
)
from backend.shared.db import get_connection

from backend.ingestion.models.query import Query


def test_pipeline_findings():

    connection = get_connection()

    try:

        pipeline = OptimizationPipelineBuilder(
            connection,
        ).build()

        query = Query(
            id="TEST001",
            name="Finding Test",
            category="test",
            difficulty="easy",
            expected_issue="",
            description="",
            expected_fix="",
            sql="""
            SELECT *
            FROM customers
            WHERE id = 1;
            """,
        )

        execution = PipelineExecution(
            job=PipelineJob(
                source="pytest",
                pipeline_version="1.0",
            ),
            context=PipelineContext(
                database="postgres",
                schema="public",
            ),
        )

        execution.state.add_artifact(
            "query",
            query,
        )

        executor = PipelineExecutor()

        executor.execute(
            pipeline,
            execution,
        )

        assert execution.state.findings is not None
        assert isinstance(
            execution.state.findings,
            list,
        )

    finally:

        connection.close()