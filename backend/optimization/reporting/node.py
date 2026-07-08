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
from backend.optimization.reporting.context import (
    ReportingContext,
)
from backend.optimization.reporting.engine import (
    ReportingEngine,
)


class ReportingNode(
    PipelineNode,
):
    """
    Generates the final optimization report.
    """

    def __init__(
        self,
        engine: ReportingEngine,
    ) -> None:

        self._engine = engine

    @property
    def name(
        self,
    ) -> str:

        return "reporting"

    def execute(
        self,
        execution: PipelineExecution,
    ) -> NodeResult:

        strategy_result = (
            execution.state.strategy_result
        )

        if strategy_result is None:

            return NodeResult.failure(
                "Strategy result is missing.",
            )

        context = ReportingContext(
            strategy_result=strategy_result,
        )

        execution.state.report = (
            self._engine.generate(
                context,
            )
        )

        return NodeResult.success()