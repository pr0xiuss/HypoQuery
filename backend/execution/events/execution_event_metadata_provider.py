from collections import defaultdict
from datetime import UTC, datetime
from uuid import UUID, uuid4

from backend.execution.contracts.execution import PipelineExecution
from backend.execution.contracts.events.enums import EventVersion
from backend.execution.events.metadata import EventMetadata
from backend.execution.events.version import CURRENT_EVENT_VERSION


class ExecutionEventMetadataProvider:
    """
    Creates immutable metadata for execution events.
    """

    def __init__(self) -> None:
        self._sequence_numbers: dict[UUID, int] = defaultdict(int)

    def create(
        self,
        execution: PipelineExecution,
    ) -> EventMetadata:
        execution_id = execution.context.execution_id
        trace_id = execution.context.trace_id

        self._sequence_numbers[execution_id] += 1

        return EventMetadata(
            event_id=uuid4(),
            execution_id=execution_id,
            trace_id=trace_id,
            sequence_number=self._sequence_numbers[execution_id],
            timestamp=datetime.now(UTC),
            event_version=CURRENT_EVENT_VERSION,
        )

    def reset(
        self,
        execution_id: UUID,
    ) -> None:
        self._sequence_numbers.pop(execution_id, None)