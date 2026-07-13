from __future__ import annotations

from dataclasses import dataclass

from backend.operations.contracts.snapshots import (
    OptimizationCaseSnapshot,
)


@dataclass(
    frozen=True,
    slots=True,
)
class CaseCreated:
    """
    Published integration event emitted
    when a new Optimization Case is created.
    """

    snapshot: OptimizationCaseSnapshot