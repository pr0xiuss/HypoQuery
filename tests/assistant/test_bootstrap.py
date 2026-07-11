from backend.assistant.bootstrap import (
    build_assistant_platform,
)
from backend.assistant.platform import (
    AssistantPlatform,
)


def test_bootstrap():

    platform = build_assistant_platform()

    assert isinstance(
        platform,
        AssistantPlatform,
    )