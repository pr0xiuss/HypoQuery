from __future__ import annotations

from dataclasses import dataclass, field

from backend.optimization.history.models.execution_record import (
    ExecutionRecord,
)


@dataclass(slots=True)
class SearchResult:
    """
    Result returned from a history search.
    """

    records: list[
        ExecutionRecord
    ] = field(
        default_factory=list,
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