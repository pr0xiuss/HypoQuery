from __future__ import annotations

from backend.optimization.validation.hypopg.hypopg_client import (
    HypoPGClient,
)
from backend.optimization.validation.hypopg.hypothetical_index import (
    HypotheticalIndex,
)


class HypoPGSession:
    """
    Coordinates lifecycle of hypothetical indexes.
    """

    def __init__(
        self,
        client: HypoPGClient,
    ) -> None:

        self._client = client

    def create(
        self,
        statement: str,
    ) -> HypotheticalIndex:

        return self._client.create_index(
            statement,
        )

    def cleanup(
        self,
    ) -> None:

        self._client.reset()

    def available(
        self,
    ) -> bool:

        return self._client.extension_available()