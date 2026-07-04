from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from backend.execution.contracts.fingerprint import QueryFingerprint
from backend.optimization.analysis.models.analysis_result import (
    AnalysisResult,
)
from backend.optimization.analysis.models.analysis_result import (
    AnalysisResult,
)


@dataclass(slots=True)
class RecommendationContext:
    """
    Published input contract for the Recommendation bounded context.

    Recommendation operates purely on AnalysisResult and never
    directly inspects execution plans.
    """

    analysis_result: AnalysisResult

    normalized_sql: str | None = None

    fingerprint: QueryFingerprint | None = None

    database_metadata: Any = None

    workload_statistics: Any = None

    configuration: Any = None