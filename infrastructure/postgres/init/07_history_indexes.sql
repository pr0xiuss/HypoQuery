-- ============================================================
-- HypoQuery Optimization History Indexes
-- ============================================================

CREATE INDEX IF NOT EXISTS
idx_history_fingerprint
ON optimization_history (
    fingerprint
);

CREATE INDEX IF NOT EXISTS
idx_history_database
ON optimization_history (
    database_name
);

CREATE INDEX IF NOT EXISTS
idx_history_schema
ON optimization_history (
    schema_name
);

CREATE INDEX IF NOT EXISTS
idx_history_pipeline
ON optimization_history (
    pipeline_name
);

CREATE INDEX IF NOT EXISTS
idx_history_executed_at
ON optimization_history (
    executed_at DESC
);

CREATE INDEX IF NOT EXISTS
idx_history_improvement
ON optimization_history (
    estimated_improvement_percent DESC
);

CREATE INDEX IF NOT EXISTS
idx_history_strategy_count
ON optimization_history (
    strategy_count
);

CREATE INDEX IF NOT EXISTS
idx_history_recommendation_count
ON optimization_history (
    recommendation_count
);

CREATE INDEX IF NOT EXISTS
idx_history_snapshot
ON optimization_history
USING GIN (
    snapshot_json
);