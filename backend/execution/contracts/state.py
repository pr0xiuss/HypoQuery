from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class PipelineState:
    """
    Mutable execution state.

    Nodes progressively enrich this object as the pipeline executes.
    """

    execution_plan: Any | None = None

    findings: list[Any] = field(default_factory=list)

    artifacts: dict[str, Any] = field(default_factory=dict)

    metrics: dict[str, Any] = field(default_factory=dict)

    errors: list[Exception] = field(default_factory=list)


    def add_metric(self, key: str, value: Any) -> None:
        self.metrics[key] = value

    def add_artifact(self, key: str, value: Any) -> None:
        self.artifacts[key] = value

    def add_error(self, error: Exception) -> None:
        self.errors.append(error)