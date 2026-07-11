from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class Plugin(ABC):
    """
    Base contract implemented by every
    assistant platform plugin.
    """

    @property
    @abstractmethod
    def name(
        self,
    ) -> str:
        """
        Unique plugin name.
        """

    @abstractmethod
    def register(
        self,
    ) -> None:
        """
        Register plugin resources with the
        assistant platform.
        """