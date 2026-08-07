from pathlib import Path
from uuid import UUID
from backend.platform.apis.discovery.domain.discovered_route import DiscoveredRoute
from backend.platform.apis.domain.api_framework import ApiFramework


class FastAPIRouteParser:
    """
    Converts FastAPI route decorators into
    DiscoveredRoute objects.
    """

    def parse(
        self,
        *,
        environment_id: UUID,
        method: str,
        path: str,
        handler: str,
        source_file: Path,
        line_number: int,
    ) -> DiscoveredRoute:

        return DiscoveredRoute(
            environment_id=environment_id,
            framework=ApiFramework.FASTAPI,
            method=method.upper(),
            path=path,
            handler=handler,
            source_file=source_file,
            line_number=line_number,
        )