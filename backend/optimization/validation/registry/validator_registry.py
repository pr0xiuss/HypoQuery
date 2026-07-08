from __future__ import annotations

from collections.abc import Iterator

from backend.optimization.validation.validators.base_validator import (
    RecommendationValidator,
)


class ValidatorRegistry:
    """
    Stores all registered recommendation validators.
    """

    def __init__(self) -> None:

        self._validators: list[
            RecommendationValidator
        ] = []

    def register(
        self,
        validator: RecommendationValidator,
    ) -> None:

        self._validators.append(
            validator,
        )

    def __iter__(
        self,
    ) -> Iterator[RecommendationValidator]:

        return iter(
            self._validators,
        )

    def __len__(
        self,
    ) -> int:

        return len(
            self._validators,
        )