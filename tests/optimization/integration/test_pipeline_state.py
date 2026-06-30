from backend.execution.contracts.context import PipelineContext
from backend.execution.contracts.execution import PipelineExecution
from backend.execution.contracts.job import PipelineJob
from backend.execution.pipeline.executor import PipelineExecutor
from backend.optimization.pipeline.optimization_pipeline_builder import (
    OptimizationPipelineBuilder,
)
from backend.shared.db import get_connection

from backend.ingestion.models.query import Query


def test_pipeline_state():

    connection = get_connection()

    try:

        pipeline = OptimizationPipelineBuilder(
            connection,
        ).build()

        query = Query(
            id="TEST001",
            name="State Test",
            category="test",
            difficulty="easy",
            expected_issue="",
            description="",
            expected_fix="",
            sql="SELECT 1;",
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

        assert execution.state.normalized_sql is not None
        assert execution.state.fingerprint is not None
        assert execution.state.execution_plan is not None

    finally:

        connection.close()