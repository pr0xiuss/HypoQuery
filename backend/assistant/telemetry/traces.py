from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from datetime import UTC
from datetime import datetime


@dataclass(slots=True)
class TraceEvent:
    """
    Represents one assistant execution.
    """

    provider: str

    operation: str

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(
            UTC,
        )
    )


class TraceCollector:
    """
    Stores assistant execution traces.
    """

    def __init__(
        self,
    ) -> None:

        self._events: list[
            TraceEvent
        ] = []

    def record(
        self,
        provider: str,
        operation: str,
    ) -> None:

        self._events.append(
            TraceEvent(
                provider=provider,
                operation=operation,
            )
        )

    @property
    def events(
        self,
    ) -> tuple[
        TraceEvent,
        ...
    ]:

        return tuple(
            self._events
        )