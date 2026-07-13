from __future__ import annotations

from dataclasses import dataclass

from backend.operations.events.base_event import (
    CaseEvent,
    MonitoringEvent,
    OperationalAssessmentEvent,
    VerificationEvent,
)


@dataclass(
    frozen=True,
    slots=True,
)
class CaseCreatedEvent(CaseEvent):
    """
    Published when an Optimization Case
    is created.
    """


@dataclass(
    frozen=True,
    slots=True,
)
class CaseArchivedEvent(CaseEvent):
    """
    Published when an Optimization Case
    is archived.
    """


@dataclass(
    frozen=True,
    slots=True,
)
class OptimizationVerifiedEvent(
    VerificationEvent,
):
    """
    Published when an Optimization Case
    has been successfully verified.
    """


@dataclass(
    frozen=True,
    slots=True,
)
class OperationalAssessmentCompletedEvent(
    OperationalAssessmentEvent,
):
    """
    Published when an Operational Assessment
    has been completed.
    """


@dataclass(
    frozen=True,
    slots=True,
)
class RegressionDetectedEvent(
    MonitoringEvent,
):
    """
    Published when Monitoring determines
    that optimization value has regressed.
    """