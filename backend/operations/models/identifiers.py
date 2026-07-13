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