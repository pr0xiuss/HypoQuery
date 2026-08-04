from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict

from backend.platform.apis.domain.api_framework import ApiFramework


class ApiResponse(
    BaseModel,
):
    id: UUID

    environment_id: UUID

    name: str

    slug: str

    description: str | None

    framework: ApiFramework

    base_url: str

    version: str | None

    is_active: bool

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        frozen=True,
        from_attributes=True,
    )