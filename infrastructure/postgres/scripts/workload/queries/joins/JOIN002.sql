-- id: JOIN002
-- name: Customer Orders Reviews
-- category: JOIN
-- difficulty: MEDIUM
-- expected_issue: HASH_JOIN
-- description: Joins customers, orders and reviews.
-- expected_fix: Ensure join columns are indexed.

SELECT
    c.first_name,
    o.order_id,
    r.rating
FROM customers c
JOIN orders o
ON c.customer_id = o.customer_id
JOIN reviews r
ON c.customer_id = r.customer_id;