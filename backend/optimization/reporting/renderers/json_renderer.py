from __future__ import annotations

import json
from dataclasses import asdict
from enum import Enum

from backend.optimization.reporting.models.optimization_report import (
    OptimizationReport,
)
from backend.optimization.reporting.renderers.base_renderer import (
    ReportRenderer,
)


class JsonRenderer(
    ReportRenderer,
):
    """
    Renders an optimization report as JSON.
    """

    @property
    def name(
        self,
    ) -> str:

        return "json"

    def render(
        self,
        report: OptimizationReport,
    ) -> str:

        def convert(
            value,
        ):

            if isinstance(
                value,
                Enum,
            ):
                return value.value

            if isinstance(
                value,
                dict,
            ):
                return {
                    key: convert(
                        item,
                    )
                    for key, item in value.items()
                }

            if isinstance(
                value,
                list,
            ):
                return [
                    convert(
                        item,
                    )
                    for item in value
                ]

            return value

        payload = convert(
            asdict(
                report,
            )
        )

        return json.dumps(
            payload,
            indent=4,
            default=str,
        )