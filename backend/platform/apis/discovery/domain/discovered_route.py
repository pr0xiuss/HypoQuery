from pathlib import Path
from uuid import UUID
from pydantic import BaseModel
from pydantic import ConfigDict

from backend.platform.apis.domain.api_framework import ApiFramework


class DiscoveredRoute(
    BaseModel,
):
    """
    Canonical route representation produced by every
    framework-specific extractor.
    """
    environment_id: UUID

    framework: ApiFramework

    method: str

    path: str

    handler: str

    source_file: Path | None = None

    line_number: int | None = None

    summary: str | None = None

    description: str | None = None

    tags: list[str] = []

    version: str | None = None

    authentication_required: bool = False

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )