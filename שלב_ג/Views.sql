-- VIEW and QUERIES for Financial department

-- VIEW: Average Total Payment Per Student
-- This view combines student and payment data to calculate the average total payment for each student,
-- regardless of the payment type, rounded to three decimal places.
-- This helps in understanding the average revenue per student with cleaner formatting.
CREATE VIEW Average_Total_Payment_Per_Student AS
SELECT
    s.StudentID,
    s.FirstName || ' ' || s.LastName AS StudentName,
    ROUND(AVG(p.amount), 3) AS AverageTotalPayment
FROM
    Student s
JOIN
    Payment p ON s.StudentID = p.StudentID
GROUP BY
    s.StudentID, s.FirstName, s.LastName
ORDER BY
    StudentName;

-- STORY BEHIND THE VIEW: The finance department wants to know the average total payment made by each student,
-- irrespective of the payment type, displayed with improved readability by rounding to three decimal places.
-- This can assist in estimating the average revenue per student with cleaner formatting.

SELECT * FROM Average_Total_Payment_Per_Student;


-- QUERY 1 on the VIEW: Display the top 3 students with the highest average total payment (rounded).
SELECT
    StudentName,
    AverageTotalPayment
FROM
    Average_Total_Payment_Per_Student
ORDER BY
    AverageTotalPayment DESC
LIMIT 3;

-- QUERY 2 on the VIEW: Calculate the overall average total payment across all students.
SELECT
    ROUND(AVG(AverageTotalPayment), 3) AS OverallAveragePaymentPerStudent
FROM
    Average_Total_Payment_Per_Student;

--------------------------------------------------------------------------------------------

-- VIEW and QUERIES for the Dormitory department

-- VIEW: Analysis of Building Capacity vs. Potential Number of Residents
-- This view combines information about buildings and apartments to display the maximum room capacity per building,
-- and compares it to the total number of registered students (assuming all are potential residents).
CREATE VIEW Building_Capacity_Vs_Registered_Students AS
SELECT
    b.BuildingID,
    b.BuildingName,
    b.MaxApartments,
    SUM(a.RoomCapacity) AS TotalRoomCapacity,
    (SELECT COUNT(*) FROM student_remote) AS TotalRegisteredStudents -- Total registered students
FROM
    Building b
JOIN
    Apartment a ON b.BuildingID = a.BuildingID
GROUP BY
    b.BuildingID, b.BuildingName, b.MaxApartments
ORDER BY
    b.BuildingName;

-- STORY BEHIND THE VIEW: The dorm management is interested in comparing the potential housing capacity
-- (based on the number of rooms) with the total number of students in the university, to assess the need
-- for expanding housing options.

SELECT * FROM Building_Capacity_Vs_Registered_Students;

-- QUERY 1: Display the average potential occupancy percentage per building (assuming every registered student wants a room) .
SELECT
    BuildingName,
    ROUND(CAST((SELECT COUNT(*) FROM student_remote) AS DECIMAL) / SUM(TotalRoomCapacity) * 100, 3) AS AveragePotentialOccupancy
FROM
    Building_Capacity_Vs_Registered_Students
GROUP BY
    BuildingName
ORDER BY
    AveragePotentialOccupancy DESC;

-- QUERY 2: Display the difference between the number of registered students and the room capacity in each building.
SELECT
    BuildingName,
    (SELECT COUNT(*) FROM student_remote) - SUM(TotalRoomCapacity) AS StudentCapacityDifference
FROM
    Building_Capacity_Vs_Registered_Students
GROUP BY
    BuildingName
ORDER BY
    StudentCapacityDifference DESC;