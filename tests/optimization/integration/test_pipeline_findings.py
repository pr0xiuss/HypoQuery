from backend.execution.contracts.context import PipelineContext
from backend.execution.contracts.execution import PipelineExecution
from backend.execution.contracts.job import PipelineJob
from tests.execution.test_pipeline_executor import (
    build_executor,
)
from backend.optimization.pipeline.optimization_pipeline_builder import (
    OptimizationPipelineBuilder,
)
from backend.optimization.analysis.models.finding_collection import (
    FindingCollection,
)
from uuid import uuid4
from backend.ingestion.models.query import Query


def test_pipeline_findings(db_connection):

    connection = db_connection

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
        WHERE customer_id = 1;
        """,
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
        query,
    )
    executor = build_executor()
    executor.execute(
        pipeline,
        execution,
    )
    assert execution.state.analysis_result is not None
    assert isinstance(
        execution.state.analysis_result.findings,
        FindingCollection,
    )
    connection.close()