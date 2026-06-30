from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class QueryFingerprint:
    """
    Immutable value object representing a normalized SQL fingerprint.
    """

    normalized_sql: str
    hash: str
    algorithm: str = "sha256"