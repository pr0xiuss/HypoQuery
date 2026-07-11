from __future__ import annotations

from enum import StrEnum


class RetrievalScope(StrEnum):
    """
    Defines the portion of the Knowledge Graph that
    may be searched.

    The scope allows retrieval to remain deterministic
    and bounded.
    """

    LOCAL = "local"

    NEIGHBOURHOOD = "neighbourhood"

    STRATEGY = "strategy"

    EXECUTION = "execution"

    GLOBAL = "global"