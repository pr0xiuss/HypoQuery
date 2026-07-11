from __future__ import annotations

from backend.knowledge.projection.handlers.base_handler import (
    Projector,
)


class ProjectionRegistry:
    """
    Registry containing every Knowledge Projector.
    """

    def __init__(self) -> None:
        self._projectors: list[
            Projector
        ] = []

    def register(
        self,
        projector: Projector,
    ) -> None:

        self._projectors.append(
            projector,
        )

    def all(
        self,
    ) -> tuple[
        Projector,
        ...
    ]:

        return tuple(
            self._projectors,
        )