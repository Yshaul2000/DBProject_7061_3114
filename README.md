
# DBProject - University Financial Department Database System

## 📘 Project Report 

This project is a university financial department database management system. It was developed as part of a database course project.

### 🧑‍💻 Authors
- Amit Mordov  
- Yinon Shaul

### 🏢 Project Scope
- **System**: University Management System  
- **Unit**: Financial Department  

---

## 📌 Table of Contents
1. [Overview](#overview)
2. [ERD and DSD Diagrams](#erd-and-dsd-diagrams)
3. [Data Structure Description](#data-structure-description)
4. [Data Insertion Methods](#data-insertion-methods)
5. [Backup & Restore](#backup--restore)
6. [Stage 2 – Advanced SQL Queries & Constraints](#-stage-2--advanced-sql-queries--constraints)
   - [SELECT Queries](#select-queries)
   - [DELETE Queries](#delete-queries)
   - [UPDATE Queries](#update-queries)
   - [Constraints Using ALTER TABLE](#constraints-using-alter-table)
7. [Conclusion](#conclusion)

---

## 🧾 Overview

This database system is designed to manage the financial operations of a university. It includes data about departments, employees, budgets, students, payments, scholarships, and financial aid.

The system uses foreign keys, weak entities, and entity relationships to maintain data consistency and avoid redundancy.

---

## 🗂️ ERD and DSD Diagrams

### ERD
![ERD](images/Stage1/ERD.jpg)

### DSD
![DSD](images/Stage1/DSD.jpg)

---

## 🗃️ Data Structure Description

> Below is a summary of the main entities and their fields:

### Department  
Represents a university department.

### Employees  
- `employee_id`  
- `name`  
- `salary`  
- `hire_date`  
- `department_id` (Foreign Key)

### Budget  
- `budget_id`  
- `total_amount`  
- `budget_year`

### uses_budget  
Links budgets to departments.  
- `department_id` (FK)  
- `budget_id` (FK)

### Student  
- `StudentID`  
- `FirstName`, `LastName`, `Email`

### Payment *(Weak Entity)*  
- `payment_id`  
- `StudentID` (FK)  
- `amount`, `payment_date`, `type_payment`, `topic`

### Scholarship  
- `scholarship_id`  
- `Name`, `Amount`, `AnnualHours`

### takes_scholarship  
- `scholarship_id` (FK)  
- `StudentID` (FK)  
- `approval_date`

### Financial_Aid  
- `aid_id`  
- `aid_type`, `aid_amount`, `approval_date`, `repayment_due`

### receives_aid  
- `StudentID` (FK)  
- `aid_id` (FK)  
- `application_date`

📄 SQL table creation scripts are included in the `Stage1` folder.

---

## 📥 Data Insertion Methods

### ✅ Method A: Python Script  
![Python Script](images/Stage1/student.jpg)

### ✅ Method B: Mockaroo Generator  
![Mockaroo](images/Stage1/mockaroo_Financial_Aid.jpg)

### ✅ Method C: Generatedata  
![Generatedata](images/Stage1/generatedata_Budget.jpg)

---

## 💾 Backup & Restore

### Backup  
![Backup](images/Stage1/Backup_success.jpg)

### Restore  
![Restore](images/Stage1/Restore_success.jpg)

---

# 📘 Stage 2 – Advanced SQL Queries & Constraints

This section includes documentation and screenshots for advanced SQL queries (SELECT, DELETE, UPDATE) and constraint handling as required in Stage 2.

---

## 📊 SELECT Queries

> A total of 8 SELECT queries were implemented. Each query is described and accompanied by screenshots.

### 🔍 SELECT 1: Total payments per student per year
![Query](images/Stage2/S1.jpg)

### 🔍 SELECT 2: Monthly income summary from payments
![Query](images/Stage2/S2.jpg)

### 🔍 SELECT 3: Payments in the last month
![Query](images/Stage2/S3.jpg)

### 🔍 SELECT 4: Departments with total budgets over 50,000
![Query](images/Stage2/S4.jpg)

### 🔍 SELECT 5: Employees by hire year and department
![Query](images/Stage2/S5.jpg)

### 🔍 SELECT 6: Average payment amount by type
![Query](images/Stage2/S6.jpg)

### 🔍 SELECT 7: Students receiving aid but no scholarship
![Query](images/Stage2/S7.jpg)

### 🔍 SELECT 8: Highest scholarship granted per year
![Query](images/Stage2/S8.jpg)

---

## 🗑️ DELETE Queries

### ❌ DELETE 1: Remove old small payments
```sql
DELETE FROM Payment
WHERE payment_date < CURRENT_DATE - INTERVAL '2 years'
  AND amount < (
      SELECT AVG(p2.amount)
      FROM Payment p2
      WHERE p2.type_payment = Payment.type_payment
  );
```
![Before](images/Stage2/D1.jpg)

### ❌ DELETE 2: Delete employees with salary between 70,000 and 90,000
```sql
DELETE FROM Employees
WHERE salary between 70000 and 90000;
```
![Before](images/Stage2/D2.jpg)

### ❌ DELETE 3: Delete scholarships with low hour requirements
```sql
ALTER TABLE takes_scholarship
DROP CONSTRAINT takes_scholarship_scholarship_id_fkey,
ADD CONSTRAINT takes_scholarship_scholarship_id_fkey
FOREIGN KEY (scholarship_id) REFERENCES Scholarship(scholarship_id) ON DELETE CASCADE;

DELETE FROM Scholarship
WHERE AnnualHours < 90;
```
![Before](images/Stage2/D3.jpg)

---

## 🔄 UPDATE Queries

### ✏️ UPDATE 1: Reduce salary by 80% in low-budget departments
```sql
UPDATE Employees
SET salary = salary * 0.2
WHERE department_id IN (
    SELECT ub.department_id
    FROM uses_budget ub
    JOIN Budget b ON ub.budget_id = b.budget_id
    GROUP BY ub.department_id
    HAVING SUM(b.total_amount) < 100000
);
```
![Before](images/Stage2/U1.jpg)

### ✏️ UPDATE 2: Raise scholarship by 10% if payment average is higher
```sql
UPDATE Scholarship
SET Amount = CASE
    WHEN (SELECT AVG(p.amount)
          FROM Payment p
          JOIN takes_scholarship ts ON p.StudentID = ts.StudentID
          WHERE ts.scholarship_id = Scholarship.scholarship_id) > Scholarship.Amount
    THEN Scholarship.Amount * 1.1
    ELSE Scholarship.Amount
END;
```
![Before](images/Stage2/U2.jpg)

### ✏️ UPDATE 3: Add prefix "israel-" before email @ sign
```sql
UPDATE Student
SET Email = SUBSTRING(Email, 1, POSITION('@' IN Email) - 1) || 'israel-' || SUBSTRING(Email, POSITION('@' IN Email), LENGTH(Email))
WHERE Email NOT LIKE '%israel-%';
```
![Before](images/Stage2/U3.jpg)

---

## 🔐 Constraints Using `ALTER TABLE`

### 🔧 Constraint 1: ON DELETE CASCADE for `takes_scholarship`
```sql
ALTER TABLE takes_scholarship
DROP CONSTRAINT takes_scholarship_scholarship_id_fkey,
ADD CONSTRAINT takes_scholarship_scholarship_id_fkey
FOREIGN KEY (scholarship_id) REFERENCES Scholarship(scholarship_id) ON DELETE CASCADE;
```
![Constraint](images/Stage2/Constraints1.jpg)

### 🔧 Constraint 2: CHECK constraint on positive salary
```sql
ALTER TABLE Employees
ADD CONSTRAINT positive_salary CHECK (salary > 0);
```
![Constraint](images/Stage2/C1.jpg)

### 🔧 Constraint 3: DEFAULT value for scholarship amount
```sql
ALTER TABLE Scholarship
ALTER COLUMN Amount SET DEFAULT 1000.00;
```
![Constraint](images/Stage2/C3.jpg)


### 🔧 Constraint 4: NOT NULL for student first name
```sql
ALTER TABLE Student
ALTER COLUMN FirstName SET NOT NULL;
```

---

## ✅ Conclusion

This project successfully demonstrates the design, implementation, and operation of a financial management database system for a university. Throughout the two project stages, we:

- Designed a normalized relational database with ERD & DSD diagrams.
- Implemented and populated the database using scripts and data generators.
- Performed complex SQL operations including data analysis (SELECT), maintenance (UPDATE/DELETE), and constraint handling.
- Demonstrated robust backup and recovery procedures.

We gained deep insight into database modeling, query optimization, and real-world data operations.

---
