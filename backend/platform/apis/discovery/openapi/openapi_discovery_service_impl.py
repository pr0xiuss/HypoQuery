from pathlib import Path
from uuid import UUID

from backend.platform.apis.discovery.domain.discovered_route import (
    DiscoveredRoute,
)
from backend.platform.apis.discovery.openapi.openapi_discovery_service import (
    OpenAPIDiscoveryService,
)
from backend.platform.apis.discovery.openapi.openapi_loader import (
    OpenAPILoader,
)
from backend.platform.apis.discovery.openapi.openapi_route_extractor import (
    OpenAPIRouteExtractor,
)


class OpenAPIDiscoveryServiceImpl(
    OpenAPIDiscoveryService,
):
    """
    Coordinates OpenAPI discovery.
    """

    def __init__(
        self,
        loader: OpenAPILoader,
        extractor: OpenAPIRouteExtractor,
    ) -> None:
        self._loader = loader
        self._extractor = extractor

    def discover(
        self,
        *,
        environment_id: UUID,
        specification: Path,
    ) -> list[DiscoveredRoute]:

        document = self._loader.load(
            specification,
        )

        return self._extractor.extract(
            environment_id=environment_id,
            specification=document,
        )