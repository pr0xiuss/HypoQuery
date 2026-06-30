from backend.optimization.rules.base_rule import (
    BaseRule,
)
from backend.optimization.models.execution_plan import (
    ExecutionPlan,
)
from backend.optimization.models.optimization_finding import (
    OptimizationFinding,
)


class SortRule(BaseRule):

    def check(
        self,
        plan: ExecutionPlan,
    ) -> list[OptimizationFinding]:

        if plan.node_type != "Sort":
            return []

        return [
            OptimizationFinding(
                issue="Sort Operation Detected",
                severity="MEDIUM",
                recommendation=(
                    "Consider adding an index on the "
                    "ORDER BY columns or reducing the "
                    "number of rows being sorted."
                ),
                node_type=plan.node_type,
                estimated_cost=plan.total_cost,
                estimated_rows=plan.estimated_rows,
            )
        ]
