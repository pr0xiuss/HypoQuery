from backend.execution.contracts.events import ExecutionEvent
from backend.execution.contracts.events.node import (
    NodeCompletedEvent,
    NodeFailedEvent,
    NodeStartedEvent,
)
from backend.execution.contracts.events.pipeline import (
    PipelineCompletedEvent,
    PipelineFailedEvent,
    PipelineStartedEvent,
)
from backend.execution.contracts.subscriber import Subscriber


class MetricsSubscriber(Subscriber):
    """
    Maintains in-memory execution metrics.

    Later phases will export these metrics to an external backend.
    """

    def __init__(self) -> None:
        self._metrics: dict[str, int] = {
            "pipelines_started": 0,
            "pipelines_completed": 0,
            "pipelines_failed": 0,
            "nodes_started": 0,
            "nodes_completed": 0,
            "nodes_failed": 0,
        }

    def handle(
        self,
        event: ExecutionEvent,
    ) -> None:

        if isinstance(event, PipelineStartedEvent):
            self._metrics["pipelines_started"] += 1

        elif isinstance(event, PipelineCompletedEvent):
            self._metrics["pipelines_completed"] += 1

        elif isinstance(event, PipelineFailedEvent):
            self._metrics["pipelines_failed"] += 1

        elif isinstance(event, NodeStartedEvent):
            self._metrics["nodes_started"] += 1

        elif isinstance(event, NodeCompletedEvent):
            self._metrics["nodes_completed"] += 1

        elif isinstance(event, NodeFailedEvent):
            self._metrics["nodes_failed"] += 1

    @property
    def metrics(self) -> dict[str, int]:
        return dict(self._metrics)

    def clear(self) -> None:
        for key in self._metrics:
            self._metrics[key] = 0