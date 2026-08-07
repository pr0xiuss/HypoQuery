from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict

from backend.platform.apis.discovery.domain.discovered_route import (
    DiscoveredRoute,
)
from backend.platform.apis.discovery.synchronization.sync_operation import (
    SyncOperation,
)


class SyncPlan(
    BaseModel,
):
    """
    Represents a synchronization action.
    """

    operation: SyncOperation

    route: DiscoveredRoute | None = None

    existing_api_id: UUID | None = None

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )