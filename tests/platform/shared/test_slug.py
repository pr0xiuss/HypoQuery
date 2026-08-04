from backend.platform.shared.slug import generate_slug


def test_slugify_simple_text():
    """
    Slugify converts text to lowercase hyphenated form.
    """

    assert generate_slug("My Organization") == "my-organization"


def test_slugify_multiple_spaces():
    """
    Consecutive spaces are collapsed.
    """

    assert generate_slug("My   Test    Project") == "my-test-project"


def test_slugify_already_slugified():
    """
    Existing slugs remain unchanged.
    """

    assert generate_slug("backend-api") == "backend-api"