from datetime import datetime


class DatabaseHealthResult:
    def __init__(
        self,
        *,
        healthy: bool,
        latency_ms: float,
        postgres_version: str | None,
        checked_at: datetime,
        error: str | None,
    ):
        self.healthy = healthy
        self.latency_ms = latency_ms
        self.postgres_version = postgres_version
        self.checked_at = checked_at
        self.error = error