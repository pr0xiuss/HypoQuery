-- id: JOIN003
-- name: Products Reviews
-- category: JOIN
-- difficulty: EASY
-- expected_issue: HASH_JOIN
-- description: Joins products with reviews.
-- expected_fix: Index product_id if required.

SELECT
    p.product_name,
    r.rating
FROM products p
JOIN reviews r
ON p.product_id = r.product_id;