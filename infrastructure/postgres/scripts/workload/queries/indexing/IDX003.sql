-- id: IDX003
-- name: Inventory Lookup
-- category: INDEXING
-- difficulty: MEDIUM
-- expected_issue: MISSING_INDEX
-- description: Looks up inventory by warehouse.
-- expected_fix: CREATE INDEX idx_inventory_warehouse ON inventory(warehouse_name);

SELECT *
FROM inventory
WHERE warehouse_name = 'Warehouse A';