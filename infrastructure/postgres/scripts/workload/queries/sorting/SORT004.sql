-- id: SORT004
-- name: Customers By Last Name
-- category: SORTING
-- difficulty: MEDIUM
-- expected_issue: SORT
-- description: Sorts customers alphabetically by last name.
-- expected_fix: Create an index on last_name.

SELECT *
FROM customers
ORDER BY last_name;