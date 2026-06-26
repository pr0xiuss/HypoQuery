SELECT
    product_id,
    AVG(rating)
FROM reviews
GROUP BY product_id;