from __future__ import annotations

from collections.abc import Iterator

from backend.optimization.models.execution_plan import ExecutionPlan


class ExecutionPlanTraverser:
    """
    Traverses an ExecutionPlan tree.

    This class centralizes traversal logic so that analysis
    rules focus only on business logic rather than tree
    navigation.
    """

    def depth_first(
        self,
        root: ExecutionPlan,
    ) -> Iterator[ExecutionPlan]:
        """
        Performs a pre-order depth-first traversal.

        Yields:
            Every node in the execution plan exactly once.
        """
        yield root

        for child in root.children:
            yield from self.depth_first(child)

    def depth_first_with_depth(
        self,
        root: ExecutionPlan,
        depth: int = 0,
    ) -> Iterator[tuple[ExecutionPlan, int]]:
        """
        Performs a pre-order depth-first traversal while
        tracking the depth of each node.
        """

        yield root, depth

        for child in root.children:
            yield from self.depth_first_with_depth(
                child,
                depth + 1,
            )