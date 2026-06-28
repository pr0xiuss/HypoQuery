from infrastructure.postgres.scripts.observability.analyzers.rules.base_rule import (
    BaseRule,
)
from infrastructure.postgres.scripts.observability.models.execution_plan import (
    ExecutionPlan,
)
from infrastructure.postgres.scripts.observability.models.optimization_finding import (
    OptimizationFinding,
)


class HashJoinRule(BaseRule):

    def check(
        self,
        plan: ExecutionPlan,
    ) -> list[OptimizationFinding]:

        if plan.node_type != "Hash Join":
            return []

        return [
            OptimizationFinding(
                issue="Hash Join Detected",
                severity="LOW",
                recommendation=(
                    "Verify join columns are indexed and "
                    "ensure hash joins are appropriate for "
                    "the dataset size."
                ),
                node_type=plan.node_type,
                estimated_cost=plan.total_cost,
                estimated_rows=plan.estimated_rows,
            )
        ]