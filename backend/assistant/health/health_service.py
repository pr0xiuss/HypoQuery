from __future__ import annotations

from backend.assistant.health.health_check import (
    HealthCheck,
)


class HealthService:
    """
    Executes assistant platform health
    checks.
    """

    def __init__(
        self,
        checks: list[HealthCheck],
    ) -> None:

        self._checks = checks

    def check(
        self,
    ) -> dict[str, bool]:

        return {
            check.name: check.check()
            for check in self._checks
        }