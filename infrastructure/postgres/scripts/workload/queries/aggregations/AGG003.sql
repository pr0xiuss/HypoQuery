-- id: AGG003
-- name: Average Review Rating
-- category: AGGREGATION
-- difficulty: EASY
-- expected_issue: HASH_AGGREGATE
-- description: Computes average rating for every product.
-- expected_fix: Index grouping column when dataset grows.

SELECT
    product_id,
    AVG(rating)
FROM reviews
GROUP BY product_id;