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
from backend.ingestion.models.query import (
    Query,
)
from backend.optimization.pipeline.optimization_pipeline_builder import (
    OptimizationPipelineBuilder,
)
from tests.execution.test_pipeline_executor import (
    build_executor,
)


def test_artifact_flow(
    db_connection,
):

    pipeline = (
        OptimizationPipelineBuilder(
            db_connection,
        ).build()
    )

    execution_id = uuid4()

    trace_id = uuid4()

    execution = PipelineExecution(
        job=PipelineJob(
            source="pytest",
            pipeline_version="1.0",
            job_id=execution_id,
            trace_id=trace_id,
        ),
        context=PipelineContext(
            execution_id=execution_id,
            trace_id=trace_id,
            pipeline_name="optimization",
            pipeline_version="1.0",
            database="postgres",
            schema="public",
        ),
    )

    execution.state.add_artifact(
        "query",
        Query(
            id="PHASE4003",
            name="Artifact Flow",
            category="test",
            difficulty="easy",
            expected_issue="",
            description="",
            expected_fix="",
            sql="SELECT 1;",
        ),
    )

    executor = build_executor()

    executor.execute(
        pipeline,
        execution,
    )

    assert execution.state.normalized_sql

    assert execution.state.fingerprint

    assert execution.state.execution_plan is not None

    assert (
        execution.state.recommendation_result
        is not None
    )

    assert (
        execution.state.validation_result
        is not None
    )

    assert (
        execution.state.ranking_result
        is not None
    )

    assert (
        execution.state.strategy_result
        is not None
    )

    assert (
        execution.state.report
        is not None
    )

    assert (
        execution.state.history_result
        is not None
    )