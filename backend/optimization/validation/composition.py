from __future__ import annotations

from psycopg import Connection

from backend.optimization.collectors.explain_collector import ExplainCollector
from backend.optimization.parsers.explain_parser import ExplainParser
from backend.optimization.validation.builders.index_statement_builder import IndexStatementBuilder
from backend.optimization.validation.comparison.plan_comparator import PlanComparator
from backend.optimization.validation.engine import ValidationEngine
from backend.optimization.validation.hypopg.hypopg_client import HypoPGClient
from backend.optimization.validation.hypopg.hypopg_session import HypoPGSession
from backend.optimization.validation.registry.validator_registry import ValidatorRegistry
from backend.optimization.validation.validators.hypothetical_index_validator import HypotheticalIndexValidator


def build_validation_engine(
    connection: Connection,
) -> ValidationEngine:
    """
    Builds the Validation bounded context.
    """

    registry = ValidatorRegistry()

    registry.register(
        HypotheticalIndexValidator(
            statement_builder=IndexStatementBuilder(),
            session=HypoPGSession(
                HypoPGClient(
                    connection,
                ),
            ),
            collector=ExplainCollector(
                connection,
            ),
            parser=ExplainParser(),
            comparator=PlanComparator(),
        )
    )

    return ValidationEngine(
        registry,
    )