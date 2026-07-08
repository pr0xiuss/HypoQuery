from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class SearchCriteria:
    """
    Criteria used to search execution history.
    """

    execution_id: UUID | None = None

    fingerprint: str | None = None

    database: str | None = None

    schema: str | None = None

    pipeline_name: str | None = None

    minimum_improvement: float | None = None

    maximum_improvement: float | None = None

    executed_after: datetime | None = None

    executed_before: datetime | None = None