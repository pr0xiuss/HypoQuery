-- ============================================================
-- HypoQuery Optimization History
-- ============================================================

CREATE TABLE IF NOT EXISTS optimization_history
(
    execution_id UUID PRIMARY KEY,

    trace_id UUID NOT NULL,

    fingerprint TEXT NOT NULL,

    normalized_sql TEXT NOT NULL

    pipeline_name TEXT NOT NULL,

    pipeline_version TEXT NOT NULL,

    database_name TEXT NOT NULL,

    schema_name TEXT NOT NULL,

    executed_at TIMESTAMPTZ NOT NULL,

    recommendation_count INTEGER NOT NULL,

    validated_recommendation_count INTEGER NOT NULL,

    strategy_count INTEGER NOT NULL,

    estimated_improvement_percent DOUBLE PRECISION NOT NULL,

    highest_strategy_score DOUBLE PRECISION NOT NULL,

    snapshot_json JSONB NOT NULL
);