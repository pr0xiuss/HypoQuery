from __future__ import annotations

from backend.execution.contracts.execution import PipelineExecution
from backend.execution.contracts.node_result import NodeResult
from backend.execution.pipeline.base_node import PipelineNode
from backend.optimization.collectors.explain_collector import ExplainCollector


class ExplainCollectNode(PipelineNode):
    """
    Executes EXPLAIN ANALYZE for the current query.
    """

    def __init__(self, collector: ExplainCollector,) -> None:

        self._collector = collector

    @property
    def name(self) -> str:
        return "explain_collect"

    def execute(
        self,
        execution: PipelineExecution,
    ) -> NodeResult:

        query = execution.state.artifacts.get("query")

        if query is None:
            return NodeResult.failure(
                "No query found."
            )

        report = self._collector.collect(query)

        execution.state.add_artifact(
            "execution_report",
            report,
        )

        return NodeResult.success()