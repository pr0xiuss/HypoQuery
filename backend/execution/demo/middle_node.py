from backend.execution.contracts.execution import PipelineExecution
from backend.execution.contracts.node_result import NodeResult
from backend.execution.contracts.enums import NodeStatus
from backend.execution.pipeline.base_node import PipelineNode


class MiddleNode(PipelineNode):

    @property
    def name(self) -> str:
        return "middle"

    def execute(self, execution: PipelineExecution) -> NodeResult:

        counter = execution.state.artifacts.get("counter", 0)

        execution.state.add_artifact(
            "counter",
            counter + 1
        )

        return NodeResult(
            status=NodeStatus.SUCCESS,
            message="Middle node executed."
        )