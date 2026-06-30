from backend.optimization.rules.base_rule import (
    BaseRule,
)
from backend.optimization.models.execution_plan import (
    ExecutionPlan,
)
from backend.optimization.models.optimization_finding import (
    OptimizationFinding,
)


class NestedLoopRule(BaseRule):

    def check(
        self,
        plan: ExecutionPlan,
    ) -> list[OptimizationFinding]:

        if plan.node_type != "Nested Loop":
            return []

        return [
            OptimizationFinding(
                issue="Nested Loop Detected",
                severity="MEDIUM",
                recommendation=(
                    "Consider indexing join columns or "
                    "using a hash join for larger datasets."
                ),
                node_type=plan.node_type,
                estimated_cost=plan.total_cost,
                estimated_rows=plan.estimated_rows,
            )
        ]
