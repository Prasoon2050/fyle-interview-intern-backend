-- Write query to get number of assignments for each state
SELECT state, COUNT(*) as count
FROM assignments
GROUP BY state;


