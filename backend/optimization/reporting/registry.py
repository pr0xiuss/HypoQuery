from __future__ import annotations

from backend.optimization.reporting.renderers.base_renderer import ReportRenderer


class RendererRegistry:
    """
    Registry of available report renderers.
    """

    def __init__(self) -> None:

        self._renderers: dict[
            str,
            ReportRenderer,
        ] = {}

    def register(self, renderer: ReportRenderer) -> None:

        self._renderers[
            renderer.name
        ] = renderer

    def get(self, name: str,) -> ReportRenderer:

        try:

            return self._renderers[
                name
            ]

        except KeyError as error:

            raise LookupError(
                f"Unknown renderer '{name}'."
            ) from error

    def contains(self, name: str,) -> bool:

        return (
            name in self._renderers
        )

    def names(self,) -> tuple[str, ...]:

        return tuple(
            self._renderers.keys(),
        )

    def __iter__(self,):

        return iter(
            self._renderers.values(),
        )

    def __len__(self,) -> int:

        return len(
            self._renderers,
        )