from backend.assistant.models.usage import (
    Usage,
)
from backend.assistant.telemetry.metrics import (
    MetricsCollector,
)


def test_metrics_collector():

    collector = MetricsCollector()

    collector.record(
        Usage(
            input_tokens=10,
            output_tokens=20,
            total_tokens=30,
        )
    )

    metrics = collector.metrics

    assert metrics.requests == 1

    assert metrics.input_tokens == 10

    assert metrics.output_tokens == 20

    assert metrics.total_tokens == 30