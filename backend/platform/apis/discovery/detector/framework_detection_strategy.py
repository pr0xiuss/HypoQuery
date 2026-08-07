from abc import ABC
from abc import abstractmethod
from pathlib import Path

from backend.platform.apis.domain.api_framework import (
    ApiFramework,
)


class FrameworkDetectionStrategy(
    ABC,
):
    """
    Strategy used to identify whether a repository
    belongs to a specific backend framework.
    """

    @abstractmethod
    def supports(
        self,
        repository_root: Path,
    ) -> bool:
        """
        Returns True if this strategy recognizes
        the repository.
        """

    @property
    @abstractmethod
    def framework(
        self,
    ) -> ApiFramework:
        """
        Framework represented by this strategy.
        """