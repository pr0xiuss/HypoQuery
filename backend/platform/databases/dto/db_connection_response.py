from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict


class DatabaseConnectionResponse(BaseModel):
    """
    Response returned after registering a database connection.
    """

    id: UUID

    environment_id: UUID

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