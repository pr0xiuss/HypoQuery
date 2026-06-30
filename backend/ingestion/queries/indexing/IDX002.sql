-- id: IDX002
-- name: Reviews By Product
-- category: INDEXING
-- difficulty: EASY
-- expected_issue: MISSING_INDEX
-- description: Filters reviews by product_id.
-- expected_fix: CREATE INDEX idx_reviews_product_id ON reviews(product_id);

SELECT *
FROM reviews
WHERE product_id = 500;