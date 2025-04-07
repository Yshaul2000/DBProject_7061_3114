# DBProject - University Financial Department Database System

## 📘 Project Report (Hebrew Below)

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
6. [Conclusion](#conclusion)

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

---

# 📘 Stage 2 – Advanced SQL Queries & Constraints

This section includes documentation and screenshots for advanced SQL queries (SELECT, DELETE, UPDATE) and constraint handling as required in Stage 2.

---

## 📊 SELECT Queries

> A total of 8 SELECT queries were implemented. Each query is described and accompanied by screenshots of the query and its result (up to 5 rows).

### 🔍 SELECT 1: Total payments per student per year
Shows how much each student paid in total each year.
![Query](images/Stage2/S1.jpg)

### 🔍 SELECT 2: Monthly income summary from payments
Calculates total income grouped by month and type of payment.
![Query](images/Stage2/S2.jpg)

### 🔍 SELECT 3: Payments in the last month
Retrieves recent payments including payment type and topic.
![Query](images/Stage2/S3.jpg)

### 🔍 SELECT 4: Departments with total budgets over 50,000
Displays departments that have received significant funding.
![Query](images/Stage2/S4.jpg)

### 🔍 SELECT 5: Employees by hire year and department
Gives insight into employees, their hiring date and salary.
![Query](images/Stage2/S5.jpg)

### 🔍 SELECT 6: Average payment amount by type
Shows statistical data about payment types.
![Query](images/Stage2/S6.jpg)

### 🔍 SELECT 7: Students receiving aid but no scholarship
Highlights financially struggling students.
![Query](images/Stage2/S7.jpg)

### 🔍 SELECT 8: Highest scholarship granted per year
Displays top scholarship per year based on approval date.
![Query](images/Stage2/S8.jpg)

---

## 🗑️ DELETE Queries

> Each DELETE query includes a description, the SQL code, and screenshots showing the database **before and after** the deletion.

### ❌ DELETE 1: Old small payments (older than 2 years, below average)
Removes outdated, small-value transactions.
![Before](images/Stage2/D1.jpg)

### ❌ DELETE 2: Employees earning between 70,000 and 90,000
Used to clean up high-salary ranges.
![Before](images/Stage2/D2.jpg)

### ❌ DELETE 3: Scholarships with low hour requirements (Cascade delete)
Requires modifying a foreign key to include ON DELETE CASCADE.
![Before](images/Stage2/D3.jpg)

---

## 🔄 UPDATE Queries

> Each UPDATE query includes the purpose, SQL code, and screenshots showing the **before and after** state of the data.

### ✏️ UPDATE 1: Reduce employee salary by 80% for low-budget departments
Targets departments with a total budget below 100,000.
![Before](images/Stage2/U1.jpg)

### ✏️ UPDATE 2: Raise scholarship by 10% based on average payments
Dynamically adjusts scholarship if payment average is higher.
![Before](images/Stage2/U2.jpg)

### ✏️ UPDATE 3: Add "israel-" prefix before '@' in student emails
Used string manipulation to improve email consistency.
![Before](images/Stage2/U3.jpg)

---

## 🔐 Constraints Using `ALTER TABLE`

> Each constraint added with `ALTER TABLE` is documented below, including an attempt to violate it and the resulting error message.

### 🔧 Constraint 1: ON DELETE CASCADE for `takes_scholarship`
Ensures that deleting a scholarship also deletes associated records in `takes_scholarship`.

#### ✔️ Alter Command
```sql
ALTER TABLE takes_scholarship
DROP CONSTRAINT takes_scholarship_scholarship_id_fkey,
ADD CONSTRAINT takes_scholarship_scholarship_id_fkey
FOREIGN KEY (scholarship_id) REFERENCES Scholarship(scholarship_id) ON DELETE CASCADE;

---


---
