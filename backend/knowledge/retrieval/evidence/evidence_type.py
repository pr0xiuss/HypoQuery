from __future__ import annotations

from enum import StrEnum


class EvidenceType(StrEnum):
    """
    High-level classification of retrieved evidence.
    """

    FINDING = "finding"

    RECOMMENDATION = "recommendation"

    VALIDATION = "validation"

    STRATEGY = "strategy"

    EXECUTION = "execution"

    GRAPH = "graph"