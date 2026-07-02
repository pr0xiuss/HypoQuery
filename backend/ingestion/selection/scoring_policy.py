from .analysis_candidate import AnalysisCandidate
from .candidate_score import CandidateScore


class ScoringPolicy:
    """
    Computes the priority score of an analysis candidate.
    """

    def score(
        self,
        candidate: AnalysisCandidate,
    ) -> CandidateScore:

        duration_score = (
            candidate.average_duration_ms * 0.40
        )

        frequency_score = (
            candidate.execution_count * 0.30
        )

        resource_score = (
            (
                candidate.shared_blocks_read
                + candidate.temp_blocks_written
            )
            * 0.20
        )

        rows_score = (
            candidate.rows_processed * 0.10
        )

        return CandidateScore(
            duration_score=duration_score,
            frequency_score=frequency_score,
            resource_score=resource_score,
            rows_score=rows_score,
        )