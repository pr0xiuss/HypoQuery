from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ValidationMetadata:
    """
    Stores additional information produced during validation.
    """

    attributes: dict[str, object] = field(
        default_factory=dict,
    )