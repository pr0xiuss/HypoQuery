from abc import ABC
from abc import abstractmethod

from backend.platform.apis.discovery.domain.discovered_route import (
    DiscoveredRoute,
)
from backend.platform.apis.dto.create_api_request import (
    CreateApiRequest,
)


class RegistryMapper(
    ABC,
):
    """
    Maps discovery models into API registry DTOs.
    """

    @abstractmethod
    def to_create_request(
        self,
        route: DiscoveredRoute,
    ) -> CreateApiRequest:
        """
        Converts a discovered route into a
        CreateApiRequest.
        """