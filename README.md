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
   - [Rollback & Commit Transactions](#rollback--commit-transactions)
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

<br><br>

# 📘 Stage 2 – Advanced SQL Queries & Constraints

This section includes documentation and screenshots for advanced SQL queries (SELECT, DELETE, UPDATE) and constraint handling as required in Stage 2.

---

## 📊 SELECT Queries

> A total of 8 SELECT queries were implemented. Each query is described and accompanied by screenshots.

### 🔍 SELECT 1: Total payments per student per year

📘 **Background**: A student once requested a refund, claiming they paid twice. Investigation revealed the finance office lacked a clear annual payment summary per student.  
✅ **Benefit**: This report helps the finance department track student income, detect anomalies or duplicates, and give accurate responses to student inquiries.

![Query](images/Stage2/S1.jpg)

### 🔍 SELECT 2: Monthly income summary from payments

📘 **Background**: As the quarter ended, the university's management requested a summarized monthly income report to monitor cash flow.  
✅ **Benefit**: Enables budget planning and helps evaluate financial stability month by month.

![Query](images/Stage2/S2.jpg)

### 🔍 SELECT 3: Payments in the last month

📘 **Background**: A new online payment system was launched. The administration wanted to assess how many students actually used it in the last month.  
✅ **Benefit**: Tracks adoption of the new platform and allows real-time financial activity monitoring.

![Query](images/Stage2/S3.jpg)

### 🔍 SELECT 4: Departments with total budgets over 50,000

📘 **Background**: A department complained of unequal funding. The administration needed a clear comparison of budgets between departments.  
✅ **Benefit**: Helps identify well-funded departments and supports a fair reallocation of resources.

![Query](images/Stage2/S4.jpg)

### 🔍 SELECT 5: Employees by hire year and department

📘 **Background**: HR wanted insights into which departments had large hiring waves and in which years.  
✅ **Benefit**: Supports workforce planning and helps predict future hiring needs.

![Query](images/Stage2/S5.jpg)

### 🔍 SELECT 6: Average payment amount by type

📘 **Background**: The finance office wanted to compare types of student payments — for example, course fees vs. administrative charges.  
✅ **Benefit**: Helps assess pricing strategy and reveals key income sources.

![Query](images/Stage2/S6.jpg)

### 🔍 SELECT 7: Students receiving aid but no scholarship

📘 **Background**: Aid requests were rising. The administration wanted to identify students receiving financial aid who might also qualify for scholarships but hadn't applied.  
✅ **Benefit**: Allows targeted outreach and better scholarship utilization to reduce aid dependency.

![Query](images/Stage2/S7.jpg)

### 🔍 SELECT 8: Highest scholarship granted per year

📘 **Background**: The student newspaper requested information about the highest awarded scholarships per year.  
✅ **Benefit**: Promotes transparency and encourages students to apply for high-value scholarships.

![Query](images/Stage2/S8.jpg)

---

<br>

## 🗑️ DELETE Queries

### ❌ DELETE 1: Remove old small payments

📘 **Background**: During database backup, it was discovered that the Payment table held outdated and low-value data no longer needed.  
✅ **Benefit**: Cleaning old data improves performance and reduces storage overhead.

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

📘 **Background**: An internal audit flagged a suspicious salary range (70k–90k) for employees with unclear roles.  
✅ **Benefit**: Quickly removes potentially fraudulent or incorrect employee entries during a cleanup phase.

```sql
DELETE FROM Employees
WHERE salary between 70000 and 90000;
```
![Before](images/Stage2/D2.jpg)

### ❌ DELETE 3: Delete scholarships with low hour requirements

📘 **Background**: Scholarships with fewer than 90 annual service hours were deemed ineffective in terms of student contribution.  
✅ **Benefit**: Ensures every scholarship involves a minimum amount of community service and provides better impact.

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

<br>

## 🔄 UPDATE Queries

### ✏️ UPDATE 1: Reduce salary by 80% in low-budget departments

📘 **Background**: Budget cuts were applied in several departments. Instead of layoffs, the university opted to reduce salaries in underfunded departments.  
✅ **Benefit**: Maintains employment while staying within budgetary limits.

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

📘 **Background**: Students receiving scholarships were still paying more than their awarded amount on average.  
✅ **Benefit**: Ensures scholarship values are adjusted to match actual educational expenses, promoting equity.

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

📘 **Background**: Due to integration with a new government verification system, all student emails had to include the "israel-" prefix before the @ symbol.  
✅ **Benefit**: Ensures email addresses conform to new national digital ID systems.

```sql
UPDATE Student
SET Email = SUBSTRING(Email, 1, POSITION('@' IN Email) - 1) || 'israel-' || SUBSTRING(Email, POSITION('@' IN Email), LENGTH(Email))
WHERE Email NOT LIKE '%israel-%';
```
![Before](images/Stage2/U3.jpg)

---

<br>

## 🔄 Rollback & Commit Transactions

### 🔙 Rollback Transaction

📘 **Background**: Due to a recent cyberattack on Israel's national systems, all updates involving sensitive data were temporarily suspended. As part of this response, the decision was made to rollback any changes to student email addresses, including the modification that was intended to prepend "israel-" to student emails.  
✅ **Benefit**: This ensures that no unintended changes were made to critical contact information, maintaining the integrity and security of the university's student database.

```sql
-- Start of rollback transaction
BEGIN;

-- Perform the update (add 'israel-' before '@' in emails)
UPDATE Student
SET Email = SUBSTRING(Email, 1, POSITION('@' IN Email) - 1) || 'israel-' || SUBSTRING(Email, POSITION('@' IN Email), LENGTH(Email))
WHERE Email NOT LIKE '%israel-%';

-- Check current state after update (before rollback)
SELECT StudentID, Email FROM Student WHERE Email LIKE '%israel-%';

-- Rollback the transaction to undo the update
ROLLBACK;

-- Check state again to confirm emails returned to original form
SELECT StudentID, Email FROM Student WHERE Email NOT LIKE '%israel-%';
```
![Rollback](images/Stage2/Rollback.jpg)

### ✅ Commit Transaction

📘 **Background**: In celebration of Israel's 77th Independence Day, the government has decided that for students receiving scholarships, if their required volunteer hours are exactly 77, an additional 77 NIS will be added to their scholarship amount.  
✅ **Benefit**: This update ensures that students who meet this specific criteria are rewarded appropriately, aligning the university's scholarship policies with the national initiative.

```sql
-- Start of commit transaction
BEGIN;

-- Update: Add 77 NIS to the Amount of scholarships with exactly 77 AnnualHours
UPDATE Scholarship
SET Amount = Amount + 77
WHERE AnnualHours = 77;

-- Preview: See the scholarships that were updated BEFORE committing
SELECT scholarship_id, Name, Amount, AnnualHours
FROM Scholarship
WHERE AnnualHours = 77;

-- Finalize the update
COMMIT;

-- Confirm the changes AFTER committing
SELECT scholarship_id, Name, Amount, AnnualHours
FROM Scholarship
WHERE AnnualHours = 77;
```
![Commit](images/Stage2/Commit.jpg)

---

## 🔧 Constraints Using ALTER TABLE

### 🔧 Constraint 1: CHECK constraint on positive salary
```sql
ALTER TABLE Employees
ADD CONSTRAINT positive_salary CHECK (salary > 0);
```
![Constraint](images/Stage2/Constraints1.jpg)

### 🔧 Constraint 2: DEFAULT value for scholarship amount
```sql
ALTER TABLE Scholarship
ALTER COLUMN Amount SET DEFAULT 1000.00;
```
![Constraint](images/Stage2/C2.jpg)


### 🔧 Constraint 3: NOT NULL for student first name
```sql
ALTER TABLE Student
ALTER COLUMN FirstName SET NOT NULL;
```
![Constraint](images/Stage2/C3.jpg)

---

<br><br>

# 🔗 Stage 3 – Data Integration Phase

This section documents the integration process between the **local financial system** and the **remote dormitory management database**, including schema updates, foreign table handling, and data merging operations.

---

## 🗂️ ERD and DSD Diagrams

### ERD (Updated – Integrated)
![ERD](images/Stage3/ERD_updated.jpg)

### DSD (Updated – Integrated)
![DSD](images/Stage3/DSD_updated.jpg)

---

## 🧠 Integration Decisions

- Integration was done using PostgreSQL's `postgres_fdw` foreign data wrapper to allow direct querying of the remote database.
- Remote tables were **mirrored** as foreign tables in the local database, then copied into newly created local tables.
- Student data was merged using a **+400 ID offset** to avoid primary key collisions.
- New columns were added to the `Student` table to accommodate remote attributes like gender, phone, and major.
- Foreign tables were **dropped after integration** for cleanliness and security.

---

## 📝 Integration Process and SQL Commands

> The following key SQL commands were used in the integration process. Each command includes a short explanation of what it does and why it was used.

### 1. Enable the Foreign Data Wrapper

This extension allows PostgreSQL to access tables from another PostgreSQL database.

```sql
CREATE EXTENSION IF NOT EXISTS postgres_fdw;
```

---

### 2. Define the Connection to the Remote Server

This command creates a server definition pointing to the external group project database.

```sql
CREATE SERVER group_db_server
FOREIGN DATA WRAPPER postgres_fdw
OPTIONS (host 'localhost', dbname 'Group_database', port '5432');
```

---

### 3. Create User Mapping for Authentication

This defines how your local user will connect to the remote database (replace credentials as needed).

```sql
CREATE USER MAPPING FOR current_user
SERVER group_db_server
OPTIONS (user 'yshaul@g.jct.ac.il', password '5TxJQ5zC');
```

---

### 4. Access the Remote Student Table

A foreign table is created that represents the `student` table in the remote database.

```sql
CREATE FOREIGN TABLE student_remote (
    studentid INTEGER,
    firstname VARCHAR(50),
    lastname VARCHAR(50),
    gender gender_type,
    dateofbirth DATE,
    enrollmentdate DATE,
    phonenumber VARCHAR(16),
    email VARCHAR(50),
    major major_type
) SERVER group_db_server
OPTIONS (schema_name 'public', table_name 'student');
```

---

### 5. Modify Local Student Table

Add new columns to support integration with the remote student table.

```sql
ALTER TABLE Student
ADD COLUMN gender gender_type,
ADD COLUMN dateofbirth DATE,
ADD COLUMN enrollmentdate DATE,
ADD COLUMN phonenumber VARCHAR(16),
ADD COLUMN major major_type;
```

You can populate these new fields with dummy/random values using the following logic:

```sql
UPDATE Student
SET
    gender = (CASE WHEN random() < 0.5 THEN 'Male' ELSE 'Female' END)::gender_type_new,
    dateofbirth = CURRENT_DATE - interval '1 year' * (18 + random() * 12),
    enrollmentdate = CURRENT_DATE - interval '1 year' * (random() * 5),
    phonenumber = '+972 ' || lpad(floor(random() * 99)::text, 2, '0') || '-' ||
                  lpad(floor(random() * 999)::text, 3, '0') || '-' ||
                  lpad(floor(random() * 9999)::text, 4, '0'),
    major = (CASE WHEN random() < 0.5 THEN 'Computer Science' ELSE 'Biology' END)::major_type;
```

---

### 6. Integrate Student Data

This inserts remote students into the local `Student` table, offsetting the IDs by 400.

```sql
INSERT INTO Student (StudentID, FirstName, LastName, Email, gender, dateofbirth, enrollmentdate, phonenumber, major)
SELECT studentid + 400, firstname, lastname, email, gender, dateofbirth, enrollmentdate, phonenumber, major
FROM student_remote;
```

---

### 7. Integrate Dormitory Management Tables

For each of the following tables, the process includes:

1. Creating a foreign table.
2. Creating a local table.
3. Copying data via `INSERT INTO ... SELECT ...`.

These tables include:

- Dorm_Management
- Building
- Apartment
- Room
- Lease
- Rental
- Maintenance_Request

Each of these was fully migrated using foreign table access followed by local storage and relational constraints.

---

### 8. Clean-Up

After data was successfully copied, all foreign tables were dropped to finalize the integration.

```sql
DROP FOREIGN TABLE apartment_remote;
DROP FOREIGN TABLE building_remote;
DROP FOREIGN TABLE dorm_management_remote;
DROP FOREIGN TABLE lease_remote;
DROP FOREIGN TABLE maintenance_request_remote;
DROP FOREIGN TABLE rental_remote;
DROP FOREIGN TABLE room_remote;
DROP FOREIGN TABLE student_remote;
```

---

## ✅ Conclusion

In this integration stage, we:

- Connected two separate databases using PostgreSQL foreign data wrappers.
- Merged student and dormitory information into the financial system.
- Ensured data consistency and normalized design through referential integrity.
- Demonstrated advanced SQL skills with DDL, DML, and data synchronization logic.

This provides a comprehensive, scalable university database system.

---

## ✅ Conclusion

This project successfully demonstrates the design, implementation, and operation of a financial management database system for a university. Throughout the two project stages, we:

- Designed a normalized relational database with ERD & DSD diagrams.
- Implemented and populated the database using scripts and data generators.
- Performed complex SQL operations including data analysis (SELECT), maintenance (UPDATE/DELETE), and constraint handling.
- Demonstrated robust backup and recovery procedures.
- Implemented transaction control with COMMIT and ROLLBACK operations to maintain data integrity.

We gained deep insight into database modeling, query optimization, and real-world data operations.

---
