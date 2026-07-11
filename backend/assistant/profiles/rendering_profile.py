from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class RenderingProfile(ABC):
    """
    Defines the preferred rendering
    format for assistant responses.
    """

    @property
    @abstractmethod
    def name(
        self,
    ) -> str:
        """
        Unique rendering profile name.
        """

    @property
    @abstractmethod
    def renderer(
        self,
    ) -> str:
        """
        Preferred renderer name.
        """