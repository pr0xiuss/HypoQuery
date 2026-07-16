from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class CreateEnvironmentRequest(BaseModel):
    """
    Request payload for creating an environment.
    """

    name: str = Field(
        min_length=2,
        max_length=100,
    )

    description: str | None = Field(
        default=None,
        max_length=500,
    )

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )