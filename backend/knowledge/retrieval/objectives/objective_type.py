from __future__ import annotations

from enum import StrEnum


class ObjectiveType(StrEnum):
    """
    High-level retrieval objective.

    Objectives describe what knowledge the retrieval
    engine should collect.
    """

    EXPLAIN_RECOMMENDATION = "explain_recommendation"

    FIND_SIMILAR_FINDINGS = "find_similar_findings"

    FIND_VALIDATIONS = "find_validations"

    FIND_STRATEGIES = "find_strategies"

    FIND_RECOMMENDATIONS = "find_recommendations"

    GRAPH_NEIGHBOURHOOD = "graph_neighbourhood"

    CUSTOM = "custom"