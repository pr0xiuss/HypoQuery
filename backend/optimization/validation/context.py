from __future__ import annotations

from dataclasses import dataclass

from psycopg import Connection

from backend.execution.contracts.fingerprint import (
    QueryFingerprint,
)
from backend.optimization.models.execution_plan import (
    ExecutionPlan,
)
from backend.optimization.recommendation.models.recommendation_result import (
    RecommendationResult,
)


@dataclass(frozen=True, slots=True)
class ValidationContext:
    """
    Immutable input supplied to the Validation bounded context.
    """

    connection: Connection

    execution_plan: ExecutionPlan

    recommendation_result: RecommendationResult

    normalized_sql: str

    fingerprint: QueryFingerprint