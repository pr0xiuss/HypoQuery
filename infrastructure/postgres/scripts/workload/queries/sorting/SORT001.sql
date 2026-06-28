-- id: SORT001
-- name: Products By Price
-- category: SORTING
-- difficulty: EASY
-- expected_issue: SORT
-- description: Sorts products by price in ascending order.
-- expected_fix: Create an index on price if sorting is frequent.

SELECT *
FROM products
ORDER BY price;