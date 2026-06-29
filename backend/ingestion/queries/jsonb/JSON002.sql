-- id: JSON002
-- name: Search By Country
-- category: JSONB
-- difficulty: EASY
-- expected_issue: JSONB_SCAN
-- description: Filters products by country stored inside JSON.
-- expected_fix: Create a GIN index on metadata.

SELECT *
FROM products
WHERE metadata->>'country' = 'India';