from __future__ import annotations

from backend.execution.contracts.execution import PipelineExecution
from backend.execution.contracts.node_result import NodeResult
from backend.execution.pipeline.base_node import PipelineNode

from backend.optimization.recommendation.context import (
    RecommendationContext,
)
from backend.optimization.recommendation.engine import (
    RecommendationEngine,
)


class RecommendationNode(PipelineNode):
    """
    Generates optimization recommendations from the
    completed AnalysisResult.
    """

    def __init__(
        self,
        engine: RecommendationEngine,
    ) -> None:

        self._engine = engine

    @property
    def name(self) -> str:
        return "recommendation"

    def execute(
        self,
        execution: PipelineExecution,
    ) -> NodeResult:

        if execution.state.analysis_result is None:
            return NodeResult.failure(
                "Analysis result missing.",
            )

        context = RecommendationContext(
            analysis_result=execution.state.analysis_result,
            normalized_sql=execution.state.normalized_sql,
            fingerprint=execution.state.fingerprint,
        )

        execution.state.recommendation_result = (
            self._engine.recommend(
                context,
            )
        )

        return NodeResult.success()