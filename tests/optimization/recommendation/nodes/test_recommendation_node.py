from uuid import uuid4

from backend.execution.contracts.context import (
    PipelineContext,
)
from backend.execution.contracts.execution import (
    PipelineExecution,
)
from backend.execution.contracts.job import (
    PipelineJob,
)
from backend.execution.contracts.enums import (
    NodeStatus,
)
from backend.optimization.analysis.models.analysis_result import (
    AnalysisResult,
)
from backend.optimization.nodes.recommendation_node import (
    RecommendationNode,
)
from backend.optimization.recommendation.composition import (
    build_recommendation_engine,
)


def create_execution() -> PipelineExecution:

    execution_id = uuid4()

    trace_id = uuid4()

    return PipelineExecution(
        job=PipelineJob(
            source="unit-test",
            pipeline_version="1.0",
            job_id=execution_id,
            trace_id=trace_id,
        ),
        context=PipelineContext(
            execution_id=execution_id,
            trace_id=trace_id,
            pipeline_name="optimization",
            pipeline_version="1.0",
            database="test_db",
            schema="public",
        ),
    )


def test_recommendation_node_returns_failure_when_analysis_missing():

    node = RecommendationNode(
        build_recommendation_engine(),
    )

    execution = create_execution()

    result = node.execute(
        execution,
    )

    assert result.status == NodeStatus.FAILED


def test_recommendation_node_stores_result():

    node = RecommendationNode(
        build_recommendation_engine(),
    )

    execution = create_execution()

    execution.state.analysis_result = (
        AnalysisResult()
    )

    result = node.execute(
        execution,
    )

    assert result.status == NodeStatus.SUCCESS

    assert (
        execution.state.recommendation_result
        is not None
    )