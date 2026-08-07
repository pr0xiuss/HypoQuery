from abc import ABC
from abc import abstractmethod

from backend.platform.apis.discovery.domain.discovered_route import (
    DiscoveredRoute,
)


class OpenAPIRouteExtractor(
    ABC,
):
    """
    Extracts API routes from an OpenAPI document.
    """

    @abstractmethod
    def extract(
        self,
        specification: dict,
    ) -> list[DiscoveredRoute]:
        """
        Converts an OpenAPI specification into
        discovered routes.
        """