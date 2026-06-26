from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class PipelineLog:

    run_id: int

    service_name: str

    node_name: str

    log_level: str

    message: str

    duration_ms: float | None = None

    payload: dict | None = None

    created_at: datetime | None = None