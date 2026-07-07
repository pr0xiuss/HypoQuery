from __future__ import annotations

from backend.optimization.reporting.models.optimization_report import (
    OptimizationReport,
)
from backend.optimization.reporting.registry import (
    RendererRegistry,
)


class RenderingService:
    """
    Facade for rendering optimization reports.
    """

    def __init__(
        self,
        registry: RendererRegistry,
    ) -> None:

        self._registry = registry

    def render(
        self,
        report: OptimizationReport,
        renderer: str,
    ) -> str:
        """
        Render an optimization report using the
        requested renderer.
        """

        return (
            self._registry
            .get(renderer)
            .render(report)
        )

    def supported_formats(
        self,
    ) -> tuple[str, ...]:
        """
        Returns all available rendering formats.
        """

        return self._registry.names()