from uuid import uuid4

from backend.execution.contracts.execution import (
    PipelineExecution,
)
from backend.execution.contracts.job import (
    PipelineJob,
)
from backend.execution.contracts.context import (
    PipelineContext,
)
from backend.optimization.reporting.builders.optimization_report_builder import (
    OptimizationReportBuilder,
)
from backend.optimization.reporting.builders.recommendation_report_builder import (
    RecommendationReportBuilder,
)
from backend.optimization.reporting.builders.strategy_report_builder import (
    StrategyReportBuilder,
)
from backend.optimization.reporting.builders.validation_report_builder import (
    ValidationReportBuilder,
)
from backend.optimization.reporting.engine import (
    ReportingEngine,
)
from backend.optimization.reporting.node import (
    ReportingNode,
)
from backend.optimization.ranking.grouping.models.strategy_result import (
    StrategyResult,
)


def test_execute():

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

    execution.state.strategy_result = (
        StrategyResult()
    )

    node = ReportingNode(
        ReportingEngine(
            OptimizationReportBuilder(
                StrategyReportBuilder(
                    RecommendationReportBuilder(),
                    ValidationReportBuilder(),
                )
            )
        )
    )

    result = node.execute(
        execution,
    )

    assert result.success

    assert execution.state.report is not None

    assert (
        execution.state.report.summary.total_strategies
        == 0
    )