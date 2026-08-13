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

    @abstractmethod
    def discover(
        self,
        environment_id: UUID,
        api_id: UUID,
        request: DiscoverApisRequest,
    ) -> SyncResult:
        """
        Discovers routes for a specific registered API
        and synchronizes its endpoint registry.
        """
        ...