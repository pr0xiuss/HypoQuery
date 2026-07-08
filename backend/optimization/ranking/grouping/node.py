from __future__ import annotations

from backend.execution.contracts.execution import (
    PipelineExecution,
)
from backend.execution.contracts.node_result import (
    NodeResult,
)
from backend.execution.pipeline.base_node import (
    PipelineNode,
)
from backend.optimization.ranking.grouping.context import (
    StrategyContext,
)
from backend.optimization.ranking.grouping.engine import (
    StrategyEngine,
)


class StrategyNode(
    PipelineNode,
):
    """
    Groups ranked recommendations into optimization strategies.
    """

    def __init__(
        self,
        engine: StrategyEngine,
    ) -> None:

        self._engine = engine

    @property
    def name(
        self,
    ) -> str:

        return "strategy"

    def execute(
        self,
        execution: PipelineExecution,
    ) -> NodeResult:

        ranking_result = (
            execution.state.ranking_result
        )

        if ranking_result is None:

            return NodeResult.failure(
                "Ranking result is missing.",
            )

        context = StrategyContext(
            ranking_result=ranking_result,
        )

        execution.state.strategy_result = (
            self._engine.group(
                context,
            )
        )

        return NodeResult.success()