-- Constraints.sql

-- אילוץ CHECK בטבלה Employees: בדיקה שהשכר חיובי
ALTER TABLE Employees
ADD CONSTRAINT positive_salary CHECK (salary > 0);

-- אילוץ DEFAULT בטבלה Payment: הגדרת סוג תשלום ברירת מחדל
ALTER TABLE Payment
ALTER COLUMN type_payment SET DEFAULT 'אחר';

-- אילוץ UNIQUE בטבלה Scholarship: בדיקה ששם המלגה ייחודי
ALTER TABLE Scholarship
ADD CONSTRAINT unique_scholarship_name UNIQUE (Name);