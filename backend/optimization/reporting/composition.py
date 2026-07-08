from __future__ import annotations

from backend.optimization.reporting.builders.optimization_report_builder import OptimizationReportBuilder
from backend.optimization.reporting.builders.recommendation_report_builder import RecommendationReportBuilder
from backend.optimization.reporting.builders.strategy_report_builder import StrategyReportBuilder
from backend.optimization.reporting.builders.validation_report_builder import ValidationReportBuilder
from backend.optimization.reporting.engine import ReportingEngine
from backend.optimization.reporting.formatters.enum_formatter import EnumFormatter
from backend.optimization.reporting.formatters.report_formatter import ReportFormatter
from backend.optimization.reporting.formatters.value_formatter import ValueFormatter
from backend.optimization.reporting.registry import RendererRegistry
from backend.optimization.reporting.renderers.console_renderer import ConsoleRenderer
from backend.optimization.reporting.renderers.json_renderer import JsonRenderer
from backend.optimization.reporting.renderers.markdown_renderer import MarkdownRenderer
from backend.optimization.reporting.rendering_service import RenderingService

def build_reporting_engine() -> ReportingEngine:
    """
    Builds the Reporting bounded context.
    """

    recommendation_builder = (
        RecommendationReportBuilder()
    )

    validation_builder = (
        ValidationReportBuilder()
    )

    strategy_builder = (
        StrategyReportBuilder(
            recommendation_builder,
            validation_builder,
        )
    )

    report_builder = (
        OptimizationReportBuilder(
            strategy_builder,
        )
    )

    return ReportingEngine(
        report_builder,
    )


def build_renderer_registry() -> RendererRegistry:
    """
    Builds the renderer registry.
    """

    formatter = ReportFormatter(
        ValueFormatter(),
        EnumFormatter(),
    )

    registry = RendererRegistry()

    registry.register(
        ConsoleRenderer(
            formatter,
        )
    )

    registry.register(
        MarkdownRenderer(
            formatter,
        )
    )

    registry.register(
        JsonRenderer()
    )

    return registry

def build_rendering_service() -> RenderingService:
    """
    Builds the report rendering service.
    """

    return RenderingService(
        build_renderer_registry(),
    )