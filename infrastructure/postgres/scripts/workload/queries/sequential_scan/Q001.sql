-- id: SEQ001
-- name: Products Full Scan
-- category: SEQUENTIAL_SCAN
-- difficulty: EASY
-- expected_issue: SEQUENTIAL_SCAN
-- description: Reads the complete products table.
-- expected_fix: Create an index on frequently filtered columns.

SELECT *
FROM products;