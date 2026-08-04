from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class CreateOrganizationRequest(BaseModel):
    """
    Request payload for creating an organization.
    """

    name: str = Field(
        min_length=2,
        max_length=100,
    )

    description: str | None

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )