-- Constraints.sql

-- אילוץ CHECK בטבלה Employees: בדיקה שהשכר חיובי
ALTER TABLE Employees
ADD CONSTRAINT positive_salary CHECK (salary > 0);

-- אילוץ DEFAULT בטבלה Scholarship: הגדרת סכום ברירת מחדל למלגה
ALTER TABLE Scholarship
ALTER COLUMN Amount SET DEFAULT 1000.00;

-- אילוץ NOT NULL בטבלה Student: הגדרת שם פרטי כחובה
ALTER TABLE Student
ALTER COLUMN FirstName SET NOT NULL;