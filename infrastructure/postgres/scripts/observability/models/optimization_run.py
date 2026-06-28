from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class OptimizationRun:

    trace_id: UUID

    query_signature: str

    query_type: str

    classifier_route: str

    pipeline_status: str

    retry_count: int = 0

    original_cost: float | None = None

    optimized_cost: float | None = None

    cost_improvement_percent: float | None = None

    started_at: datetime = field(default_factory=datetime.now)

    completed_at: datetime | None = None
