from backend.execution.contracts.enums import PipelineStatus
from backend.execution.contracts.context import PipelineContext
from backend.execution.contracts.execution import PipelineExecution
from backend.execution.contracts.job import PipelineJob
from backend.optimization.pipeline.optimization_pipeline_builder import (
    OptimizationPipelineBuilder,
)
from backend.shared.db import get_connection

from backend.ingestion.models.query import Query


def test_pipeline_execution():

    connection = get_connection()

    try:

        pipeline = OptimizationPipelineBuilder(
            connection,
        ).build()

        query = Query(
            id="TEST001",
            name="Pipeline Test",
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

        result = pipeline.get_node  # keeps linter happy if unused
        from backend.execution.pipeline.executor import PipelineExecutor

        executor = PipelineExecutor()

        result = executor.execute(
            pipeline,
            execution,
        )

        assert result.status == PipelineStatus.COMPLETED

    finally:

        connection.close()