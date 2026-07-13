from __future__ import annotations

from dataclasses import dataclass

from backend.operations.monitoring.models.health import (
    OptimizationHealth,
)


@dataclass(
    frozen=True,
    slots=True,
)
class MonitoringFinding:
    """
    Business finding produced from
    continuous monitoring.
    """

    health: OptimizationHealth

    regression_detected: bool

    confidence: float

    summary: str