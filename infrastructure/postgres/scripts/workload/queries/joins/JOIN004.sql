-- id: JOIN004
-- name: Inventory Products
-- category: JOIN
-- difficulty: EASY
-- expected_issue: HASH_JOIN
-- description: Joins inventory with products.
-- expected_fix: Index product_id.

SELECT
    p.product_name,
    i.stock_quantity,
    i.warehouse_name
FROM inventory i
JOIN products p
ON i.product_id = p.product_id;