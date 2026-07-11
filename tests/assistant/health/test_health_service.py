from backend.assistant.health.health_check import (
    HealthCheck,
)
from backend.assistant.health.health_service import (
    HealthService,
)


class FakeHealthCheck(
    HealthCheck,
):

    @property
    def name(
        self,
    ) -> str:

        return "fake"

    def check(
        self,
    ) -> bool:

        return True


def test_health_service():

    service = HealthService(
        checks=[
            FakeHealthCheck(),
        ],
    )

    result = service.check()

    assert result == {
        "fake": True,
    }