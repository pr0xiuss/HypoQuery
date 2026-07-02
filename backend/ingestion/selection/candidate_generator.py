from .analysis_candidate import AnalysisCandidate


class CandidateGenerator:
    """
    Converts collected workload data into analysis candidates.
    """

    def generate(
        self,
        workload: list[AnalysisCandidate],
    ) -> list[AnalysisCandidate]:
        """
        Generates analysis candidates.

        Currently this is an identity transformation.
        Future implementations may merge duplicate
        fingerprints, enrich metadata, or filter
        unsupported queries.
        """

        return list(workload)