from __future__ import annotations

from backend.execution.pipeline.base_node import (
    PipelineNode,
)
from backend.execution.contracts.node_result import (
    NodeResult,
)
from backend.optimization.history.context import (
    HistoryContext,
)
from backend.optimization.history.engine import (
    HistoryEngine,
)


class HistoryNode(
    PipelineNode,
):
    """
    Persists completed optimization executions.
    """

    @property
    def name(
        self,
    ) -> str:

        return "history"

    def __init__(
        self,
        engine: HistoryEngine,
    ) -> None:

        self._engine = engine

    def execute(
        self,
        execution,
    ) -> NodeResult:

        report = (
            execution.state.report
        )

        history = (
            self._engine.record(
                HistoryContext(
                    execution=execution,
                    report=report,
                )
            )
        )

        execution.state.history_result = (
            history
        )

        return NodeResult.success()