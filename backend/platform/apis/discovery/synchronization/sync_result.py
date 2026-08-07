from pydantic import BaseModel
from pydantic import ConfigDict

from backend.platform.apis.discovery.synchronization.sync_plan import (
    SyncPlan,
)


class SyncResult(
    BaseModel,
):
    """
    Represents the result of executing a
    synchronization plan.
    """

    applied: list[
        SyncPlan
    ] = []

    skipped: list[
        SyncPlan
    ] = []

    failed: list[
        SyncPlan
    ] = []

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )