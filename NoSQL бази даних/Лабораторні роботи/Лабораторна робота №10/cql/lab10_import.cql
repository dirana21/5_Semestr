COPY lab10_university_v5.students
  (student_id, full_name, email, variant, city)
FROM 'students.csv'
WITH HEADER = TRUE;
