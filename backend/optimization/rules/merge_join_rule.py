from backend.optimization.rules.base_rule import (
    BaseRule,
)
from backend.optimization.models.execution_plan import (
    ExecutionPlan,
)
from backend.optimization.models.optimization_finding import (
    OptimizationFinding,
)


class MergeJoinRule(BaseRule):

    def check(
        self,
        plan: ExecutionPlan,
    ) -> list[OptimizationFinding]:

        if plan.node_type != "Merge Join":
            return []

        return [
            OptimizationFinding(
                issue="Merge Join Detected",
                severity="LOW",
                recommendation=(
                    "Ensure join columns are sorted or "
                    "indexed appropriately to maximize "
                    "merge join efficiency."
                ),
                node_type=plan.node_type,
                estimated_cost=plan.total_cost,
                estimated_rows=plan.estimated_rows,
            )
        ]
