from __future__ import annotations

from backend.knowledge.projection.builders.base_relationship_builder import (
    RelationshipBuilder,
)
from backend.optimization.analysis.models.finding import Finding


class FindingRelationshipBuilder(RelationshipBuilder):
    """
    Builds graph relationships originating from Findings.

    Phase 5 Module 1 intentionally produces no relationships.

    Relationships will be introduced incrementally as additional
    projectors (Recommendation, Validation, Strategy, etc.)
    are implemented.
    """

    def build(
        self,
        finding: Finding,
        **kwargs,
    ) -> list:

        return []