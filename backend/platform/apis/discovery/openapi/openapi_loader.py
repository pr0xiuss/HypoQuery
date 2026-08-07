from abc import ABC
from abc import abstractmethod
from pathlib import Path


class OpenAPILoader(
    ABC,
):
    """
    Loads an OpenAPI specification from disk.
    """

    @abstractmethod
    def load(
        self,
        specification: Path,
    ) -> dict:
        """
        Loads and returns the OpenAPI document.
        """