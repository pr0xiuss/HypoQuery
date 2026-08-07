from abc import ABC
from abc import abstractmethod

from backend.platform.apis.discovery.domain.discovered_route import (
    DiscoveredRoute,
)
from backend.platform.apis.discovery.synchronization.sync_plan import (
    SyncPlan,
)


class Synchronizer(
    ABC,
):
    """
    Compares discovered routes with the API registry
    and produces synchronization operations.
    """

    @abstractmethod
    def synchronize(
        self,
        discovered_routes: list[
            DiscoveredRoute
        ],
    ) -> list[
        SyncPlan
    ]:
        """
        Produces synchronization operations.
        """