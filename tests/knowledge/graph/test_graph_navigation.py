from backend.knowledge.models.knowledge_graph import (
    KnowledgeGraph,
)
from backend.knowledge.models.node_key import (
    NodeKey,
)
from backend.knowledge.models.enums import (
    KnowledgeNodeType,
    KnowledgeRelationshipType,
)
from backend.knowledge.models.knowledge_graph import (
    KnowledgeGraph,
)
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

def test_graph_adds_node() -> None:

    graph = KnowledgeGraph()

    node = KnowledgeNode(
        key=NodeKey("finding:test"),
        type=KnowledgeNodeType.FINDING,
    )

    graph.add_node(
        node,
    )

    assert graph.contains_node(
        node.key,
    )

def test_graph_navigation():

    graph = KnowledgeGraph()

    parent = KnowledgeNode(
        key=NodeKey("parent"),
        type=KnowledgeNodeType.QUERY,
    )

    child = KnowledgeNode(
        key=NodeKey("child"),
        type=KnowledgeNodeType.FINDING,
    )

    graph.add_node(parent)
    graph.add_node(child)

    graph.connect(
        KnowledgeRelationship(
            key=RelationshipKey("parent-child"),
            type=KnowledgeRelationshipType.CONTAINS,
            source=parent.key,
            target=child.key,
        )
    )

    assert graph.children(parent.key) == (
        child,
    )

    assert graph.parents(child.key) == (
        parent,
    )

    assert graph.neighbours(parent.key) == (
        child,
    )

    assert graph.neighbours(child.key) == (
        parent,
    )