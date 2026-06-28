-- id: SUB002
-- name: Products With Reviews
-- category: SUBQUERY
-- difficulty: EASY
-- expected_issue: CORRELATED_SUBQUERY
-- description: Finds products that have at least one review.
-- expected_fix: Rewrite using EXISTS or JOIN when beneficial.

SELECT *
FROM products
WHERE product_id IN (
    SELECT product_id
    FROM reviews
);