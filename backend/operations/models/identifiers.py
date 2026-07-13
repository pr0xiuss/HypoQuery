from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(
    frozen=True,
    slots=True,
)
class OptimizationCaseId:
    """
    Strongly typed identifier for an Optimization Case.
    """

    value: UUID


@dataclass(
    frozen=True,
    slots=True,
)
class VerificationId:
    """
    Strongly typed identifier for a Verification.
    """

    value: UUID


@dataclass(
    frozen=True,
    slots=True,
)
class OperationalAssessmentId:
    """
    Strongly typed identifier for an Operational Assessment.
    """

    value: UUID


@dataclass(
    frozen=True,
    slots=True,
)
class MonitoringFindingId:
    """
    Strongly typed identifier for a Monitoring Finding.
    """

    value: UUID

@dataclass(
    frozen=True,
    slots=True,
)
class OutcomeId:
    """
    Strongly typed identifier for an
    Outcome aggregate.
    """

    value: UUID

    def __str__(self) -> str:
        return str(
            self.value,
        )
    
@dataclass(
    frozen=True,
    slots=True,
)
class MonitoringId:
    """
    Strongly typed identifier for a
    Monitoring aggregate.
    """

    value: UUID

    def __str__(self) -> str:
        return str(
            self.value,
        )
    
@dataclass(
    frozen=True,
    slots=True,
)
class PolicyId:
    """
    Strongly typed identifier for a
    Policy aggregate.
    """

    value: UUID

    def __str__(self) -> str:
        return str(
            self.value,
        )