import re


def generate_slug(value: str) -> str:
    """
    Generate a URL-friendly slug from a string.
    """

    slug = value.strip().lower()

    slug = re.sub(r"\s+", "-", slug)

    slug = re.sub(r"[^a-z0-9-]", "", slug)

    slug = re.sub(r"-{2,}", "-", slug)

    return slug.strip("-")