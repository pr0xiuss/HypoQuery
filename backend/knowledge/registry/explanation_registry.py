from __future__ import annotations

from backend.knowledge.explainers.base_explainer import (
    Explainer,
)


class ExplanationRegistry:
    """
    Registry containing every Explainer.
    """

    def __init__(
        self,
    ) -> None:

        self._explainers: list[
            Explainer
        ] = []

    def register(
        self,
        explainer: Explainer,
    ) -> None:

        self._explainers.append(
            explainer,
        )

    def all(
        self,
    ) -> tuple[
        Explainer,
        ...,
    ]:

        return tuple(
            self._explainers,
        )