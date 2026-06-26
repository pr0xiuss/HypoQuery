from infrastructure.postgres.scripts.observability.analyzers.rules.base_rule import (
    BaseRule,
)
from infrastructure.postgres.scripts.observability.models.optimization_finding import (
    OptimizationFinding,
)


class SeqScanRule(BaseRule):

    def check(self, plan):

        if plan.node_type != "Seq Scan":
            return []

        return [
            OptimizationFinding(
                issue="Sequential Scan Detected",
                severity="HIGH",
                recommendation=(
                    "Consider creating an index or reducing scanned rows."
                ),
            )
        ]