-- id: SUB001
-- name: Customers With Orders
-- category: SUBQUERY
-- difficulty: EASY
-- expected_issue: CORRELATED_SUBQUERY
-- description: Finds customers who have placed at least one order.
-- expected_fix: Rewrite using EXISTS or JOIN when appropriate.

SELECT *
FROM customers
WHERE customer_id IN (
    SELECT customer_id
    FROM orders
);