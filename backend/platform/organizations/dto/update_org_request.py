from pydantic import BaseModel, Field


class UpdateOrganizationRequest(BaseModel):
    """
    Request to update an organization.
    """

    name: str = Field(
        min_length=1,
        max_length=100,
    )

    description: str = Field(
        default="",
        max_length=500,
    )