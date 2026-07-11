from backend.assistant.telemetry.traces import (
    TraceCollector,
)


def test_traces():

    collector = TraceCollector()

    collector.record(
        provider="gemini",
        operation="generate",
    )

    assert len(
        collector.events
    ) == 1

    event = collector.events[0]

    assert event.provider == "gemini"

    assert event.operation == "generate"