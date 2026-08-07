from enum import Enum


class SyncOperation(
    str,
    Enum,
):
    """
    Operation required to synchronize a discovered
    route with the API registry.
    """

    CREATE = "create"

    UPDATE = "update"

    ARCHIVE = "archive"

    UNCHANGED = "unchanged"