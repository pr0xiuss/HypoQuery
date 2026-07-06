from __future__ import annotations

from backend.optimization.collectors.explain_collector import ExplainCollector
from backend.optimization.parsers.explain_parser import ExplainParser
from backend.optimization.validation.builders.index_statement_builder import IndexStatementBuilder
from backend.optimization.validation.comparison.plan_comparator import PlanComparator
from backend.optimization.validation.context import ValidationContext
from backend.optimization.validation.hypopg.hypopg_session import HypoPGSession
from backend.optimization.validation.models.validation_collection import ValidationCollection
from backend.optimization.validation.validators.base_validator import RecommendationValidator


class HypotheticalIndexValidator(
    RecommendationValidator,
):
    """
    Validates index recommendations using HypoPG.
    """

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

    def validate(self, context: ValidationContext,) -> ValidationCollection:

        return ValidationCollection()
    
    @property
    def supported_keys(self,) -> set[str]:

        return {
            "CREATE_INDEX",
        }