from __future__ import annotations

from dataclasses import dataclass

from backend.execution.contracts.execution import PipelineExecution
from backend.optimization.reporting.models.optimization_report import OptimizationReport
from backend.optimization.history.models.execution_record import ExecutionRecord

@dataclass(frozen=True, slots=True)
class HistoryContext:
    """
    Input contract for the History bounded context.
    """

    execution: PipelineExecution

    report: OptimizationReport

    baseline: ExecutionRecord | None = None