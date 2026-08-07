from abc import ABC
from abc import abstractmethod
from pathlib import Path

from backend.platform.apis.domain.api_framework import ApiFramework


class FrameworkDetector(
    ABC,
):
    """
    Detects which backend framework is used by a repository.
    """

    @abstractmethod
    def detect(
        self,
        repository_root: Path,
    ) -> ApiFramework:
        """
        Returns the detected framework.
        """