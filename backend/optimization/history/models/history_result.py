from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from backend.optimization.history.models.execution_record import (
    ExecutionRecord,
)


@dataclass(slots=True)
class HistoryResult:
    """
    Published contract of the History bounded context.

    Represents the collection of persisted execution
    records produced during one history execution.
    """

    records: list[
        ExecutionRecord
    ] = field(
        default_factory=list,
    )

    started_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )

    completed_at: datetime | None = None

    metadata: dict[
        str,
        object,
    ] = field(
        default_factory=dict,
    )

    @property
    def total_records(
        self,
    ) -> int:

        return len(
            self.records,
        )

    def add(
        self,
        record: ExecutionRecord,
    ) -> None:

        self.records.append(
            record,
        )