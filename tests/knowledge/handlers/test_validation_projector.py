from uuid import uuid4

from backend.knowledge.projection.builders.validation_node_builder import (
    ValidationNodeBuilder,
)
from backend.knowledge.projection.builders.validation_relationship_builder import (
    ValidationRelationshipBuilder,
)
from backend.knowledge.projection.context import ProjectionContext
from backend.knowledge.projection.handlers.validation_projector import (
    ValidationProjector,
)
from backend.knowledge.projection.job import ProjectionJob
from backend.optimization.history.models.execution_metadata import (
    ExecutionMetadata,
)
from backend.optimization.history.models.execution_record import (
    ExecutionRecord,
)
from backend.optimization.history.models.execution_summary import (
    ExecutionSummary,
)
from backend.optimization.history.models.optimization_snapshot import (
    OptimizationSnapshot,
)
from backend.optimization.recommendation.models.recommendation import (
    Recommendation,
)
from backend.optimization.recommendation.models.category import (
    RecommendationCategory,
)
from backend.optimization.recommendation.models.recommendation_key import (
    RecommendationKey,
)
from backend.optimization.recommendation.models.priority import (
    RecommendationPriority,
)
from backend.optimization.reporting.models.report_summary import (
    ReportSummary,
)
from backend.optimization.validation.models.validation import (
    Validation,
)
from backend.optimization.validation.models.validation_status import (
    ValidationStatus,
)
from backend.optimization.validation.models.validation_type import (
    ValidationType,
)


def test_validation_projector_projects_node():

    recommendation = Recommendation(
        category=RecommendationCategory.INDEX,
        code="CREATE_INDEX",
        key=RecommendationKey(
            category="index",
            target="users",
            action="create",
        ),
        title="Create Index",
        description="Create Index",
        priority=RecommendationPriority.HIGH,
    )

    validation = Validation(
        recommendation=recommendation,
        status=ValidationStatus.VALIDATED,
        validation_type=ValidationType.HYPOTHETICAL_INDEX,
    )

    snapshot = OptimizationSnapshot(
        summary=ReportSummary(),
        validations=(validation,),
    )

    execution = ExecutionRecord(
        metadata=ExecutionMetadata(
            execution_id=uuid4(),
            trace_id=uuid4(),
            fingerprint="fp",
            normalized_sql="SELECT 1",
            pipeline_name="knowledge",
            pipeline_version="1.0",
            database="postgres",
            schema="public",
        ),
        summary=ExecutionSummary(),
        snapshot=snapshot,
    )

    context = ProjectionContext(
        job=ProjectionJob(
            execution=execution,
        ),
    )

    projector = ValidationProjector(
        node_builder=ValidationNodeBuilder(),
        relationship_builder=ValidationRelationshipBuilder(),
    )

    projector.project(
        context=context,
        graph=context.graph,
    )

    assert context.graph.node_count() == 1

    assert context.graph.relationship_count() == 0