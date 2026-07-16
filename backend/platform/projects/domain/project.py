from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict


class Project(BaseModel):
    """
    Represents a software project within an organization.
    """

    id: UUID

    organization_id: UUID

    name: str

    description: str | None = None

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )