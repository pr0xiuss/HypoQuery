from uuid import uuid4

from backend.execution.contracts.context import (
    PipelineContext,
)
from backend.execution.contracts.execution import (
    PipelineExecution,
)
from backend.execution.contracts.job import (
    PipelineJob,
)
from backend.optimization.ranking.grouping.context import (
    StrategyContext,
)
from backend.optimization.ranking.grouping.engine import (
    StrategyEngine,
)
from backend.optimization.ranking.grouping.models.strategy_result import (
    StrategyResult,
)
from backend.optimization.ranking.models.ranking_result import (
    RankingResult,
)
from backend.optimization.ranking.grouping.node import (
    StrategyNode,
)


class DummyStrategyEngine(
    StrategyEngine,
):

    def __init__(
        self,
    ) -> None:
        pass

    def group(
        self,
        context: StrategyContext,
    ) -> StrategyResult:

        return StrategyResult()


def test_strategy_node():

    execution_id = uuid4()

    trace_id = uuid4()

    execution = PipelineExecution(
        job=PipelineJob(
            source="pytest",
            pipeline_version="1.0",
            job_id=execution_id,
            trace_id=trace_id,
        ),
        context=PipelineContext(
            execution_id=execution_id,
            trace_id=trace_id,
            pipeline_name="optimization",
            pipeline_version="1.0",
            database="postgres",
            schema="public",
        ),
    )

    execution.state.ranking_result = (
        RankingResult()
    )

    node = StrategyNode(
        DummyStrategyEngine(),
    )

    result = node.execute(
        execution,
    )

    assert result.success

    assert (
        execution.state.strategy_result
        is not None
    )