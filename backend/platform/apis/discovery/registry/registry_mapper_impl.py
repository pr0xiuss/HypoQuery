from backend.platform.apis.discovery.domain.discovered_route import (
    DiscoveredRoute,
)
from backend.platform.apis.discovery.registry.registry_mapper import (
    RegistryMapper,
)
from backend.platform.apis.dto.create_api_endpoint_request import (
    CreateApiEndpointRequest,
)


class RegistryMapperImpl(
    RegistryMapper,
):
    """
    Maps discovered routes to API endpoint requests.
    """

    def to_create_endpoint_request(
        self,
        route: DiscoveredRoute,
    ) -> CreateApiEndpointRequest:

        return CreateApiEndpointRequest(
            method=route.method,
            path=route.path,
            handler=route.handler,
            description=route.description,
        )