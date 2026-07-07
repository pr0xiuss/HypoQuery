from backend.optimization.reporting.formatters.enum_formatter import (
    EnumFormatter,
)
from backend.optimization.reporting.formatters.report_formatter import (
    ReportFormatter,
)
from backend.optimization.reporting.formatters.value_formatter import (
    ValueFormatter,
)
from backend.optimization.reporting.models.optimization_report import (
    OptimizationReport,
)
from backend.optimization.reporting.models.report_summary import (
    ReportSummary,
)
from backend.optimization.reporting.renderers.console_renderer import (
    ConsoleRenderer,
)


def test_render():

    renderer = ConsoleRenderer(
        ReportFormatter(
            ValueFormatter(),
            EnumFormatter(),
        )
    )

    report = OptimizationReport(
        summary=ReportSummary(
            has_recommendations=True,
            total_strategies=2,
            total_recommendations=4,
            validated_recommendations=3,
            estimated_improvement_percent=80,
            highest_strategy_score=95,
        ),
    )

    output = renderer.render(
        report,
    )

    assert "Optimization Report" in output

    assert "Strategies" in output

    assert "Recommendations" in output

    assert "80.0%" in output