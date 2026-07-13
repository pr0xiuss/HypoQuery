from __future__ import annotations

from backend.operations.models.identifiers import (
    VerificationId,
)
from backend.operations.models.references import (
    RecommendationReference,
)
from backend.operations.verification.models.comparison import (
    VerificationComparison,
)
from backend.operations.verification.models.evidence import (
    VerificationEvidence,
)
from backend.operations.verification.models.verification import (
    Verification,
)


class VerificationBuilder:
    """
    Fluent builder for constructing
    Verification aggregates.
    """

    def __init__(self) -> None:
        self._id: VerificationId | None = None
        self._recommendation: RecommendationReference | None = None
        self._comparison: VerificationComparison | None = None
        self._evidence: VerificationEvidence | None = None

    def with_id(
        self,
        identifier: VerificationId,
    ) -> "VerificationBuilder":
        self._id = identifier
        return self

    def with_recommendation(
        self,
        recommendation: RecommendationReference,
    ) -> "VerificationBuilder":
        self._recommendation = recommendation
        return self

    def with_comparison(
        self,
        comparison: VerificationComparison,
    ) -> "VerificationBuilder":
        self._comparison = comparison
        return self

    def with_evidence(
        self,
        evidence: VerificationEvidence,
    ) -> "VerificationBuilder":
        self._evidence = evidence
        return self

    def build(self) -> Verification:
        if self._id is None:
            raise ValueError(
                "Verification identifier is required."
            )

        if self._recommendation is None:
            raise ValueError(
                "Recommendation reference is required."
            )

        if self._comparison is None:
            raise ValueError(
                "Verification comparison is required."
            )

        if self._evidence is None:
            raise ValueError(
                "Verification evidence is required."
            )

        return Verification(
            id=self._id,
            recommendation=self._recommendation,
            comparison=self._comparison,
            evidence=self._evidence,
        )