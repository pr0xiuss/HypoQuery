from __future__ import annotations

from backend.knowledge.projection.builders.base_relationship_builder import (
    RelationshipBuilder,
)
from backend.optimization.validation.models.validation import (
    Validation,
)


class ValidationRelationshipBuilder(RelationshipBuilder):
    """
    Builds graph relationships originating from Validation.

    Relationships will be added once Recommendation and
    Validation projectors are connected together.
    """

    def build(
        self,
        validation: Validation,
        **kwargs,
    ) -> list:

        return []