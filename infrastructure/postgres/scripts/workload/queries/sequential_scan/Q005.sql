-- id: SEQ005
-- name: Product Events Full Scan
-- category: SEQUENTIAL_SCAN
-- difficulty: EASY
-- expected_issue: SEQUENTIAL_SCAN
-- description: Reads every product event.
-- expected_fix: Create an index on filtering columns.

SELECT *
FROM product_events;