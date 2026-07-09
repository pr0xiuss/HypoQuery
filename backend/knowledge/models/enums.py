from __future__ import annotations

from enum import Enum


class KnowledgeNodeType(str, Enum):
    """
    Supported knowledge entities stored inside the Knowledge Graph.
    """

    EXECUTION = "execution"
    QUERY = "query"
    FINDING = "finding"
    RECOMMENDATION = "recommendation"
    VALIDATION = "validation"
    STRATEGY = "strategy"

    DATABASE = "database"
    TABLE = "table"
    INDEX = "index"
    VIEW = "view"
    MATERIALIZED_VIEW = "materialized_view"
    PARTITION = "partition"
    FUNCTION = "function"

    HISTORICAL_OUTCOME = "historical_outcome"


class KnowledgeRelationshipType(str, Enum):
    """
    Semantic relationships within the optimization ontology.
    """

    LEADS_TO = "leads_to"

    VALIDATED_BY = "validated_by"

    CONTAINS = "contains"

    TARGETS = "targets"

    REFERENCES = "references"

    RELATED_TO = "related_to"

    PREVIOUSLY_OBSERVED = "previously_observed"