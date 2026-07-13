from __future__ import annotations

from dataclasses import dataclass

from backend.operations.contracts.snapshots import (
    VerificationSnapshot,
)


@dataclass(
    frozen=True,
    slots=True,
)
class VerificationCompleted:
    """
    Published integration event emitted
    when verification completes.
    """

    snapshot: VerificationSnapshot