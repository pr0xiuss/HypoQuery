from pathlib import Path
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class ApiEndpoint(
    BaseModel,
):
    """
    Domain model representing a discovered HTTP endpoint
    belonging to a registered API.
    """

    id: UUID

    api_id: UUID

    method: str

    path: str

    handler: str

    source_file: Path | None = None

    line_number: int | None = None

    summary: str | None = None

    description: str | None = None

    tags: list[str] = Field(
        default_factory=list,
    )

    version: str | None = None

    authentication_required: bool = False

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )