from pathlib import Path
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict


class ApiEndpointResponse(
    BaseModel,
):
    """
    API response representing a discovered HTTP endpoint.
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

    tags: list[str]

    version: str | None = None

    authentication_required: bool

    model_config = ConfigDict(
        from_attributes=True,
    )