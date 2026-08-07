import json
from pathlib import Path

import yaml

from backend.platform.apis.discovery.openapi.openapi_loader import (
    OpenAPILoader,
)


class OpenAPILoaderImpl(
    OpenAPILoader,
):
    """
    Loads JSON or YAML OpenAPI specifications.
    """

    def load(
        self,
        specification: Path,
    ) -> dict:

        suffix = specification.suffix.lower()

        if suffix == ".json":
            return json.loads(
                specification.read_text(
                    encoding="utf-8",
                )
            )

        if suffix in {
            ".yaml",
            ".yml",
        }:
            return yaml.safe_load(
                specification.read_text(
                    encoding="utf-8",
                )
            )

        raise ValueError(
            f"Unsupported OpenAPI specification: {specification}",
        )