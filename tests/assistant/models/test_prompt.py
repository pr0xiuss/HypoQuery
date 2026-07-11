from backend.assistant.models.prompt import (
    Prompt,
)


def test_prompt():

    prompt = Prompt(
        system="System",
        user="User",
    )

    assert prompt.system == "System"

    assert prompt.user == "User"