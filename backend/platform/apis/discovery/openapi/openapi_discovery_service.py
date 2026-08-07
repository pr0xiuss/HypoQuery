from abc import ABC
from abc import abstractmethod
from pathlib import Path

from backend.platform.apis.discovery.domain.discovered_route import (
    DiscoveredRoute,
)


class OpenAPIDiscoveryService(
    ABC,
):
    """
    Discovers API routes from an OpenAPI specification.
    """

    @abstractmethod
    def discover(
        self,
        specification: Path,
    ) -> list[DiscoveredRoute]:
        """
        Discovers every API route from an
        OpenAPI specification.
        """