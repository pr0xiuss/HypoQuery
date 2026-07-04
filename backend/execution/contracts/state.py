from dataclasses import dataclass, field
from typing import Any
from backend.optimization.analysis.models.analysis_result import AnalysisResult
from backend.execution.contracts.fingerprint import QueryFingerprint
from backend.execution.lifecycle.enums import ExecutionStatus
from backend.optimization.recommendation.models.recommendation_result import RecommendationResult

@dataclass(slots=True)
class PipelineState:
    """
    Mutable execution state.

    This object represents the current runtime state of a pipeline execution.
    Pipeline nodes progressively enrich it while the ExecutionLifecycle
    manages valid lifecycle transitions.
    """

    status: ExecutionStatus = ExecutionStatus.CREATED

    normalized_sql: str | None = None

    fingerprint: QueryFingerprint | None = None

    execution_plan: Any | None = None

    analysis_result: AnalysisResult | None = None

    recommendation_result: RecommendationResult | None = None

    artifacts: dict[str, Any] = field(default_factory=dict)

    metrics: dict[str, Any] = field(default_factory=dict)

    errors: list[Exception] = field(default_factory=list)


    def add_metric(self, key: str, value: Any) -> None:
        self.metrics[key] = value

    def add_artifact(self, key: str, value: Any) -> None:
        self.artifacts[key] = value

    def add_error(self, error: Exception) -> None:
        self.errors.append(error)