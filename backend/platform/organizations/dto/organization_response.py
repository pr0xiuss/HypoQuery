from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict


class OrganizationResponse(BaseModel):
    """
    Public representation of an organization.
    """

    id: UUID

    name: str

    slug: str

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )