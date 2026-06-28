-- id: SORT003
-- name: Reviews By Rating
-- category: SORTING
-- difficulty: EASY
-- expected_issue: SORT
-- description: Sorts reviews by rating.
-- expected_fix: Create an index on rating when sorting is common.

SELECT *
FROM reviews
ORDER BY rating DESC;