from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class MonitoringBaseline:
    """
    Baseline used when evaluating
    optimization health over time.
    """

    execution_time: float

    shared_buffers: float

    planning_time: float