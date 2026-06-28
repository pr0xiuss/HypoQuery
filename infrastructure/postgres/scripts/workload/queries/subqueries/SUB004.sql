-- id: SUB004
-- name: Highest Rated Products
-- category: SUBQUERY
-- difficulty: MEDIUM
-- expected_issue: CORRELATED_SUBQUERY
-- description: Finds products with an average rating greater than four.
-- expected_fix: Rewrite using JOIN + GROUP BY when appropriate.

SELECT *
FROM products
WHERE product_id IN
(
    SELECT product_id
    FROM reviews
    GROUP BY product_id
    HAVING AVG(rating) > 4
);