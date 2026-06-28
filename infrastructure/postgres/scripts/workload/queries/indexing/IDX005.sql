-- id: IDX005
-- name: Product Event Type Lookup
-- category: INDEXING
-- difficulty: HARD
-- expected_issue: MISSING_INDEX
-- description: Filters product events by event type.
-- expected_fix: CREATE INDEX idx_product_events_type ON product_events(event_type);

SELECT *
FROM product_events
WHERE event_type = 'PRICE_UPDATED';