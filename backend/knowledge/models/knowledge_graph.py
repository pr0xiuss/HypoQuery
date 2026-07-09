from __future__ import annotations

from dataclasses import dataclass, field

from backend.knowledge.models.enums import KnowledgeNodeType, KnowledgeRelationshipType
from backend.knowledge.models.knowledge_node import (
    KnowledgeNode,
)
from backend.knowledge.models.knowledge_relationship import (
    KnowledgeRelationship,
)
from backend.knowledge.models.node_key import (
    NodeKey,
)
from backend.knowledge.models.relationship_key import (
    RelationshipKey,
)


@dataclass(slots=True)
class KnowledgeGraph:
    """
    Aggregate root representing the complete optimization
    knowledge graph.

    The graph owns topology.

    Nodes never own neighbours.
    Relationships never own the graph.
    """

    nodes: dict[
        NodeKey,
        KnowledgeNode,
    ] = field(
        default_factory=dict,
    )

    relationships: dict[
        RelationshipKey,
        KnowledgeRelationship,
    ] = field(
        default_factory=dict,
    )

    def add_node(
        self,
        node: KnowledgeNode,
    ) -> None:

        self.nodes[node.key] = node

    def add_relationship(
        self,
        relationship: KnowledgeRelationship,
    ) -> None:

        self.relationships[
            relationship.key
        ] = relationship

    def contains_node(
        self,
        key: NodeKey,
    ) -> bool:

        return key in self.nodes

    def contains_relationship(
        self,
        key: RelationshipKey,
    ) -> bool:

        return key in self.relationships
    
    def node(
        self,
        key: NodeKey,
    ) -> KnowledgeNode | None:

        return self.nodes.get(
            key,
        )

    def relationship(
        self,
        key: RelationshipKey,
    ) -> KnowledgeRelationship | None:

        return self.relationships.get(
            key,
        )

    def outgoing(
        self,
        source: NodeKey,
    ) -> tuple[
        KnowledgeRelationship,
        ...
    ]:

        return tuple(
            relationship
            for relationship in self.relationships.values()
            if relationship.source == source
        )

    def incoming(
        self,
        target: NodeKey,
    ) -> tuple[
        KnowledgeRelationship,
        ...
    ]:

        return tuple(
            relationship
            for relationship in self.relationships.values()
            if relationship.target == target
        )
    
    def children(
        self,
        key: NodeKey,
    ) -> tuple[
        KnowledgeNode,
        ...
    ]:

        return tuple(
            self.nodes[relationship.target]
            for relationship in self.outgoing(
                key,
            )
            if relationship.target in self.nodes
        )

    def parents(
        self,
        key: NodeKey,
    ) -> tuple[
        KnowledgeNode,
        ...
    ]:

        return tuple(
            self.nodes[relationship.source]
            for relationship in self.incoming(
                key,
            )
            if relationship.source in self.nodes
        )
    
    def node_count(
        self,
    ) -> int:

        return len(
            self.nodes,
        )

    def relationship_count(
        self,
    ) -> int:

        return len(
            self.relationships,
        )

    def is_empty(
        self,
    ) -> bool:

        return (
            not self.nodes
            and not self.relationships
        )
    
    def remove_node(
        self,
        key: NodeKey,
    ) -> None:

        self.nodes.pop(
            key,
            None,
        )

        stale_relationships = [
            relationship_key
            for relationship_key, relationship
            in self.relationships.items()
            if relationship.source == key
            or relationship.target == key
        ]

        for relationship_key in stale_relationships:

            self.relationships.pop(
                relationship_key,
                None,
            )

    def remove_relationship(
        self,
        key: RelationshipKey,
    ) -> None:

        self.relationships.pop(
            key,
            None,
        )

    def clear(
        self,
    ) -> None:

        self.nodes.clear()

        self.relationships.clear()

    def copy(
        self,
    ) -> KnowledgeGraph:

        graph = KnowledgeGraph()

        graph.nodes.update(
            self.nodes,
        )

        graph.relationships.update(
            self.relationships,
        )

        return graph
    
    def nodes_by_type(
        self,
        node_type: KnowledgeNodeType,
    ) -> tuple[
        KnowledgeNode,
        ...
    ]:

        return tuple(
            node
            for node in self.nodes.values()
            if node.type == node_type
        )

    def relationships_by_type(
        self,
        relationship_type: KnowledgeRelationshipType,
    ) -> tuple[
        KnowledgeRelationship,
        ...
    ]:

        return tuple(
            relationship
            for relationship in self.relationships.values()
            if relationship.type == relationship_type
        )
    
    def has_children(
        self,
        key: NodeKey,
    ) -> bool:

        return any(
            relationship.source == key
            for relationship
            in self.relationships.values()
        )

    def has_parents(
        self,
        key: NodeKey,
    ) -> bool:

        return any(
            relationship.target == key
            for relationship
            in self.relationships.values()
        )

    def validate_relationship(
        self,
        relationship: KnowledgeRelationship,
    ) -> None:
        """
        Ensures a relationship references existing nodes.
        """

        if not self.contains_node(
            relationship.source,
        ):
            raise ValueError(
                f"Unknown source node: {relationship.source}"
            )

        if not self.contains_node(
            relationship.target,
        ):
            raise ValueError(
                f"Unknown target node: {relationship.target}"
            )

    def connect(
        self,
        relationship: KnowledgeRelationship,
    ) -> None:
        """
        Validates and stores a semantic relationship.
        """

        self.validate_relationship(
            relationship,
        )

        self.add_relationship(
            relationship,
        )

    def neighbours(
        self,
        key: NodeKey,
    ) -> tuple[
        KnowledgeNode,
        ...
    ]:

        neighbours: dict[
            NodeKey,
            KnowledgeNode,
        ] = {}

        for node in self.children(
            key,
        ):

            neighbours[node.key] = node

        for node in self.parents(
            key,
        ):

            neighbours[node.key] = node

        return tuple(
            neighbours.values(),
        )