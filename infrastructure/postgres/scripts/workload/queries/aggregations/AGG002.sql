-- id: AGG002
-- name: Orders Per Customer
-- category: AGGREGATION
-- difficulty: EASY
-- expected_issue: HASH_AGGREGATE
-- description: Counts orders grouped by customer.
-- expected_fix: Index grouping columns if frequently queried.

SELECT
    customer_id,
    COUNT(*)
FROM orders
GROUP BY customer_id;