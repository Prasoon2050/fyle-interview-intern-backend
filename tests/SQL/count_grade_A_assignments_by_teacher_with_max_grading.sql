-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
WITH teacher_grades AS (
    SELECT 
        teacher_id, 
        COUNT(*) as total_assignments,
        SUM(CASE WHEN grade = 'A' THEN 1 ELSE 0 END) as grade_A_count
    FROM 
        assignments
    WHERE 
        state = 'GRADED'
    GROUP BY 
        teacher_id
),
max_teacher AS (
    SELECT 
        teacher_id
    FROM 
        teacher_grades
    ORDER BY 
        total_assignments DESC
    LIMIT 1
)
SELECT 
    grade_A_count
FROM 
    teacher_grades
JOIN 
    max_teacher ON teacher_grades.teacher_id = max_teacher.teacher_id;
