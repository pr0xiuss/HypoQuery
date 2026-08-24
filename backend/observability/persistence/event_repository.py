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

    def list_executions(self, limit: int = 100, offset: int = 0):
        # We fetch the distinct execution_ids, order by max occurred_at descending
        # Then we just return the raw payloads to be processed, or a simple grouping
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT execution_id
                FROM execution_events
                GROUP BY execution_id
                ORDER BY MAX(occurred_at) DESC
                LIMIT %s OFFSET %s
                """,
                (limit, offset)
            )
            rows = cursor.fetchall()
            if not rows:
                return []
            
            execution_ids = [row[0] for row in rows]
            
            # Now fetch all events for these executions
            cursor.execute(
                """
                SELECT event_id, execution_id, trace_id, event_type, event_version, occurred_at, payload
                FROM execution_events
                WHERE execution_id = ANY(%s)
                ORDER BY occurred_at ASC
                """,
                (execution_ids,)
            )
            event_rows = cursor.fetchall()
            
            events = []
            for r in event_rows:
                events.append({
                    "event_id": str(r[0]),
                    "execution_id": str(r[1]),
                    "trace_id": str(r[2]),
                    "event_type": r[3],
                    "event_version": r[4],
                    "occurred_at": r[5],
                    "payload": r[6]
                })
            return events

    def get_execution(self, execution_id: str):
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT event_id, execution_id, trace_id, event_type, event_version, occurred_at, payload
                FROM execution_events
                WHERE execution_id = %s
                ORDER BY occurred_at ASC
                """,
                (execution_id,)
            )
            rows = cursor.fetchall()
            
            events = []
            for r in rows:
                events.append({
                    "event_id": str(r[0]),
                    "execution_id": str(r[1]),
                    "trace_id": str(r[2]),
                    "event_type": r[3],
                    "event_version": r[4],
                    "occurred_at": r[5],
                    "payload": r[6]
                })
            return events