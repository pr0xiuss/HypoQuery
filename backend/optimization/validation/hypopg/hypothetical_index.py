from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class HypotheticalIndex:
    """
    Domain representation of a HypoPG hypothetical index.
    """

    oid: int

    name: str

    definition: str