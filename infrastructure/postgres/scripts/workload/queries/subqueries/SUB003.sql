-- id: SUB003
-- name: Orders Above Average
-- category: SUBQUERY
-- difficulty: MEDIUM
-- expected_issue: CORRELATED_SUBQUERY
-- description: Finds orders whose total exceeds the average order value.
-- expected_fix: Compute aggregate once using a CTE or derived table if reused.

SELECT *
FROM orders
WHERE total_amount >
(
    SELECT AVG(total_amount)
    FROM orders
);