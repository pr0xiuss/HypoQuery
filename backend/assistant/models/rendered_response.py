from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RenderedResponse:
    """
    Provider-independent response produced by the
    Assistant module.

    Rendered responses are ready for presentation to
    APIs, CLIs, or web frontends.
    """

    content: str

    format: str = "markdown"