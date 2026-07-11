from backend.assistant.profiles.markdown_profile import (
    MarkdownProfile,
)


def test_markdown_profile():

    profile = MarkdownProfile()

    assert profile.name == "markdown"

    assert profile.renderer == "markdown"