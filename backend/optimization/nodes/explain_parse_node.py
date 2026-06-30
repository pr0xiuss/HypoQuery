from __future__ import annotations

from backend.execution.contracts.execution import PipelineExecution
from backend.execution.contracts.node_result import NodeResult
from backend.execution.pipeline.base_node import PipelineNode
from backend.optimization.parsers.explain_parser import ExplainParser


class ExplainParseNode(PipelineNode):
    """
    Converts raw EXPLAIN JSON into an ExecutionPlan tree.
    """

    def __init__(
        self,
        parser: ExplainParser,
    ) -> None:

        self._parser = parser

    @property
    def name(self) -> str:
        return "explain_parse"

    def execute(
        self,
        execution: PipelineExecution,
    ) -> NodeResult:

        explain_json = execution.state.artifacts.get(
            "execution_report"
        )

        if explain_json is None:
            return NodeResult.failure(
                "Execution report missing."
            )

        execution.state.execution_plan = self._parser.parse(
            explain_json
        )

        return NodeResult.success()