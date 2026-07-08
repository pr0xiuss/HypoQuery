from __future__ import annotations

from dataclasses import dataclass

from backend.optimization.history.models.execution_metadata import (
    ExecutionMetadata,
)
from backend.optimization.history.models.execution_summary import (
    ExecutionSummary,
)
from backend.optimization.history.models.optimization_snapshot import (
    OptimizationSnapshot,
)


@dataclass(frozen=True, slots=True)
class ExecutionRecord:
    """
    Aggregate root representing one completed
    optimization execution.
    """

    metadata: ExecutionMetadata

    summary: ExecutionSummary

    snapshot: OptimizationSnapshot