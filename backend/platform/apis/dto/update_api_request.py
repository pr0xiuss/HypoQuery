from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from backend.platform.apis.domain.api_framework import ApiFramework


class UpdateApiRequest(
    BaseModel,
):
    name: str = Field(...)

    description: str | None = Field(default=None)

    framework: ApiFramework = Field(...)

    base_url: str = Field(...)

    version: str | None = Field(default=None)

    is_active: bool = Field(default=True)

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )