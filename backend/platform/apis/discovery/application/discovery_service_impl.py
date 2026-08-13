from pathlib import Path
from uuid import UUID

from backend.platform.apis.discovery.application.discovery_service import (
    DiscoveryService,
)
from backend.platform.apis.discovery.domain.discovery_source_type import (
    DiscoverySourceType,
)
from backend.platform.apis.discovery.openapi.openapi_discovery_service import (
    OpenAPIDiscoveryService,
)
from backend.platform.apis.discovery.registry.registry_service import (
    RegistryService,
)
from backend.platform.apis.discovery.synchronization.sync_result import (
    SyncResult,
)
from backend.platform.apis.discovery.synchronization.synchronization_service import (
    SynchronizationService,
)
from backend.platform.apis.dto.discover_apis_request import (
    DiscoverApisRequest,
)


class DiscoveryServiceImpl(
    DiscoveryService,
):
    """
    Coordinates the complete API discovery workflow
    for a specific registered API.
    """

    def __init__(
        self,
        openapi_discovery_service: OpenAPIDiscoveryService,
        synchronization_service: SynchronizationService,
        registry_service: RegistryService,
    ) -> None:
        self._openapi_discovery_service = (
            openapi_discovery_service
        )

        self._synchronization_service = (
            synchronization_service
        )

        self._registry_service = (
            registry_service
        )

    def discover(
        self,
        environment_id: UUID,
        api_id: UUID,
        request: DiscoverApisRequest,
    ) -> SyncResult:

        match request.source_type:

            case DiscoverySourceType.OPENAPI_FILE:

                routes = (
                    self._openapi_discovery_service.discover(
                        environment_id=environment_id,
                        specification=Path(request.source),
                    )
                )

            case DiscoverySourceType.OPENAPI_URL:

                raise NotImplementedError(
                    "OpenAPI URL discovery is not implemented yet.",
                )

            case DiscoverySourceType.REPOSITORY:

                raise NotImplementedError(
                    "Repository discovery is not implemented yet.",
                )

        plans = (
            self._synchronization_service.synchronize(
                environment_id=environment_id,
                api_id=api_id,
                discovered_routes=routes,
            )
        )

        return self._registry_service.apply(
            plans,
        )