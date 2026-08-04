from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict


class ProjectResponse(BaseModel):
    """
    Public representation of a project.
    """

    id: UUID

    organization_id: UUID

    name: str

    description: str | None = None

    slug: str

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )