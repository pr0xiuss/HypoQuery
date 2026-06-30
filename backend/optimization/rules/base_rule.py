from abc import ABC, abstractmethod

from backend.optimization.models.execution_plan import (
    ExecutionPlan,
)
from backend.optimization.models.optimization_finding import (
    OptimizationFinding,
)


class BaseRule(ABC):

    @abstractmethod
    def check(
        self,
        plan: ExecutionPlan,
    ) -> list[OptimizationFinding]:
        pass
