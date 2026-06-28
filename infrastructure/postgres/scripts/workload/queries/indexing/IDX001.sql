-- id: IDX001
-- name: Orders By Customer
-- category: INDEXING
-- difficulty: EASY
-- expected_issue: MISSING_INDEX
-- description: Filters orders by customer_id.
-- expected_fix: CREATE INDEX idx_orders_customer_id ON orders(customer_id);

SELECT *
FROM orders
WHERE customer_id = 100;