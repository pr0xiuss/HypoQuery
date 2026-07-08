from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class ExecutionMetadata:
    """
    Immutable metadata describing an optimization execution.
    """

    execution_id: UUID

    trace_id: UUID

    fingerprint: str

    normalized_sql: str

    pipeline_name: str

    pipeline_version: str

    database: str

    schema: str

    executed_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )