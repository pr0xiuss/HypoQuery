from __future__ import annotations

from backend.assistant.models.usage import (
    Usage,
)
from backend.assistant.telemetry.usage_metrics import (
    UsageMetrics,
)


class MetricsCollector:
    """
    Collects assistant usage metrics.
    """

    def __init__(
        self,
    ) -> None:

        self._metrics = UsageMetrics()

    def record(
        self,
        usage: Usage,
    ) -> None:

        self._metrics.record(
            input_tokens=usage.input_tokens,
            output_tokens=usage.output_tokens,
            total_tokens=usage.total_tokens,
        )

    @property
    def metrics(
        self,
    ) -> UsageMetrics:

        return self._metrics