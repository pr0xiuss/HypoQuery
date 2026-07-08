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


def test_pipeline_contract(
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
            id="PHASE4002",
            name="Pipeline Contract",
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

    assert execution.state.recommendation_result

    assert execution.state.validation_result

    assert execution.state.ranking_result

    assert execution.state.strategy_result

    assert execution.state.report

    assert execution.state.history_result