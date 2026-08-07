from backend.platform.apis.discovery.domain.discovered_route import (
    DiscoveredRoute,
)
from backend.platform.apis.discovery.registry.registry_mapper import (
    RegistryMapper,
)
from backend.platform.apis.dto.create_api_request import (
    CreateApiRequest,
)


class RegistryMapperImpl(
    RegistryMapper,
):
    """
    Converts discovered routes into registry DTOs.
    """

    def to_create_request(
        self,
        route: DiscoveredRoute,
    ) -> CreateApiRequest:

        return CreateApiRequest(
            name=route.handler,
            method=route.method,
            path=route.path,
            framework=route.framework,
            description=route.description,
        )