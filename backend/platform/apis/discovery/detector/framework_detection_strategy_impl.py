from pathlib import Path

from backend.platform.apis.discovery.detector.framework_detector import (
    FrameworkDetector,
)
from backend.platform.apis.discovery.detector.framework_detection_strategy import (
    FrameworkDetectionStrategy,
)
from backend.platform.apis.domain.api_framework import (
    ApiFramework,
)


class FrameworkDetectorImpl(
    FrameworkDetector,
):
    """
    Detects the backend framework by evaluating
    registered detection strategies.
    """

    def __init__(
        self,
        strategies: list[
            FrameworkDetectionStrategy
        ],
    ) -> None:
        self._strategies = strategies

    def detect(
        self,
        repository_root: Path,
    ) -> ApiFramework:
        for strategy in self._strategies:
            if strategy.supports(
                repository_root,
            ):
                return strategy.framework

        return ApiFramework.OTHER