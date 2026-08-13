from abc import ABC
from abc import abstractmethod

from backend.platform.apis.discovery.synchronization.sync_plan import (
    SyncPlan,
)
from backend.platform.apis.discovery.synchronization.sync_result import (
    SyncResult,
)


class RegistryService(
    ABC,
):

    @abstractmethod
    def apply(
        self,
        plans: list[
            SyncPlan
        ],
    ) -> SyncResult:
        """
        Applies endpoint synchronization plans
        to the API endpoint registry.
        """
        ...