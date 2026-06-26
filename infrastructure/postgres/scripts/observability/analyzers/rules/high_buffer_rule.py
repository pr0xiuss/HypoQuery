from infrastructure.postgres.scripts.observability.analyzers.rules.base_rule import (
    BaseRule,
)
from infrastructure.postgres.scripts.observability.models.optimization_finding import (
    OptimizationFinding,
)


class HighBufferRule(BaseRule):

    def check(self, plan):

        if plan.shared_read_blocks <= 100:
            return []

        return [
            OptimizationFinding(
                issue="High Disk Reads",
                severity="MEDIUM",
                recommendation=(
                    "Investigate cache efficiency or indexes."
                ),
            )
        ]