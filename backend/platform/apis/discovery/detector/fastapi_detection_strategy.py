from pathlib import Path

from backend.platform.apis.discovery.detector.framework_detection_strategy import (
    FrameworkDetectionStrategy,
)
from backend.platform.apis.domain.api_framework import (
    ApiFramework,
)


class FastAPIDetectionStrategy(
    FrameworkDetectionStrategy,
):
    """
    Detects FastAPI projects.
    """

    @property
    def framework(
        self,
    ) -> ApiFramework:
        return ApiFramework.FASTAPI

    def supports(
        self,
        repository_root: Path,
    ) -> bool:

        for file in repository_root.rglob(
            "*.py",
        ):
            try:
                contents = file.read_text(
                    encoding="utf-8",
                )

                if (
                    "from fastapi import FastAPI" in contents
                    or "import fastapi" in contents
                    or "APIRouter(" in contents
                ):
                    return True

            except Exception:
                continue

        return False