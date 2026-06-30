from __future__ import annotations

from backend.execution.contracts.execution import PipelineExecution
from backend.execution.contracts.node_result import NodeResult
from backend.execution.pipeline.base_node import PipelineNode
from backend.execution.observability.services.observability_service import (
    ObservabilityService,
)


class PersistResultNode(PipelineNode):
    """
    Persists the optimization results.

    Currently delegates to the existing ObservabilityService.
    """

    def __init__(
        self,
        observability: ObservabilityService,
    ) -> None:

        self._observability = observability

    @property
    def name(self) -> str:
        return "persist_result"

    def execute(
        self,
        execution: PipelineExecution,
    ) -> NodeResult:

        query = execution.state.artifacts.get("query")

        if query is None:
            return NodeResult.failure(
                "Query missing."
            )

        try:
            plan, findings = self._observability.analyze_query(
                query
            )

            execution.state.execution_plan = plan
            execution.state.findings = findings

            return NodeResult.success()

        except Exception as exc:

            execution.state.add_error(exc)

            return NodeResult.failure(str(exc))