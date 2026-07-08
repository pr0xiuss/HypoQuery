from __future__ import annotations

from backend.execution.contracts.execution import PipelineExecution
from backend.execution.contracts.node_result import NodeResult
from backend.execution.pipeline.base_node import PipelineNode
from backend.optimization.ranking.context import (
    RankingContext,
)
from backend.optimization.ranking.engine import (
    RankingEngine,
)


class RankingNode(PipelineNode):
    """
    Executes recommendation ranking.
    """

    def __init__(self, engine: RankingEngine,) -> None:

        self._engine = engine

    @property
    def name(self,) -> str:

        return "ranking"

    def execute(self, execution: PipelineExecution,) -> NodeResult:

        recommendation_result = (
            execution.state.recommendation_result
        )

        validation_result = (
            execution.state.validation_result
        )

        if recommendation_result is None:

            return NodeResult.failure(
                "Recommendation result is missing.",
            )

        if validation_result is None:

            return NodeResult.failure(
                "Validation result is missing.",
            )

        context = RankingContext(
            recommendation_result=recommendation_result,
            validation_result=validation_result,
            fingerprint=execution.state.fingerprint,
        )

        execution.state.ranking_result = (
            self._engine.rank(
                context,
            )
        )

        return NodeResult.success()