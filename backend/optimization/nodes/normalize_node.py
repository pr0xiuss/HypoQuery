from __future__ import annotations

from backend.execution.contracts.execution import PipelineExecution
from backend.execution.contracts.node_result import NodeResult
from backend.execution.pipeline.base_node import PipelineNode


class NormalizeNode(PipelineNode):
    """
    Normalizes SQL before optimization.
    """

    @property
    def name(self) -> str:
        return "normalize"

    def execute(self, execution: PipelineExecution,) -> NodeResult:

        query = execution.state.artifacts.get("query")

        if query is None:
            return NodeResult.failure(
                "No query found."
            )

        execution.state.normalized_sql = " ".join(
            query.sql.split()
        )

        return NodeResult.success()