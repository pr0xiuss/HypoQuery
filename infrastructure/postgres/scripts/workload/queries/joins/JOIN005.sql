-- id: JOIN005
-- name: Products Events
-- category: JOIN
-- difficulty: MEDIUM
-- expected_issue: HASH_JOIN
-- description: Joins products with event history.
-- expected_fix: Index product_id.

SELECT
    p.product_name,
    e.event_type
FROM products p
JOIN product_events e
ON p.product_id = e.product_id;