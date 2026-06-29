-- id: SEQ002
-- name: Customers Full Scan
-- category: SEQUENTIAL_SCAN
-- difficulty: EASY
-- expected_issue: SEQUENTIAL_SCAN
-- description: Reads every customer row.
-- expected_fix: Create an index on frequently filtered columns.

SELECT *
FROM customers;