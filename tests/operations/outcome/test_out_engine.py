from uuid import uuid4

from backend.operations.models.identifiers import (
    OutcomeId,
    VerificationId,
)
from backend.operations.outcome.engine import (
    OutcomeEngine,
)
from backend.operations.outcome.models.assessment import (
    OutcomeAssessment,
)
from backend.operations.outcome.models.evidence import (
    OutcomeEvidence,
)
from backend.operations.outcome.models.metrics import (
    OutcomeMetrics,
)
from backend.operations.outcome.models.outcome import (
    Outcome,
)
from backend.operations.outcome.repositories.memory_repository import (
    MemoryOutcomeRepository,
)
from backend.operations.verification.models.summary import (
    VerificationSummary,
)


def build_outcome() -> Outcome:
    return Outcome(
        id=OutcomeId(uuid4()),
        evidence=OutcomeEvidence(
            verification=VerificationSummary(
                id=VerificationId(uuid4()),
                verified=True,
            ),
            summary="Verification completed.",
        ),
        metrics=OutcomeMetrics(
            performance_improvement=60.0,
            storage_overhead=4.0,
            maintenance_cost=2.0,
        ),
        assessment=OutcomeAssessment(
            category="SUCCESSFUL",
            confidence=0.93,
            summary="Optimization improved performance.",
        ),
    )


def test_engine_creates_outcome() -> None:
    repository = MemoryOutcomeRepository()

    engine = OutcomeEngine(
        repository=repository,
    )

    outcome = build_outcome()

    engine.create(
        outcome,
    )

    assert engine.contains(
        outcome.id,
    )


def test_engine_finds_outcome() -> None:
    repository = MemoryOutcomeRepository()

    engine = OutcomeEngine(
        repository=repository,
    )

    outcome = build_outcome()

    engine.create(
        outcome,
    )

    assert (
        engine.find(
            outcome.id,
        )
        == outcome
    )