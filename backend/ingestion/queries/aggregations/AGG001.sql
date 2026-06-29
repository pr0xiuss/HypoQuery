-- id: AGG001
-- name: Average Product Price
-- category: AGGREGATION
-- difficulty: EASY
-- expected_issue: HASH_AGGREGATE
-- description: Computes the average price of all products.
-- expected_fix: Consider indexing filter columns when aggregation is combined with filtering.

SELECT AVG(price)
FROM products;