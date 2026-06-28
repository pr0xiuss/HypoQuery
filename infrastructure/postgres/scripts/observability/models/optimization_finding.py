from dataclasses import dataclass


@dataclass(slots=True)
class OptimizationFinding:

    issue: str

    severity: str

    recommendation: str

    node_type: str

    estimated_cost: float

    estimated_rows: int
