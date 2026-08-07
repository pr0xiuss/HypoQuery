from abc import ABC
from abc import abstractmethod
from pathlib import Path

from backend.platform.apis.discovery.domain.discovered_route import (
    DiscoveredRoute,
)


class BaseRouteExtractor(
    ABC,
):
    """
    Base contract implemented by every framework
    route extractor.
    """

    @abstractmethod
    def discover(
        self,
        repository_root: Path,
    ) -> list[DiscoveredRoute]:
        """
        Discovers routes inside the repository.
        """