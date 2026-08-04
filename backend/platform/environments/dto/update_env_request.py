from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from backend.platform.environments.domain.env_type import (
    EnvironmentType,
)


class UpdateEnvironmentRequest(BaseModel):
    """
    Request payload for updating an environment.
    """

    name: str = Field(
        min_length=2,
        max_length=100,
    )

    type: EnvironmentType

    description: str | None = Field(
        default=None,
        max_length=500,
    )

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )