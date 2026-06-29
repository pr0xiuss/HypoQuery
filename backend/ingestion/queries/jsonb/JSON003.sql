-- id: JSON003
-- name: Search By Warranty
-- category: JSONB
-- difficulty: MEDIUM
-- expected_issue: JSONB_SCAN
-- description: Filters products having a warranty field.
-- expected_fix: Use a GIN index for JSON existence queries.

SELECT *
FROM products
WHERE metadata ? 'warranty';