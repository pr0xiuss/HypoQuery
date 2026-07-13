from __future__ import annotations
from backend.operations.models.enums import OptimizationHealthStatus
from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class OptimizationHealth:
    """
    Current health assessment of an
    optimization.
    """

    status: OptimizationHealthStatus

    confidence: float

    summary: str