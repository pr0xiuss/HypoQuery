from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Prompt:
    """
    Canonical prompt produced from an
    ExplanationSnapshot.

    Prompt remains provider-agnostic and can be sent
    to any supported language model.
    """

    system: str

    user: str