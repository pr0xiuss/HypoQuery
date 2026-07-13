from __future__ import annotations

from dataclasses import dataclass

from backend.operations.contracts.snapshots import (
    PolicySnapshot,
)


@dataclass(
    frozen=True,
    slots=True,
)
class PolicyEvaluated:
    """
    Published integration event emitted
    when policy evaluation completes.
    """

    snapshot: PolicySnapshot