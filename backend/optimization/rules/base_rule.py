from abc import ABC, abstractmethod

from infrastructure.postgres.scripts.observability.models.execution_plan import (
    ExecutionPlan,
)
from infrastructure.postgres.scripts.observability.models.optimization_finding import (
    OptimizationFinding,
)


class BaseRule(ABC):

    @abstractmethod
    def check(
        self,
        plan: ExecutionPlan,
    ) -> list[OptimizationFinding]:
        pass
