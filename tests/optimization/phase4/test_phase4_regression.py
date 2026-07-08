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


def create_execution():

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
            id="PHASE4004",
            name="Regression",
            category="test",
            difficulty="easy",
            expected_issue="",
            description="",
            expected_fix="",
            sql="SELECT 1;",
        ),
    )

    return execution


def test_phase4_regression(
    db_connection,
):

    pipeline = (
        OptimizationPipelineBuilder(
            db_connection,
        ).build()
    )

    executor = build_executor()

    first = create_execution()

    second = create_execution()

    executor.execute(
        pipeline,
        first,
    )

    executor.execute(
        pipeline,
        second,
    )

    assert (
        first.state.fingerprint
        == second.state.fingerprint
    )

    assert (
        first.state.report.summary.total_recommendations
        == second.state.report.summary.total_recommendations
    )

    assert (
        first.state.report.summary.total_strategies
        == second.state.report.summary.total_strategies
    )

    assert (
        first.state.report.summary.estimated_improvement_percent
        == second.state.report.summary.estimated_improvement_percent
    )