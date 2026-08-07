from abc import ABC
from abc import abstractmethod


class DiscoverySource(
    ABC,
):
    """
    Represents any source capable of providing
    API metadata.
    """

    @abstractmethod
    def name(
        self,
    ) -> str:
        """
        Returns a human-readable source name.
        """