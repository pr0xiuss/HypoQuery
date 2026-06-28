-- id: JSON001
-- name: Search By Brand
-- category: JSONB
-- difficulty: EASY
-- expected_issue: JSONB_SCAN
-- description: Finds products by brand stored in JSON metadata.
-- expected_fix: Create a GIN index on the metadata column.

SELECT *
FROM products
WHERE metadata->>'brand' = 'Apple';