from collections import defaultdict
from datetime import datetime, timezone
from uuid import UUID, uuid4

from backend.execution.contracts.events.enums import EventVersion
from backend.execution.events.metadata import EventMetadata
from backend.execution.events.version import CURRENT_EVENT_VERSION


class EventMetadataFactory:
    def __init__(self) -> None:
        self._sequence_numbers: dict[UUID, int] = defaultdict(int)

    def create(
        self,
        execution_id: UUID,
        trace_id: UUID,
    ) -> EventMetadata:
        self._sequence_numbers[execution_id] += 1

        return EventMetadata(
            event_id=uuid4(),   # Replace with UUID7 later
            execution_id=execution_id,
            trace_id=trace_id,
            sequence_number=self._sequence_numbers[execution_id],
            timestamp=datetime.now(timezone.utc),
            event_version=CURRENT_EVENT_VERSION,
        )