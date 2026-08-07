from backend.platform.apis.discovery.domain.discovered_route import (
    DiscoveredRoute,
)
from backend.platform.apis.discovery.synchronization.sync_operation import (
    SyncOperation,
)
from backend.platform.apis.discovery.synchronization.sync_plan import (
    SyncPlan,
)
from backend.platform.apis.discovery.synchronization.synchronizer import (
    Synchronizer,
)


class SynchronizerImpl(
    Synchronizer,
):
    """
    Temporary synchronizer implementation.

    Currently every discovered route is treated as
    a CREATE operation.

    Later this implementation will compare against
    the persisted API registry.
    """

    def synchronize(
        self,
        discovered_routes: list[
            DiscoveredRoute
        ],
    ) -> list[
        SyncPlan
    ]:

        return [
            SyncPlan(
                operation=SyncOperation.CREATE,
                route=route,
            )
            for route in discovered_routes
        ]