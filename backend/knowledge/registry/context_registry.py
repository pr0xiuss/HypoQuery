from __future__ import annotations

from backend.knowledge.builders.base_builder import (
    ContextBuilder,
)


class ContextRegistry:
    """
    Registry containing every ContextBuilder.
    """

    def __init__(
        self,
    ) -> None:

        self._builders: list[
            ContextBuilder
        ] = []

    def register(
        self,
        builder: ContextBuilder,
    ) -> None:

        self._builders.append(
            builder,
        )

    def all(
        self,
    ) -> tuple[
        ContextBuilder,
        ...,
    ]:

        return tuple(
            self._builders,
        )