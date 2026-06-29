from infrastructure.postgres.scripts.observability.analyzers.rules.base_rule import (
    BaseRule,
)
from infrastructure.postgres.scripts.observability.models.execution_plan import (
    ExecutionPlan,
)
from infrastructure.postgres.scripts.observability.models.optimization_finding import (
    OptimizationFinding,
)


class IndexOnlyScanRule(BaseRule):

    def check(
        self,
        plan: ExecutionPlan,
    ) -> list[OptimizationFinding]:

        if plan.node_type != "Index Only Scan":
            return []

        return [
            OptimizationFinding(
                issue="Index Only Scan Detected",
                severity="INFO",
                recommendation=(
                    "Excellent execution strategy. "
                    "Ensure the visibility map remains "
                    "well maintained through regular VACUUM."
                ),
                node_type=plan.node_type,
                estimated_cost=plan.total_cost,
                estimated_rows=plan.estimated_rows,
            )
        ]
