from dataclasses import asdict, is_dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID

from backend.execution.contracts.events.base import ExecutionEvent


class EventSerializer:
    """
    Serializes execution events into JSON-compatible dictionaries.
    """

    def serialize(
        self,
        event: ExecutionEvent,
    ) -> dict:

        return self._convert(
            asdict(event),
        )

    def _convert(
        self,
        value,
    ):
        if isinstance(value, dict):
            return {
                key: self._convert(val)
                for key, val in value.items()
            }

        if isinstance(value, list):
            return [
                self._convert(item)
                for item in value
            ]

        if isinstance(value, tuple):
            return [
                self._convert(item)
                for item in value
            ]

        if isinstance(value, UUID):
            return str(value)

        if isinstance(value, datetime):
            return value.isoformat()

        if isinstance(value, Enum):
            return value.value

        if is_dataclass(value):
            return self._convert(
                asdict(value),
            )

        return value