from datetime import datetime
from uuid import UUID
from backend.platform.environments.domain.env_type import EnvironmentType
from pydantic import BaseModel
from pydantic import ConfigDict


class EnvironmentResponse(BaseModel):
    """
    Public representation of an environment.
    """

    id: UUID

    project_id: UUID

    name: str

    description: str | None = None

    slug: str

    type: EnvironmentType

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )