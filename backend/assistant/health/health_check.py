from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class HealthCheck(ABC):
    """
    Base contract implemented by every
    assistant health check.
    """

    @property
    @abstractmethod
    def name(
        self,
    ) -> str:
        """
        Health check name.
        """

    @abstractmethod
    def check(
        self,
    ) -> bool:
        """
        Execute the health check.
        """