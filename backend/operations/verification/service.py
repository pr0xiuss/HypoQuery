from __future__ import annotations

from uuid import uuid4

from backend.operations.contracts.snapshots import (
    VerificationSnapshot,
)
from backend.operations.models.identifiers import (
    VerificationId,
)
from backend.operations.models.references import (
    RecommendationReference,
)
from backend.operations.verification.builders.verification_builder import (
    VerificationBuilder,
)
from backend.operations.verification.engine import (
    VerificationEngine,
)
from backend.operations.verification.models.comparison import (
    VerificationComparison,
)
from backend.operations.verification.models.evidence import (
    VerificationEvidence,
)


class VerificationService:
    """
    Application service for Verification operations.
    """

    def __init__(
        self,
        engine: VerificationEngine,
        builder: VerificationBuilder,
    ) -> None:
        self._engine = engine
        self._builder = builder

    def create(
        self,
        *,
        recommendation: RecommendationReference,
        comparison: VerificationComparison,
        evidence: VerificationEvidence,
    ) -> VerificationSnapshot:

        verification = (
            self._builder
            .with_id(
                VerificationId(
                    uuid4(),
                )
            )
            .with_recommendation(
                recommendation,
            )
            .with_comparison(
                comparison,
            )
            .with_evidence(
                evidence,
            )
            .build()
        )

        self._engine.create(
            verification,
        )

        return VerificationSnapshot(
            verification_id=verification.id,
            verified=verification.comparison.matches,
        )