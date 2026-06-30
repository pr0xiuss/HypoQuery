from __future__ import annotations

from backend.execution.contracts.execution import PipelineExecution
from backend.execution.contracts.node_result import NodeResult
from backend.execution.pipeline.base_node import PipelineNode
from backend.optimization.analyzers.plan_analyzer import PlanAnalyzer


class PlanAnalyzeNode(PipelineNode):
    """
    Runs deterministic optimization rules.
    """

    def __init__(
        self,
        analyzer: PlanAnalyzer,
    ) -> None:

        self._analyzer = analyzer

    @property
    def name(self) -> str:
        return "plan_analyze"

    def execute(
        self,
        execution: PipelineExecution,
    ) -> NodeResult:

        if execution.state.execution_plan is None:
            return NodeResult.failure(
                "Execution plan missing."
            )

        execution.state.findings = self._analyzer.analyze(
            execution.state.execution_plan
        )

        return NodeResult.success()