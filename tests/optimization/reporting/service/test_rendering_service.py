from backend.optimization.reporting.models.optimization_report import (
    OptimizationReport,
)
from backend.optimization.reporting.models.report_summary import (
    ReportSummary,
)
from backend.optimization.reporting.registry import (
    RendererRegistry,
)
from backend.optimization.reporting.renderers.base_renderer import (
    ReportRenderer,
)
from backend.optimization.reporting.rendering_service import (
    RenderingService,
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

        return "rendered"


def test_render():

    registry = RendererRegistry()

    registry.register(
        DummyRenderer(),
    )

    service = RenderingService(
        registry,
    )

    report = OptimizationReport(
        summary=ReportSummary(),
    )

    assert (
        service.render(
            report,
            "dummy",
        )
        == "rendered"
    )

    assert (
        service.supported_formats()
        == ("dummy",)
    )