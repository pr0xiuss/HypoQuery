from unittest.mock import Mock

from backend.execution.contracts.execution import (
    PipelineExecution,
)
from backend.execution.contracts.job import (
    PipelineJob,
)
from backend.execution.contracts.context import (
    PipelineContext,
)
from backend.execution.contracts.state import (
    PipelineState,
)
from backend.optimization.models.execution_plan import (
    ExecutionPlan,
)
from backend.optimization.nodes.validation_node import (
    ValidationNode,
)
from backend.optimization.recommendation.models.recommendation_collection import (
    RecommendationCollection,
)
from uuid import uuid4


def test_validation_node_executes():

    engine = Mock()

    engine.validate.return_value = Mock()

    node = ValidationNode(
        engine,
    )

    execution = PipelineExecution(
        job=PipelineJob(
            source="pytest",
            pipeline_version="1.0",
        ),
        context=PipelineContext(
            execution_id=uuid4(),
            trace_id=uuid4(),
            pipeline_name="optimization",
            pipeline_version="1.0",
            database="postgres",
            schema="public",
        ),
        state=PipelineState(
            execution_plan=ExecutionPlan(
                node_type="Seq Scan",
            ),
            recommendation_result=RecommendationCollection(),
            normalized_sql="SELECT 1;",
        ),
    )

    result = node.execute(
        execution,
    )

    assert result.success

    engine.validate.assert_called_once()