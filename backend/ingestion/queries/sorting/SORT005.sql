-- id: SORT005
-- name: Product Events Latest First
-- category: SORTING
-- difficulty: MEDIUM
-- expected_issue: SORT
-- description: Retrieves the latest product events.
-- expected_fix: Create an index on created_at.

SELECT *
FROM product_events
ORDER BY created_at DESC;