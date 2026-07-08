from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from backend.execution.contracts.fingerprint import QueryFingerprint


@dataclass(slots=True)
class AnalysisContext:
    """
    Published input contract for the Analysis bounded context.

    Each analysis domain consumes only the artifacts it requires.
    """

    normalized_sql: str | None = None

    fingerprint: QueryFingerprint | None = None

    execution_plan: Any | None = None

    database_metadata: Any = None

    workload_statistics: Any = None

    configuration: Any = None