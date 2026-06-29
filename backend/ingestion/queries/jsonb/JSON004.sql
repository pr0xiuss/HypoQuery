-- id: JSON004
-- name: Premium Products
-- category: JSONB
-- difficulty: MEDIUM
-- expected_issue: JSONB_SCAN
-- description: Finds premium products stored inside JSON metadata.
-- expected_fix: Add a GIN index on metadata.

SELECT *
FROM products
WHERE metadata->>'tier' = 'Premium';