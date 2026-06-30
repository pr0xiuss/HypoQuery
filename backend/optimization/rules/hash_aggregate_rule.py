from backend.optimization.rules.base_rule import (
    BaseRule,
)
from backend.optimization.models.execution_plan import (
    ExecutionPlan,
)
from backend.optimization.models.optimization_finding import (
    OptimizationFinding,
)


class HashAggregateRule(BaseRule):

    def check(
        self,
        plan: ExecutionPlan,
    ) -> list[OptimizationFinding]:

        if plan.node_type != "HashAggregate":
            return []

        return [
            OptimizationFinding(
                issue="Hash Aggregate Detected",
                severity="LOW",
                recommendation=(
                    "Review GROUP BY columns and consider "
                    "indexes if aggregation is performed "
                    "frequently."
                ),
                node_type=plan.node_type,
                estimated_cost=plan.total_cost,
                estimated_rows=plan.estimated_rows,
            )
        ]
