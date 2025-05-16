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



