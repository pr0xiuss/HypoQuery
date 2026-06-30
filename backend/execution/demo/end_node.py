from backend.execution.contracts.execution import PipelineExecution
from backend.execution.contracts.node_result import NodeResult
from backend.execution.contracts.enums import NodeStatus
from backend.execution.pipeline.base_node import PipelineNode


class EndNode(PipelineNode):

    @property
    def name(self) -> str:
        return "end"

    def execute(self, execution: PipelineExecution) -> NodeResult:

        execution.state.add_artifact("finished", True)

        return NodeResult(
            status=NodeStatus.SUCCESS,
            message="End node executed."
        )