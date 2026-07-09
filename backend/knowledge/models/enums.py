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
    Controlled semantic relationships between knowledge entities.

    These relationships define the ontology of the Knowledge Graph.
    """

    GENERATED = "generated"

    OBSERVED = "observed"

    BASED_ON = "based_on"

    VALIDATES = "validates"

    CONTAINS = "contains"

    TARGETS = "targets"

    CREATES = "creates"

    REFERENCES = "references"

    RELATED_TO = "related_to"

    SIMILAR_TO = "similar_to"

    PREVIOUSLY_OBSERVED = "previously_observed"