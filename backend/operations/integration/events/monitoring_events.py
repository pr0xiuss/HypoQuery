from __future__ import annotations

from dataclasses import dataclass

from backend.operations.contracts.snapshots import (
    MonitoringSnapshot,
)


@dataclass(
    frozen=True,
    slots=True,
)
class MonitoringUpdated:
    """
    Published integration event emitted
    when monitoring is updated.
    """

    snapshot: MonitoringSnapshot