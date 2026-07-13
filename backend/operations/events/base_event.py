from __future__ import annotations

from dataclasses import dataclass

from backend.execution.events.metadata import EventMetadata


@dataclass(
    frozen=True,
    slots=True,
)
class OperationsEvent:
    """
    Root immutable event published by the
    Operations bounded context.
    """

    metadata: EventMetadata


@dataclass(
    frozen=True,
    slots=True,
)
class CaseEvent(OperationsEvent):
    """
    Base class for all Optimization Case events.
    """


@dataclass(
    frozen=True,
    slots=True,
)
class VerificationEvent(OperationsEvent):
    """
    Base class for all Verification events.
    """


@dataclass(
    frozen=True,
    slots=True,
)
class OperationalAssessmentEvent(OperationsEvent):
    """
    Base class for all Operational Assessment events.
    """


@dataclass(
    frozen=True,
    slots=True,
)
class MonitoringEvent(OperationsEvent):
    """
    Base class for all Monitoring events.
    """