from abc import ABC
from abc import abstractmethod
from uuid import UUID
from backend.platform.apis.discovery.domain.discovered_route import DiscoveredRoute
from backend.platform.apis.discovery.synchronization.sync_plan import SyncPlan


class SynchronizationService(
    ABC,
):
    """
    Compares discovered routes with the API registry
    and produces a synchronization plan.
    """

    @abstractmethod
    def synchronize(
        self,
        environment_id: UUID,
        discovered_routes: list[
            DiscoveredRoute
        ],
    ) -> list[
        SyncPlan
    ]:
        """
        Produces synchronization operations.
        """