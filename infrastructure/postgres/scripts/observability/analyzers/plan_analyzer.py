from infrastructure.postgres.scripts.observability.analyzers.rules.high_buffer_rule import (
    HighBufferRule,
)
from infrastructure.postgres.scripts.observability.analyzers.rules.seq_scan_rule import (
    SeqScanRule,
)
from infrastructure.postgres.scripts.observability.analyzers.rules.temp_write_rule import (
    TempWriteRule,
)
from infrastructure.postgres.scripts.observability.models.execution_plan import (
    ExecutionPlan,
)
from infrastructure.postgres.scripts.observability.models.optimization_finding import (
    OptimizationFinding,
)


class PlanAnalyzer:

    def __init__(self):

        self.rules = [
            SeqScanRule(),
            HighBufferRule(),
            TempWriteRule(),
        ]

    def analyze(
        self,
        plan: ExecutionPlan,
    ) -> list[OptimizationFinding]:

        findings = []

        for rule in self.rules:
            findings.extend(
                rule.check(plan)
            )

        return findings