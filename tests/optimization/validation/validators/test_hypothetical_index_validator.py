from unittest.mock import Mock

from backend.optimization.models.execution_plan import (
    ExecutionPlan,
)
from backend.optimization.recommendation.models.category import (
    RecommendationCategory,
)
from backend.optimization.recommendation.models.location import (
    RecommendationLocation,
)
from backend.optimization.recommendation.models.metadata import (
    RecommendationMetadata,
)
from backend.optimization.recommendation.models.priority import (
    RecommendationPriority,
)
from backend.optimization.recommendation.models.recommendation import (
    Recommendation,
)
from backend.optimization.recommendation.models.recommendation_key import (
    RecommendationKey,
)
from backend.optimization.validation.context import (
    ValidationContext,
)
from backend.optimization.validation.models.improvement_metrics import (
    ImprovementMetrics,
)
from backend.optimization.validation.models.validation_status import (
    ValidationStatus,
)
from backend.optimization.validation.validators.hypothetical_index_validator import (
    HypotheticalIndexValidator,
)


def test_validator_runs_complete_validation():

    builder = Mock()

    builder.build.return_value = (
        "CREATE INDEX idx_users_id "
        "ON users(id)"
    )

    session = Mock()

    session.__enter__ = Mock(
        return_value=session,
    )

    session.__exit__ = Mock(
        return_value=None,
    )

    session.create.return_value = Mock(
        name="idx_users_id",
    )

    collector = Mock()

    collector.collect.return_value = {
        "Plan": {
            "Node Type": "Index Scan",
        },
        "Planning Time": 0,
        "Execution Time": 0,
    }

    parser = Mock()

    parser.parse.return_value = ExecutionPlan(
        node_type="Index Scan",
        total_cost=20,
    )

    comparator = Mock()

    comparator.compare.return_value = (
        ImprovementMetrics(
            before_cost=100,
            after_cost=20,
            cost_delta=-80,
            improvement_percent=80,
            before_rows=1000,
            after_rows=1000,
            plan_changed=True,
            cost_reduced=True,
        )
    )

    validator = HypotheticalIndexValidator(
        statement_builder=builder,
        session=session,
        collector=collector,
        parser=parser,
        comparator=comparator,
    )

    recommendation = Recommendation(
        category=RecommendationCategory.INDEX,
        code="CREATE_INDEX",
        key=RecommendationKey(
            category="index",
            target="users",
            action="create",
        ),
        title="Create Index",
        description="",
        priority=RecommendationPriority.HIGH,
        location=RecommendationLocation(
            relation="users",
            schema="public",
        ),
        metadata=RecommendationMetadata(
            attributes={
                "filter_columns": [
                    "id",
                ],
            },
        ),
    )

    context = ValidationContext(
        execution_plan=ExecutionPlan(
            node_type="Seq Scan",
            total_cost=100,
        ),
        recommendation_result=None,
        normalized_sql="SELECT * FROM users;",
        fingerprint=None,
    )

    validation = validator.validate(
        context,
        recommendation,
    )

    assert validation.status == (
        ValidationStatus.VALIDATED
    )

    builder.build.assert_called_once()

    session.create.assert_called_once()

    collector.collect.assert_called_once()

    parser.parse.assert_called_once()

    comparator.compare.assert_called_once()