from dataclasses import dataclass


@dataclass(slots=True)
class OptimizationFinding:

    issue: str

    severity: str

    recommendation: str