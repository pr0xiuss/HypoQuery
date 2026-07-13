from __future__ import annotations

from backend.operations.integration.context import (
    OperationsIntegrationContext,
)


class OperationsFacade:
    """
    Public application boundary of the
    Operations bounded context.
    """

    def __init__(
        self,
        context: OperationsIntegrationContext,
    ) -> None:
        self._context = context

    @property
    def cases(
        self,
    ):
        return self._context.cases.service

    @property
    def verification(
        self,
    ):
        return self._context.verification.service

    @property
    def outcome(
        self,
    ):
        return self._context.outcome.service

    @property
    def monitoring(
        self,
    ):
        return self._context.monitoring.service

    @property
    def policy(
        self,
    ):
        return self._context.policy.service