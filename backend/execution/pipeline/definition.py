from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class NodeDefinition:
    """
    Metadata describing a pipeline node.
    """

    name: str
    version: str = "1.0"
    description: str = ""


@dataclass(frozen=True, slots=True)
class PipelineDefinition:
    """
    Immutable definition of a pipeline.
    """

    pipeline_id: str
    version: str
    description: str = ""

    nodes: tuple[NodeDefinition, ...] = field(default_factory=tuple)

    edges: dict[str, tuple[str, ...]] = field(default_factory=dict)

    entry_node: str | None = None