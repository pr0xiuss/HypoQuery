from __future__ import annotations

from enum import StrEnum


class EvidenceSource(StrEnum):
    """
    Origin of retrieved evidence.

    Multiple retrieval mechanisms may contribute
    evidence over time.
    """

    KNOWLEDGE_GRAPH = "knowledge_graph"

    VECTOR_INDEX = "vector_index"

    SEARCH_INDEX = "search_index"

    EXECUTION_HISTORY = "execution_history"

    USER_INPUT = "user_input"