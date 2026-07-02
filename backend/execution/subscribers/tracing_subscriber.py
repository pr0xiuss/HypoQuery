from collections import defaultdict
from uuid import UUID

from backend.execution.contracts.events import ExecutionEvent
from backend.execution.contracts.subscriber import Subscriber


class TracingSubscriber(Subscriber):
    """
    Maintains an in-memory execution timeline grouped by trace ID.

    Later phases will export traces to a tracing backend.
    """

    def __init__(self) -> None:
        self._traces: dict[
            UUID,
            list[ExecutionEvent],
        ] = defaultdict(list)

    def handle(
        self,
        event: ExecutionEvent,
    ) -> None:
        self._traces[
            event.metadata.trace_id
        ].append(event)

    @property
    def traces(
        self,
    ) -> dict[UUID, list[ExecutionEvent]]:
        return {
            trace_id: list(events)
            for trace_id, events in self._traces.items()
        }

    def clear(self) -> None:
        self._traces.clear()