from __future__ import annotations

from backend.optimization.collectors.explain_collector import ExplainCollector
from backend.optimization.parsers.explain_parser import ExplainParser
from backend.optimization.recommendation.models.recommendation import Recommendation
from backend.optimization.validation.builders.index_statement_builder import IndexStatementBuilder
from backend.optimization.validation.comparison.plan_comparator import PlanComparator
from backend.optimization.validation.context import ValidationContext
from backend.optimization.validation.hypopg.hypopg_session import HypoPGSession
from backend.optimization.validation.models.validation import Validation
from backend.optimization.validation.models.validation_status import ValidationStatus
from backend.optimization.validation.models.validation_type import ValidationType
from backend.optimization.validation.validators.base_validator import RecommendationValidator


class HypotheticalIndexValidator(RecommendationValidator,):

    def __init__(
        self,
        statement_builder: IndexStatementBuilder,
        session: HypoPGSession,
        collector: ExplainCollector,
        parser: ExplainParser,
        comparator: PlanComparator,
    ) -> None:

        self._statement_builder = statement_builder

        self._session = session

        self._collector = collector

        self._parser = parser

        self._comparator = comparator

    @property
    def name(self,) -> str:

        return "hypothetical_index"

    @property
    def supported_codes(self,) -> set[str]:

        return {
            "CREATE_INDEX",
        }

    def validate(self, context: ValidationContext, recommendation: Recommendation,) -> Validation | None:

        try:
            statement = self._statement_builder.build(recommendation,)
            
            with self._session:
                index = self._session.create(statement,)
                report = self._collector.collect(context.normalized_sql,)
                candidate_plan = self._parser.parse(report,)
                metrics = self._comparator.compare(context.execution_plan, candidate_plan,)

                return Validation(
                    recommendation=recommendation,
                    status=(
                        ValidationStatus.VALIDATED
                        if metrics.cost_reduced
                        else ValidationStatus.REJECTED
                    ),
                    validation_type=ValidationType.HYPOTHETICAL_INDEX,
                    validation_artifact=index.name,
                    metrics=metrics,
                )

        except Exception:

            return Validation(
                recommendation=recommendation,
                status=ValidationStatus.FAILED,
                validation_type=ValidationType.HYPOTHETICAL_INDEX,
                validation_artifact=None,
                metrics=None,
            )