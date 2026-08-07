from abc import ABC
from abc import abstractmethod
from uuid import UUID

from backend.platform.apis.dto.discover_apis_request import (
    DiscoverApisRequest,
)
from backend.platform.apis.discovery.synchronization.sync_result import (
    SyncResult,
)


class DiscoveryService(
    ABC,
):
    """
    Coordinates API discovery and registry synchronization.
    """

    @abstractmethod
    def discover(
        self,
        environment_id: UUID,
        request: DiscoverApisRequest,
    ) -> SyncResult:
        """
        Discovers APIs and synchronizes the API registry.
        """