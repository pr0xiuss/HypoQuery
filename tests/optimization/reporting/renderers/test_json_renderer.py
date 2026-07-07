import json

from backend.optimization.reporting.models.optimization_report import (
    OptimizationReport,
)
from backend.optimization.reporting.models.report_summary import (
    ReportSummary,
)
from backend.optimization.reporting.renderers.json_renderer import (
    JsonRenderer,
)


def test_render():

    renderer = JsonRenderer()

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

    payload = json.loads(
        renderer.render(
            report,
        )
    )

    assert (
        payload["summary"]["total_strategies"]
        == 2
    )

    assert (
        payload["summary"]["total_recommendations"]
        == 4
    )

    assert (
        payload["summary"]["estimated_improvement_percent"]
        == 80
    )