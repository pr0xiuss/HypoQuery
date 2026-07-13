from __future__ import annotations

from dataclasses import dataclass

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


@dataclass(
    slots=True,
)
class Verification:
    """
    Aggregate representing the deterministic
    verification of an implemented optimization.
    """

    id: VerificationId

    recommendation: RecommendationReference

    comparison: VerificationComparison

    evidence: VerificationEvidence