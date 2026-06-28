-- id: JSON005
-- name: Products With Features
-- category: JSONB
-- difficulty: HARD
-- expected_issue: JSONB_SCAN
-- description: Searches products containing a features array.
-- expected_fix: Use a GIN index for containment operations.

SELECT *
FROM products
WHERE metadata ? 'features';