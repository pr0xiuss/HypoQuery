from __future__ import annotations

import json

from backend.execution.contracts.events.base import (
    ExecutionEvent,
)

from backend.observability.persistence.event_serializer import (
    EventSerializer,
)


class EventRepository:
    """
    Persists execution events.
    """

    def __init__(
        self,
        connection,
        serializer: EventSerializer,
    ) -> None:
        self._connection = connection
        self._serializer = serializer

    def save(
        self,
        event: ExecutionEvent,
    ) -> None:

        payload = self._serializer.serialize(
            event,
        )

        with self._connection.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO execution_events (
                    event_id,
                    execution_id,
                    trace_id,
                    event_type,
                    event_version,
                    occurred_at,
                    payload
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s::jsonb
                )
                """,
                (
                    str(event.metadata.event_id),
                    str(event.metadata.execution_id),
                    str(event.metadata.trace_id),
                    event.__class__.__name__,
                    event.metadata.event_version.value,
                    event.metadata.timestamp,
                    json.dumps(payload),
                ),
            )

        self._connection.commit()