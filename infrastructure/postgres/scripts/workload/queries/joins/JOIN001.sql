-- id: JOIN001
-- name: Orders Customers Inner Join
-- category: JOIN
-- difficulty: EASY
-- expected_issue: HASH_JOIN
-- description: Joins orders with customers using customer_id.
-- expected_fix: Add indexes on join keys if missing.

SELECT
    o.order_id,
    c.first_name,
    c.last_name,
    o.total_amount
FROM orders o
JOIN customers c
ON o.customer_id = c.customer_id;