-- id: SORT002
-- name: Orders By Amount
-- category: SORTING
-- difficulty: EASY
-- expected_issue: SORT
-- description: Sorts orders by total amount.
-- expected_fix: Create an index on total_amount.

SELECT *
FROM orders
ORDER BY total_amount DESC;