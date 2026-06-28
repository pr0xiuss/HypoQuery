-- id: AGG004
-- name: Inventory By Warehouse
-- category: AGGREGATION
-- difficulty: MEDIUM
-- expected_issue: HASH_AGGREGATE
-- description: Calculates stock quantity for every warehouse.
-- expected_fix: Index warehouse_name if grouping becomes expensive.

SELECT
    warehouse_name,
    SUM(stock_quantity)
FROM inventory
GROUP BY warehouse_name;