from backend.optimization.reporting.registry import (
    RendererRegistry,
)
from backend.optimization.reporting.renderers.base_renderer import (
    ReportRenderer,
)
from backend.optimization.reporting.models.optimization_report import (
    OptimizationReport,
)


class DummyRenderer(
    ReportRenderer,
):

    @property
    def name(
        self,
    ) -> str:

        return "dummy"

    def render(
        self,
        report: OptimizationReport,
    ) -> str:

        return "dummy"


def test_registry():

    registry = RendererRegistry()

    renderer = DummyRenderer()

    registry.register(
        renderer,
    )

    assert (
        registry.get(
            "dummy",
        )
        is renderer
    )

    assert (
        registry.contains(
            "dummy",
        )
    )

    assert (
        registry.names()
        == ("dummy",)
    )

    assert len(
        registry,
    ) == 1