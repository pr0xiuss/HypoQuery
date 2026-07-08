from __future__ import annotations

from backend.execution.contracts.execution import PipelineExecution
from backend.execution.contracts.node_result import NodeResult
from backend.execution.pipeline.base_node import PipelineNode
from backend.optimization.analysis.context import AnalysisContext
from backend.optimization.analysis.engine import AnalysisEngine


class PlanAnalyzeNode(PipelineNode):
    """
    Integrates the Analysis bounded context into the execution pipeline.
    """

    def __init__(
        self,
        engine: AnalysisEngine,
    ) -> None:
        self._engine = engine

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

        context = AnalysisContext(
            execution_plan=execution.state.execution_plan,
        )

        execution.state.analysis_result = self._engine.analyze(
            context
        )

        return NodeResult.success(
            "Execution plan analyzed successfully."
        )