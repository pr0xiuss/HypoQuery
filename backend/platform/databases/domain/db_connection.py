from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict


class DatabaseConnection(BaseModel):
    """
    Domain model representing a registered PostgreSQL database connection.
    """

    id: UUID

    environment_id: UUID

    password: str

    name: str

    host: str

    port: int

    database_name: str

    username: str

    ssl_enabled: bool

    is_active: bool

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )