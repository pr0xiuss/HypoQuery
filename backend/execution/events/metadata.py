from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from backend.execution.contracts.events.enums import EventVersion
from typing import Any


@dataclass(frozen=True, slots=True)
class EventMetadata:
    """
    Immutable metadata shared by every execution event.
    """

    event_id: UUID
    execution_id: UUID
    trace_id: UUID

    sequence_number: int

    timestamp: datetime

    event_version: EventVersion
    
    metadata: dict[str, Any] = None