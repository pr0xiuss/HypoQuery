from backend.assistant.telemetry.usage_metrics import (
    UsageMetrics,
)


def test_usage_metrics():

    metrics = UsageMetrics()

    metrics.record(
        input_tokens=10,
        output_tokens=20,
        total_tokens=30,
    )

    assert metrics.requests == 1

    assert metrics.input_tokens == 10

    assert metrics.output_tokens == 20

    assert metrics.total_tokens == 30