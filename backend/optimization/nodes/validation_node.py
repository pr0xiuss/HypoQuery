from __future__ import annotations

from backend.execution.contracts.execution import PipelineExecution
from backend.execution.contracts.node_result import NodeResult
from backend.execution.pipeline.base_node import PipelineNode
from backend.optimization.validation.context import ValidationContext
from backend.optimization.validation.engine import ValidationEngine


class ValidationNode(PipelineNode):
    """
    Executes recommendation validation.
    """

    def __init__(self, engine: ValidationEngine,) -> None:

        self._engine = engine

    @property
    def name(self,) -> str:

        return "validation"

    def execute(self, execution: PipelineExecution,) -> NodeResult:

        recommendation_result = (
            execution.state.recommendation_result
        )

        execution_plan = (
            execution.state.execution_plan
        )

        if recommendation_result is None:

            return NodeResult.failure(
                "Recommendation result is missing.",
            )

        if execution_plan is None:

            return NodeResult.failure(
                "Execution plan is missing.",
            )

        context = ValidationContext(
            execution_plan=execution_plan,
            recommendation_result=recommendation_result,
            normalized_sql=execution.state.normalized_sql,
            fingerprint=execution.state.fingerprint,
        )

        execution.state.validation_result = (
            self._engine.validate(
                context,
            )
        )

        return NodeResult.success()