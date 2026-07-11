from __future__ import annotations
from backend.optimization.analysis.models.finding import Finding
from backend.optimization.recommendation.models.recommendation import Recommendation
from backend.optimization.validation.models.validation import Validation
from backend.optimization.ranking.grouping.models.strategy import Strategy
from backend.optimization.reporting.models.report_summary import ReportSummary
from dataclasses import dataclass



@dataclass(frozen=True, slots=True)
class OptimizationSnapshot:
    """
    Immutable snapshot of the optimization output
    produced during one execution.
    """
    summary: ReportSummary

    findings: tuple[Finding, ...] = ()

    recommendations: tuple[Recommendation, ...] = ()

    validations: tuple[Validation, ...] = ()

    strategies: tuple[Strategy, ...] = ()
