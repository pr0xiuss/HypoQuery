-- id: SEQ004
-- name: Reviews Full Scan
-- category: SEQUENTIAL_SCAN
-- difficulty: EASY
-- expected_issue: SEQUENTIAL_SCAN
-- description: Reads every review.
-- expected_fix: Create an index on search columns.

SELECT *
FROM reviews;