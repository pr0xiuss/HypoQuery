from backend.platform.apis.discovery.extractors.base_route_extractor import (
    BaseRouteExtractor,
)
from backend.platform.apis.domain.api_framework import (
    ApiFramework,
)


class RouteExtractorRegistry:
    """
    Registry responsible for resolving the appropriate
    route extractor for a framework.
    """

    def __init__(
        self,
        extractors: dict[
            ApiFramework,
            BaseRouteExtractor,
        ],
    ) -> None:
        self._extractors = extractors

    def get(
        self,
        framework: ApiFramework,
    ) -> BaseRouteExtractor:
        try:
            return self._extractors[
                framework
            ]
        except KeyError as exc:
            raise ValueError(
                f"No extractor registered for framework: {framework.value}",
            ) from exc