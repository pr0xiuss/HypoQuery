from backend.assistant.profiles.json_profile import (
    JsonProfile,
)


def test_json_profile():

    profile = JsonProfile()

    assert profile.name == "json"

    assert profile.renderer == "json"