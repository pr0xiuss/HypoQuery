-- id: AGG005
-- name: Product Events Count
-- category: AGGREGATION
-- difficulty: MEDIUM
-- expected_issue: HASH_AGGREGATE
-- description: Counts product events grouped by event type.
-- expected_fix: Index event_type for repeated analytical queries.

SELECT
    event_type,
    COUNT(*)
FROM product_events
GROUP BY event_type;