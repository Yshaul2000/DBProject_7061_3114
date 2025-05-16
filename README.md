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



# 🔗 Stage 3 – Data Integration Phase

📜 This stage focuses on integrating the Financial Department database with the Dormitory Management database, a key aspect of the university management system. The goal is to create a unified database that allows for a comprehensive view of student-related information, including financial and residential data.
---

## 🗂️ ERD and DSD Diagrams

### ERD (Finansi)
![ERD](images/Stage3/ERD.jpg)

### DSD (Finansi)
![DSD](images/Stage3/DSD.jpg)

### ERD (Dormitory)
![ERD](images/Stage3/Dormitory_erd.jpg)

### DSD (Dormitory)
![DSD](images/Stage3/Dormitory_dsd.jpg)

### ERD (Integration)
![ERD](images/Stage3/merge_erd.jpg)

### DSD (Integration)
![DSD](images/Stage3/merge_dsd.jpg)
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

This section contains the complete SQL integration script used in Stage 3 of the project, with all commands and comments fully preserved and documented.

---

```sql
-- 1. Create the postgres_fdw extension if it doesn't exist.
--    This extension is required to work with foreign tables in PostgreSQL.
CREATE EXTENSION IF NOT EXISTS postgres_fdw;

-- 2. Create a server object that defines the connection to the remote database.
CREATE SERVER group_db_server
FOREIGN DATA WRAPPER postgres_fdw
OPTIONS (host 'localhost', dbname 'Group_database', port '5432');

-- 3. Create a user mapping to specify the credentials for accessing the remote server.
--    Replace 'yshaul@g.jct.ac.il' and '5TxJQ5zC' with the actual username and password.
--    'current_user' refers to the user executing this command on the local database.
CREATE USER MAPPING FOR current_user
SERVER group_db_server
OPTIONS (user 'yshaul@g.jct.ac.il', password '5TxJQ5zC');

------------------------------------
-- 4. Create a foreign table in the local database that represents the 'student' table in the remote database.
--    This foreign table acts as a local interface to the remote table, enabling data integration.
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

-- Select all data from the foreign table to verify the connection and data retrieval.
SELECT * FROM student_remote;

----------------------------------------------------------------------
-- Alter the existing 'Student' table in the local database to add new columns.
--    These columns are added to facilitate data integration between the 'Student' tables
--    located in both the local and remote databases.
ALTER TABLE Student
ADD COLUMN gender gender_type,
ADD COLUMN dateofbirth DATE,
ADD COLUMN enrollmentdate DATE,
ADD COLUMN phonenumber VARCHAR(16),
ADD COLUMN major major_type;

-- Update the 'Student' table with randomly generated data for the new columns.
--    This assumes you want to populate these columns with some data for testing or initial setup.
--    If you intend to insert specific data from the remote table, the subsequent INSERT statement will handle that.
UPDATE Student
SET
    gender = (CASE WHEN random() < 0.5 THEN 'Male' ELSE 'Female' END)::gender_type_new,
    dateofbirth = CURRENT_DATE - interval '1 year' * (18 + random() * 12),
    enrollmentdate = CURRENT_DATE - interval '1 year' * (random() * 5),
    phonenumber = '+972 ' || lpad(floor(random() * 99)::text, 2, '0') || '-' ||
                  lpad(floor(random() * 999)::text, 3, '0') || '-' ||
                  lpad(floor(random() * 9999)::text, 4, '0'),
    major = (CASE WHEN random() < 0.5 THEN 'Computer Science' ELSE 'Biology' END)::major_type;

-- Select all data from the 'Student' table to view the updated data.
SELECT * FROM Student;


-- Integration note:
-- During the integration phase, the student tables from the remote and local databases are being merged.
-- Decisions are being made to ensure data integrity and prevent overwriting of existing information.
INSERT INTO Student (StudentID, FirstName, LastName, Email, gender, dateofbirth, enrollmentdate, phonenumber, major)
SELECT studentid + 400, firstname, lastname, email, gender, dateofbirth, enrollmentdate, phonenumber, major
FROM student_remote;

-- Select all data from the 'Student' table to view the data after the integration attempt.
SELECT * FROM Student;


-- 5. Creating all tables that do not have a direct relationship, such as FK, to the Student table
-- that is shared by both primary tables, by creating a foreign table, followed by a local table,
--and copying the contents to it

-- 6.  Create a foreign table for the 'Dorm_Management' table in the remote database.
--     This allows you to access dorm management information from the remote server.
CREATE FOREIGN TABLE dorm_Management_remote (
    ManagerID INT,
    FullName VARCHAR(100) NOT NULL,
    PhoneNumber VARCHAR(16) NOT NULL,
    Email VARCHAR(50) NOT NULL,
    HireDate DATE NOT NULL
) SERVER group_db_server
OPTIONS (schema_name 'public', table_name 'dorm_management');

-- Create the Dorm_Management table
CREATE TABLE Dorm_Management (
    ManagerID INT PRIMARY KEY,
    FullName VARCHAR(100) NOT NULL,
	PhoneNumber VARCHAR(16) NOT NULL CHECK (PhoneNumber ~ '^\+972 5[0-9]-[0-9]{3}-[0-9]{4}$'),
    Email VARCHAR(50) NOT NULL CHECK (Email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    HireDate DATE NOT NULL
);

INSERT INTO Dorm_Management (ManagerID, FullName, PhoneNumber, Email, HireDate)
SELECT ManagerID, FullName, PhoneNumber, Email, HireDate
FROM dorm_Management_remote;

-- Verify the data in the local 'Dorm_Management' table.
SELECT * FROM Dorm_Management ;


-- 7. Create a foreign table for the 'Building' table in the remote database.
--     This allows you to access building information from the remote server.
CREATE FOREIGN TABLE building_remote (
    BuildingID INT,
    BuildingName VARCHAR(100) NOT NULL,
    Address VARCHAR(100) NOT NULL,
    MaxApartments INT NOT NULL,
    ManagerID INT NOT NULL
) SERVER group_db_server
OPTIONS (schema_name 'public', table_name 'building');

-- Create the Building table
CREATE TABLE Building (
    BuildingID INT PRIMARY KEY,
    BuildingName VARCHAR(100) NOT NULL,
    Address VARCHAR(100) NOT NULL,
    MaxApartments INT NOT NULL CHECK (MaxApartments > 0),
    ManagerID INT NOT NULL,
    FOREIGN KEY (ManagerID) REFERENCES Dorm_Management(ManagerID)
);

-- Copy data from the remote 'building' table to the local 'Building' table.
INSERT INTO Building (BuildingID, BuildingName, Address, MaxApartments, ManagerID)
SELECT BuildingID, BuildingName, Address, MaxApartments, ManagerID
FROM building_remote;

-- Verify the data in the local 'Building' table.
SELECT * FROM Building;


-- 8. Create a foreign table for the 'Apartment' table in the remote database.
--     This allows you to access apartment information from the remote server.
CREATE FOREIGN TABLE apartment_remote (
    ApartmentID INT NOT NULL,
    BuildingID INT NOT NULL,
    RoomCapacity INT NOT NULL,
    FloorNumber INT NOT NULL,
    MaxRooms INT NOT NULL
) SERVER group_db_server
OPTIONS (schema_name 'public', table_name 'apartment');

-- Create the Apartment table
CREATE TABLE Apartment (
    ApartmentID INT NOT NULL,
    BuildingID INT NOT NULL,
    RoomCapacity INT NOT NULL CHECK (RoomCapacity > 0),
    FloorNumber INT NOT NULL,
    MaxRooms INT NOT NULL CHECK (MaxRooms > 0),
    PRIMARY KEY (ApartmentID, BuildingID),
    FOREIGN KEY (BuildingID) REFERENCES Building(BuildingID)
);

-- Copy data from the remote 'apartment' table to the local 'Apartment' table.
INSERT INTO Apartment (ApartmentID, BuildingID, RoomCapacity, FloorNumber, MaxRooms)
SELECT ApartmentID, BuildingID, RoomCapacity, FloorNumber, MaxRooms
FROM apartment_remote;

-- Verify the data in the local 'Apartment' table.
SELECT * FROM Apartment;


-- 9. Create a foreign table for the 'Room' table in the remote database.
--     This allows you to access room information from the remote server.
CREATE FOREIGN TABLE room_remote (
    RoomID INT NOT NULL,
    MaxPeople INT NOT NULL,
    HasBalcony BOOLEAN NOT NULL,
    ApartmentID INT NOT NULL,
    BuildingID INT NOT NULL
) SERVER group_db_server
OPTIONS (schema_name 'public', table_name 'room');

-- Create the Room table
CREATE TABLE Room (
    RoomID INT PRIMARY KEY,
    MaxPeople INT NOT NULL CHECK (MaxPeople > 0),
    HasBalcony BOOLEAN NOT NULL,
    ApartmentID INT NOT NULL,
    BuildingID INT NOT NULL,
    FOREIGN KEY (ApartmentID, BuildingID) REFERENCES Apartment(ApartmentID, BuildingID)
);

-- Copy data from the remote 'room' table to the local 'Room' table.
INSERT INTO Room (RoomID, MaxPeople, HasBalcony, ApartmentID, BuildingID)
SELECT RoomID, MaxPeople, HasBalcony, ApartmentID, BuildingID
FROM room_remote;

-- Verify the data in the local 'Room' table.
SELECT * FROM Room;


-- 10. Create a foreign table for the 'Lease' table in the remote database.
--     This allows you to access lease information from the remote server.
CREATE FOREIGN TABLE lease_remote (
    LeaseID INT NOT NULL,
    ContractDate DATE NOT NULL,
    DiscountPercent DECIMAL(5, 2) NOT NULL,
    ManagerID INT NOT NULL
) SERVER group_db_server
OPTIONS (schema_name 'public', table_name 'lease');

-- Create the Lease table
CREATE TABLE Lease (
    LeaseID SERIAL PRIMARY KEY,
    ContractDate DATE NOT NULL,
    DiscountPercent DECIMAL(5, 2) NOT NULL CHECK (DiscountPercent >= 0 AND DiscountPercent <= 100),
    ManagerID INT NOT NULL,
    FOREIGN KEY (ManagerID) REFERENCES Dorm_Management(ManagerID)
);

-- Copy data from the remote 'lease' table to the local 'Lease' table.
INSERT INTO Lease (LeaseID, ContractDate, DiscountPercent, ManagerID)
SELECT LeaseID, ContractDate, DiscountPercent, ManagerID
FROM lease_remote;

-- Verify the data in the local 'Lease' table.
SELECT * FROM Lease;


---------------
-- 11. Note: The following tables ('rental_remote' and 'maintenance_request_remote')
-- are being created as foreign tables and are assumed to have a foreign key
-- relationship to the 'student' table in the remote database.

-- 12. Create a foreign table for the 'Rental' table in the remote database.
--     This allows you to access rental information from the remote server.
CREATE FOREIGN TABLE rental_remote (
    StudentID INT NOT NULL,
    RoomID INT NOT NULL,
    LeaseID INT NOT NULL,
    CheckInDate DATE NOT NULL,
    CheckOutDate DATE NOT NULL
) SERVER group_db_server
OPTIONS (schema_name 'public', table_name 'rental');

-- Create the Rental table
CREATE TABLE Rental (
    StudentID INT NOT NULL,
    RoomID INT NOT NULL,
    LeaseID INT NOT NULL,
    CheckInDate DATE NOT NULL,
    CheckOutDate DATE NOT NULL CHECK (CheckOutDate > CheckInDate),
    PRIMARY KEY (StudentID, RoomID, LeaseID),
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID),
    FOREIGN KEY (RoomID) REFERENCES Room(RoomID),
    FOREIGN KEY (LeaseID) REFERENCES Lease(LeaseID)
);

-- Copy data from the remote 'rental' table to the local 'Rental' table.
INSERT INTO Rental (StudentID, RoomID, LeaseID, CheckInDate, CheckOutDate)
SELECT StudentID, RoomID, LeaseID, CheckInDate, CheckOutDate
FROM rental_remote;

-- Verify the data in the local 'Rental' table.
SELECT * FROM Rental;


-- 13. Create a foreign table for the 'Maintenance_Request' table in the remote database.
--     This allows you to access maintenance request information from the remote server.
CREATE FOREIGN TABLE maintenance_request_remote (
    RequestID INT NOT NULL,
    IssueDescription TEXT NOT NULL,
    RequestDate DATE NOT NULL,
    ResolvedDate DATE,
    Priority VARCHAR(50) NOT NULL, -- Assuming priority_type is a VARCHAR in the remote table
    ManagerID INT NOT NULL,
    StudentID INT,
    RoomID INT,
    LeaseID INT
) SERVER group_db_server
OPTIONS (schema_name 'public', table_name 'maintenance_request');

-- Create the Maintenance_Request table
CREATE TABLE Maintenance_Request (
    RequestID INT PRIMARY KEY,
    IssueDescription TEXT NOT NULL,
    RequestDate DATE NOT NULL,
    ResolvedDate DATE,
    Priority priority_type NOT NULL,
    ManagerID INT NOT NULL,
    StudentID INT,
    RoomID INT,
    LeaseID INT,
    FOREIGN KEY (ManagerID) REFERENCES Dorm_Management(ManagerID),
    FOREIGN KEY (StudentID, RoomID, LeaseID) REFERENCES Rental(StudentID, RoomID, LeaseID),
    CHECK (ResolvedDate IS NULL OR ResolvedDate >= RequestDate)
);

-- Copy data from the remote 'maintenance_request' table to the local 'Maintenance_Request' table.
INSERT INTO Maintenance_Request (RequestID, IssueDescription, RequestDate, ResolvedDate, Priority, ManagerID, StudentID, RoomID, LeaseID)
SELECT RequestID, IssueDescription, RequestDate, ResolvedDate, Priority::priority_type, ManagerID, StudentID, RoomID, LeaseID
FROM maintenance_request_remote;

-- Verify the data in the local 'Maintenance_Request' table.
SELECT * FROM Maintenance_Request;


-- 14. Delete all foreign tables created to access the remote database, after performing the
-- integration, decisions, and information integration.
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
