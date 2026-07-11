from backend.knowledge.projection.builders.finding_node_builder import (
    FindingNodeBuilder,
)
from backend.knowledge.projection.handlers.finding_projector import (
    FindingProjector,
)
from backend.knowledge.projection.registry.projection_registry import (
    ProjectionRegistry,
)


def test_projection_registry():

    registry = ProjectionRegistry()

    projector = FindingProjector(
        node_builder=FindingNodeBuilder(),
    )

    registry.register(
        projector,
    )

    projectors = registry.all()

    assert len(
        projectors,
    ) == 1

    assert projectors[0] is projector