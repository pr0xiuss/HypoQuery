from uuid import uuid4

from backend.execution.contracts.execution import (
    PipelineExecution,
)
from backend.execution.contracts.job import (
    PipelineJob,
)
from backend.execution.contracts.context import (
    PipelineContext,
)
from backend.optimization.pipeline.optimization_pipeline_builder import (
    OptimizationPipelineBuilder,
)
from backend.ingestion.models.query import (
    Query,
)


def test_pipeline_produces_validation_result(
    db_connection,
):

    pipeline = (
        OptimizationPipelineBuilder(
            db_connection,
        ).build()
    )

    execution = PipelineExecution(
        job=PipelineJob(
            source="pytest",
            pipeline_version="1.0",
        ),
        context=PipelineContext(
            execution_id=uuid4(),
            trace_id=uuid4(),
            pipeline_name="optimization",
            pipeline_version="1.0",
            database="postgres",
            schema="public",
        ),
    )

    execution.state.add_artifact(
        "query",
        Query(
            id="TEST",
            name="Validation Test",
            category="test",
            difficulty="easy",
            expected_issue="",
            description="",
            expected_fix="",
            sql="SELECT 1;",
        ),
    )

    from tests.execution.test_pipeline_executor import (
        build_executor,
    )

    executor = build_executor()

    result = executor.execute(
        pipeline,
        execution,
    )

    assert result.execution.state.validation_result is not None