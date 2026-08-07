from pathlib import Path

from backend.platform.apis.discovery.sources.discovery_source import (
    DiscoverySource,
)


class OpenAPISource(
    DiscoverySource,
):
    """
    Represents an OpenAPI specification.
    """

    def __init__(
        self,
        specification: Path,
    ) -> None:
        self._specification = specification

    @property
    def specification(
        self,
    ) -> Path:
        return self._specification

    def name(
        self,
    ) -> str:
        return "OpenAPI"