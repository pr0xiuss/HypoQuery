from __future__ import annotations

from backend.knowledge.retrieval.handlers.base_handler import (
    Retriever,
)


class RetrievalRegistry:
    """
    Registry containing every deterministic retriever.
    """

    def __init__(self) -> None:

        self._retrievers: list[
            Retriever
        ] = []

    def register(
        self,
        retriever: Retriever,
    ) -> None:

        self._retrievers.append(
            retriever,
        )

    def all(
        self,
    ) -> tuple[
        Retriever,
        ...
    ]:

        return tuple(
            self._retrievers,
        )