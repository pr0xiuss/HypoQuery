-- id: SEQ003
-- name: Orders Full Scan
-- category: SEQUENTIAL_SCAN
-- difficulty: EASY
-- expected_issue: SEQUENTIAL_SCAN
-- description: Reads the entire orders table.
-- expected_fix: Create an index on commonly filtered fields.

SELECT *
FROM orders;