import re
from pathlib import Path
from uuid import UUID
from backend.platform.apis.discovery.domain.discovered_route import DiscoveredRoute
from backend.platform.apis.discovery.extractors.base_route_extractor import BaseRouteExtractor
from backend.platform.apis.discovery.extractors.fastapi_route_parser import FastAPIRouteParser


class FastAPIRouteExtractor(
    BaseRouteExtractor,
):
    """
    Discovers FastAPI routes from Python source files.
    """

    ROUTE_PATTERN = re.compile(
        r'@(app|router)\.(get|post|put|delete|patch|options|head)\("([^"]+)"'
    )

    FUNCTION_PATTERN = re.compile(
        r"def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\("
    )

    def __init__(
        self,
        parser: FastAPIRouteParser,
    ) -> None:
        self._parser = parser

    def discover(
        self,
        environment_id: UUID,
        repository_root: Path,
    ) -> list[DiscoveredRoute]:

        routes: list[DiscoveredRoute] = []

        for file in repository_root.rglob(
            "*.py",
        ):

            try:
                lines = file.read_text(
                    encoding="utf-8",
                ).splitlines()

            except Exception:
                continue

            for index, line in enumerate(lines):

                match = self.ROUTE_PATTERN.search(
                    line,
                )

                if match is None:
                    continue

                handler = "unknown"

                for next_line in lines[index + 1 :]:

                    function_match = self.FUNCTION_PATTERN.search(
                        next_line,
                    )

                    if function_match:
                        handler = function_match.group(
                            1,
                        )
                        break

                routes.append(
                    self._parser.parse(
                        environment_id=environment_id,
                        method=match.group(2),
                        path=match.group(3),
                        handler=handler,
                        source_file=file,
                        line_number=index + 1,
                    )
                )

        return routes