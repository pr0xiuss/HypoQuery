from abc import ABC
from abc import abstractmethod

from backend.platform.apis.discovery.domain.discovered_route import (
    DiscoveredRoute,
)
from backend.platform.apis.dto.create_api_endpoint_request import (
    CreateApiEndpointRequest,
)


class RegistryMapper(
    ABC,
):

    @abstractmethod
    def to_create_endpoint_request(
        self,
        route: DiscoveredRoute,
    ) -> CreateApiEndpointRequest:
        """
        Maps a discovered route to an endpoint creation request.
        """
        ...