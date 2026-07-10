from backend.assistant.models.usage import (
    Usage,
)


def test_usage():

    usage = Usage(
        input_tokens=100,
        output_tokens=50,
        total_tokens=150,
    )

    assert usage.input_tokens == 100

    assert usage.output_tokens == 50

    assert usage.total_tokens == 150