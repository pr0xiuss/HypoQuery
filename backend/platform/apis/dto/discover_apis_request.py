from pydantic import BaseModel
from pydantic import ConfigDict

from backend.platform.apis.discovery.domain.discovery_source_type import (
    DiscoverySourceType,
)


class DiscoverApisRequest(
    BaseModel,
):
    """
    Request to discover APIs.
    """

    source_type: DiscoverySourceType

    source: str

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )