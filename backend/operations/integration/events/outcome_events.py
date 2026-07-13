from __future__ import annotations

from dataclasses import dataclass

from backend.operations.contracts.snapshots import (
    OutcomeSnapshot,
)


@dataclass(
    frozen=True,
    slots=True,
)
class OutcomePublished:
    """
    Published integration event emitted
    when an Outcome has been assessed.
    """

    snapshot: OutcomeSnapshot