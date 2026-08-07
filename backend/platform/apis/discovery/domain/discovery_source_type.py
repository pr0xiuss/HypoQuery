from enum import Enum


class DiscoverySourceType(
    str,
    Enum,
):
    """
    Supported API discovery sources.
    """

    OPENAPI_URL = "openapi_url"

    OPENAPI_FILE = "openapi_file"

    REPOSITORY = "repository"