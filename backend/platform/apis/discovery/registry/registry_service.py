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
    """
    Applies synchronization plans to the
    persisted API registry.
    """

    @abstractmethod
    def apply(
        self,
        plans: list[
            SyncPlan
        ],
    ) -> SyncResult:
        """
        Applies a synchronization plan and
        returns the execution result.
        """