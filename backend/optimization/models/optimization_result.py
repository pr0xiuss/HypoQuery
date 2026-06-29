from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class OptimizationResult:

    run_id: int

    diagnosis: str

    remediation_type: str

    recommended_index_sql: str | None = None

    rewritten_query: str | None = None

    llm_confidence: str | None = None

    retrieval_score: float | None = None

    faithfulness_score: float | None = None

    validation_status: str = "PENDING"

    original_explain_plan: dict | None = None

    optimized_explain_plan: dict | None = None

    created_at: datetime | None = None
