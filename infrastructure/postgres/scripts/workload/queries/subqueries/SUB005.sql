-- id: SUB005
-- name: Customers Without Orders
-- category: SUBQUERY
-- difficulty: HARD
-- expected_issue: CORRELATED_SUBQUERY
-- description: Finds customers who have never placed an order.
-- expected_fix: Rewrite using NOT EXISTS or LEFT JOIN.

SELECT *
FROM customers c
WHERE NOT EXISTS
(
    SELECT 1
    FROM orders o
    WHERE o.customer_id = c.customer_id
);