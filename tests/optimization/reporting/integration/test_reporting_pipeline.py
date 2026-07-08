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
from backend.execution.contracts.enums import (
    PipelineStatus,
)


def test_reporting_pipeline(
    db_connection,
):

    pipeline = (
        OptimizationPipelineBuilder(
            db_connection,
        )
        .build()
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
            id="REPORT001",
            name="Reporting Test",
            category="test",
            difficulty="easy",
            expected_issue="",
            description="",
            expected_fix="",
            sql="SELECT 1;",
        ),
    )

    executor = build_executor()

    result = executor.execute(
        pipeline,
        execution,
    )

    assert (result.status == PipelineStatus.COMPLETED)

    assert (
        execution.state.report
        is not None
    )

    assert (
        execution.state.report.summary
        is not None
    )