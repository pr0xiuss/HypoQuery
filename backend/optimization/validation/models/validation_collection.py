from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterator

from backend.optimization.validation.models.validation import (
    Validation,
)


@dataclass(slots=True)
class ValidationCollection:
    """
    Represents all validations produced during one validation execution.
    """

    validations: list[Validation] = field(
        default_factory=list,
    )

    def add(
        self,
        validation: Validation,
    ) -> None:

        self.validations.append(
            validation,
        )

    def extend(
        self,
        validations: ValidationCollection,
    ) -> None:

        self.validations.extend(
            validations,
        )

    def __iter__(self) -> Iterator[Validation]:

        return iter(
            self.validations,
        )

    def __len__(self) -> int:

        return len(
            self.validations,
        )

    def is_empty(self) -> bool:

        return len(
            self.validations,
        ) == 0