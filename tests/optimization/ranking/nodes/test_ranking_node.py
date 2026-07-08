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
from backend.optimization.nodes.ranking_node import (
    RankingNode,
)
from backend.optimization.ranking.context import (
    RankingContext,
)
from backend.optimization.ranking.engine import (
    RankingEngine,
)
from backend.optimization.ranking.models.ranking_result import (
    RankingResult,
)
from backend.optimization.recommendation.models.recommendation_result import (
    RecommendationResult,
)
from backend.optimization.validation.models.validation_result import (
    ValidationResult,
)


class DummyRankingEngine(
    RankingEngine,
):

    def __init__(
        self,
    ) -> None:
        pass

    def rank(
        self,
        context: RankingContext,
    ) -> RankingResult:

        return RankingResult()


def test_ranking_node():

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

    execution.state.recommendation_result = (
        RecommendationResult()
    )

    execution.state.validation_result = (
        ValidationResult()
    )

    node = RankingNode(
        DummyRankingEngine(),
    )

    result = node.execute(
        execution,
    )

    assert result.success

    assert (
        execution.state.ranking_result
        is not None
    )