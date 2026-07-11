from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class UsageMetrics:
    """
    Aggregated assistant usage metrics.
    """

    requests: int = 0

    input_tokens: int = 0

    output_tokens: int = 0

    total_tokens: int = 0

    def record(
        self,
        input_tokens: int,
        output_tokens: int,
        total_tokens: int,
    ) -> None:

        self.requests += 1

        self.input_tokens += input_tokens

        self.output_tokens += output_tokens

        self.total_tokens += total_tokens