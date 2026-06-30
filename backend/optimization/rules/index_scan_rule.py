from backend.optimization.rules.base_rule import (
    BaseRule,
)
from backend.optimization.models.execution_plan import (
    ExecutionPlan,
)
from backend.optimization.models.optimization_finding import (
    OptimizationFinding,
)


class IndexScanRule(BaseRule):

    def check(
        self,
        plan: ExecutionPlan,
    ) -> list[OptimizationFinding]:

        if plan.node_type != "Index Scan":
            return []

        return [
            OptimizationFinding(
                issue="Index Scan Detected",
                severity="INFO",
                recommendation=(
                    "The query is already using an index. "
                    "Verify that the index remains selective "
                    "and appropriate for the workload."
                ),
                node_type=plan.node_type,
                estimated_cost=plan.total_cost,
                estimated_rows=plan.estimated_rows,
            )
        ]
