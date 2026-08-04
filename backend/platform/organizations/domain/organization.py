from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict


class Organization(BaseModel):
    """
    Represents an organization within the platform.
    """

    id: UUID

    name: str

    description: str | None

    slug: str

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )