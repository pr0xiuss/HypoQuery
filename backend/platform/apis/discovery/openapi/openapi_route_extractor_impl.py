from uuid import UUID

from backend.platform.apis.discovery.domain.discovered_route import (
    DiscoveredRoute,
)
from backend.platform.apis.discovery.extractors.fastapi_route_parser import (
    FastAPIRouteParser,
)
from backend.platform.apis.discovery.openapi.openapi_route_extractor import (
    OpenAPIRouteExtractor,
)


class OpenAPIRouteExtractorImpl(
    OpenAPIRouteExtractor,
):
    """
    Converts an OpenAPI specification into
    DiscoveredRoute objects.
    """

    def __init__(
        self,
        parser: FastAPIRouteParser,
    ) -> None:
        self._parser = parser

    def extract(
        self,
        *,
        environment_id: UUID,
        specification: dict,
    ) -> list[DiscoveredRoute]:

        routes: list[DiscoveredRoute] = []

        paths = specification.get(
            "paths",
            {},
        )

        for path, operations in paths.items():

            for method, metadata in operations.items():

                routes.append(
                    self._parser.parse(
                        environment_id=environment_id,
                        method=method,
                        path=path,
                        handler=metadata.get(
                            "operationId",
                            "unknown",
                        ),
                        source_file=None,
                        line_number=0,
                    )
                )

        return routes