from .analysis_candidate import AnalysisCandidate
from .scoring_policy import ScoringPolicy


class SelectionEngine:
    """
    Selects the highest-priority analysis candidates.
    """

    def __init__(self, scoring_policy: ScoringPolicy,) -> None:
        
        self._scoring_policy = scoring_policy

    def select(self, candidates: list[AnalysisCandidate], limit: int,) -> list[AnalysisCandidate]:

        ranked = sorted(
            candidates,
            key=lambda candidate: (self._scoring_policy.score(candidate).total),
            reverse=True,
        )

        return ranked[:limit]