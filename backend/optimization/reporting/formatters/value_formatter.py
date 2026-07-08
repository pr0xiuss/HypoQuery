from __future__ import annotations


class ValueFormatter:
    """
    Formats primitive values for presentation.
    """

    def percentage(
        self,
        value: float,
    ) -> str:

        return f"{value:.1f}%"

    def score(
        self,
        value: float,
    ) -> str:

        return f"{value:.1f}"

    def boolean(
        self,
        value: bool,
    ) -> str:

        return (
            "Yes"
            if value
            else "No"
        )

    def cost(
        self,
        value: float,
    ) -> str:

        return f"{value:.2f}"

    def duration_ms(
        self,
        value: float,
    ) -> str:

        return f"{value:.2f} ms"