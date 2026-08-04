from datetime import datetime

from pydantic import BaseModel


class DatabaseHealthResponse(BaseModel):
    healthy: bool

    latency_ms: float

    postgres_version: str | None

    checked_at: datetime

    error: str | None
