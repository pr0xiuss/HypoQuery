from __future__ import annotations

from dataclasses import dataclass, field

from backend.knowledge.projection.builders.finding_node_builder import (
    FindingNodeBuilder,
)
from backend.knowledge.projection.builders.graph_snapshot_builder import (
    GraphSnapshotBuilder,
)
from backend.knowledge.projection.builders.recommendation_node_builder import (
    RecommendationNodeBuilder,
)
from backend.knowledge.projection.builders.recommendation_relationship_builder import (
    RecommendationRelationshipBuilder,
)
from backend.knowledge.projection.builders.strategy_node_builder import (
    StrategyNodeBuilder,
)
from backend.knowledge.projection.builders.strategy_relationship_builder import (
    StrategyRelationshipBuilder,
)
from backend.knowledge.projection.builders.validation_node_builder import (
    ValidationNodeBuilder,
)
from backend.knowledge.projection.builders.validation_relationship_builder import (
    ValidationRelationshipBuilder,
)
from backend.knowledge.projection.engine import ProjectionEngine
from backend.knowledge.projection.handlers.finding_projector import (
    FindingProjector,
)
from backend.knowledge.projection.handlers.recommendation_projector import (
    RecommendationProjector,
)
from backend.knowledge.projection.handlers.strategy_projector import (
    StrategyProjector,
)
from backend.knowledge.projection.handlers.validation_projector import (
    ValidationProjector,
)
from backend.knowledge.projection.registry.projection_registry import (
    ProjectionRegistry,
)


@dataclass(slots=True)
class ProjectionComposition:
    """
    Composition root for the Knowledge Projection subsystem.
    """

    projection_registry: ProjectionRegistry = field(
        default_factory=ProjectionRegistry,
    )

    snapshot_builder: GraphSnapshotBuilder = field(
        default_factory=GraphSnapshotBuilder,
    )

    engine: ProjectionEngine = field(init=False)

    def __post_init__(self) -> None:

        self.projection_registry.register(
            FindingProjector(
                node_builder=FindingNodeBuilder(),
            )
        )

        self.projection_registry.register(
            RecommendationProjector(
                node_builder=RecommendationNodeBuilder(),
                relationship_builder=RecommendationRelationshipBuilder(),
            )
        )

        self.projection_registry.register(
            ValidationProjector(
                node_builder=ValidationNodeBuilder(),
                relationship_builder=ValidationRelationshipBuilder(),
            )
        )

        self.projection_registry.register(
            StrategyProjector(
                node_builder=StrategyNodeBuilder(),
                relationship_builder=StrategyRelationshipBuilder(),
            )
        )

        self.engine = ProjectionEngine(
            registry=self.projection_registry,
        )