from backend.optimization.analysis.traversal.execution_plan_traverser import (
    ExecutionPlanTraverser,
)
from backend.optimization.models.execution_plan import ExecutionPlan


def test_depth_first_single_node():

    root = ExecutionPlan(
        node_type="Seq Scan",
    )

    traverser = ExecutionPlanTraverser()

    nodes = list(
        traverser.depth_first(root)
    )

    assert len(nodes) == 1
    assert nodes[0].node_type == "Seq Scan"


def test_depth_first_tree():

    child1 = ExecutionPlan(
        node_type="Index Scan",
    )

    child2 = ExecutionPlan(
        node_type="Sort",
    )

    root = ExecutionPlan(
        node_type="Nested Loop",
        children=[
            child1,
            child2,
        ],
    )

    traverser = ExecutionPlanTraverser()

    nodes = list(
        traverser.depth_first(root)
    )

    assert [
        node.node_type
        for node in nodes
    ] == [
        "Nested Loop",
        "Index Scan",
        "Sort",
    ]