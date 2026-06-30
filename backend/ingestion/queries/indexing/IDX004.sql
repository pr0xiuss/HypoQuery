-- id: IDX004
-- name: Product Category Lookup
-- category: INDEXING
-- difficulty: MEDIUM
-- expected_issue: MISSING_INDEX
-- description: Filters products by category.
-- expected_fix: CREATE INDEX idx_products_category ON products(category);

SELECT *
FROM products
WHERE category = 'Electronics';