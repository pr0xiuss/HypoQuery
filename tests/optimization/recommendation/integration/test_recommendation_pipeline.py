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
from backend.execution.pipeline.executor import (
    PipelineExecutor,
)
from backend.optimization.analysis.models.analysis_result import (
    AnalysisResult,
)
from backend.optimization.analysis.models.categories import (
    FindingCategory,
)
from backend.optimization.analysis.models.finding import (
    Finding,
)
from backend.optimization.analysis.models.severity import (
    FindingSeverity,
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

    execution = PipelineExecution(
        job=PipelineJob(
            source="integration-test",
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

    result = AnalysisResult()

    result.findings.add(
        Finding(
            category=FindingCategory.EXECUTION,
            code="LARGE_TABLE_SCAN",
            title="Large Sequential Scan",
            description="Large scan.",
            severity=FindingSeverity.HIGH,
        )
    )

    execution.state.analysis_result = result

    return execution


def test_recommendation_node_generates_recommendations():

    node = RecommendationNode(
        build_recommendation_engine(),
    )

    execution = create_execution()

    result = node.execute(
        execution,
    )

    assert result.success

    recommendation_result = (
        execution.state.recommendation_result
    )

    assert recommendation_result is not None

    assert recommendation_result.total_recommendations == 1

    recommendation = list(
        recommendation_result.recommendations
    )[0]

    assert recommendation.code == "CREATE_INDEX"