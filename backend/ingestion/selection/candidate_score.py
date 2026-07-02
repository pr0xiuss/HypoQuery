from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CandidateScore:
    """
    Detailed score assigned to an analysis candidate.
    """

    duration_score: float

    frequency_score: float

    resource_score: float

    rows_score: float

    @property
    def total(self) -> float:
        return (
            self.duration_score
            + self.frequency_score
            + self.resource_score
            + self.rows_score
        )