from __future__ import annotations

from dataclasses import dataclass

from backend.optimization.history.models.execution_record import (
    ExecutionRecord,
)


@dataclass(frozen=True, slots=True)
class ProjectionJob:
    """
    Represents a single knowledge projection request.

    A ProjectionJob transforms one immutable ExecutionRecord
    into projected optimization knowledge.
    """

    execution: ExecutionRecord