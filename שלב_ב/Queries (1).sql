-- =============================================
-- SELECT 1: Total payments by student and year
-- =============================================
SELECT 
    s.StudentID,
    s.FirstName || ' ' || s.LastName AS FullName,
    EXTRACT(YEAR FROM p.payment_date) AS PayYear,
    SUM(p.amount) AS TotalPaid
FROM 
    Student s
JOIN 
    Payment p ON s.StudentID = p.StudentID
GROUP BY 
    s.StudentID, FullName, EXTRACT(YEAR FROM p.payment_date)
ORDER BY 
    TotalPaid DESC;


-- ======================================================
-- SELECT 2: Monthly income summary from payments
-- ======================================================
SELECT 
    EXTRACT(YEAR FROM payment_date) AS PayYear,
    EXTRACT(MONTH FROM payment_date) AS PayMonth,
    type_payment,
    SUM(amount) AS TotalMonthlyIncome
FROM 
    Payment
GROUP BY 
    EXTRACT(YEAR FROM payment_date), EXTRACT(MONTH FROM payment_date), type_payment
ORDER BY 
    PayYear DESC, PayMonth DESC;



-- =============================================
-- SELECT 3: Payments from the past month, including type and topic
-- =============================================
SELECT 
    s.StudentID,
    s.FirstName || ' ' || s.LastName AS FullName,
    TO_CHAR(p.payment_date, 'YYYY-MM-DD') AS PaymentDate,
    p.amount,
    p.type_payment,
    p.topic
FROM 
    Student s
JOIN 
    Payment p ON s.StudentID = p.StudentID
WHERE 
    p.payment_date >= CURRENT_DATE - INTERVAL '1 month';

-- =============================================
-- SELECT 4: Departments with total budgets over 50,000
-- =============================================
SELECT 
    d.name AS DepartmentName,
    SUM(b.total_amount) AS TotalBudget
FROM 
    Department d
JOIN 
    uses_budget ub ON d.department_id = ub.department_id
JOIN 
    Budget b ON ub.budget_id = b.budget_id
GROUP BY 
    d.name
HAVING 
    SUM(b.total_amount) > 50000;

-- =============================================
-- SELECT 5: Employees by hire year and department
-- =============================================
SELECT 
    e.name AS EmployeeName,
    EXTRACT(YEAR FROM e.hire_date) AS HireYear,
    d.name AS DepartmentName,
    e.salary
FROM 
    Employees e
JOIN 
    Department d ON e.department_id = d.department_id
ORDER BY 
    HireYear DESC;

-- =============================================
-- SELECT 6: Average payment amount by type
-- =============================================
SELECT 
    type_payment,
    AVG(amount) AS AvgAmount,
    COUNT(*) AS NumPayments
FROM 
    Payment
GROUP BY 
    type_payment
ORDER BY 
    AvgAmount DESC;

-- =============================================
-- SELECT 7: Students with financial aid but no scholarship
-- =============================================
SELECT 
    s.StudentID,
    s.FirstName,
    s.LastName,
    COUNT(ra.aid_id) AS AidCount
FROM 
    Student s
LEFT JOIN 
    takes_scholarship ts ON s.StudentID = ts.StudentID
JOIN 
    receives_aid ra ON s.StudentID = ra.StudentID
WHERE 
    ts.scholarship_id IS NULL
GROUP BY 
    s.StudentID, s.FirstName, s.LastName;

-- =============================================
-- SELECT 8: Highest scholarship in each year
-- =============================================
SELECT 
    sch.Name AS ScholarshipName,
    EXTRACT(YEAR FROM ts.approval_date) AS ApprovalYear,
    sch.Amount
FROM 
    takes_scholarship ts
JOIN 
    Scholarship sch ON ts.scholarship_id = sch.scholarship_id
WHERE 
    sch.Amount = (
        SELECT MAX(s2.Amount)
        FROM Scholarship s2
        JOIN takes_scholarship ts2 ON ts2.scholarship_id = s2.scholarship_id
        WHERE EXTRACT(YEAR FROM ts2.approval_date) = EXTRACT(YEAR FROM ts.approval_date)
    );

-- ====================================================================================
-- DELETE 1: Delete old payments (older than 2 years) with amounts below average by type
-- ====================================================================================
DELETE FROM Payment
WHERE payment_date < CURRENT_DATE - INTERVAL '2 years'
  AND amount < (
      SELECT AVG(p2.amount)
      FROM Payment p2
      WHERE p2.type_payment = Payment.type_payment
	  );

-- ====================================================================================
-- DELETE 2: Delete employees with very high salaries
-- ====================================================================================
DELETE FROM Employees
WHERE salary between 70000 and 90000;

-- ====================================================================================
-- DELETE 3: Delete scholarships with low annual hours and related records
-- ====================================================================================
-- Modify foreign key constraint in "takes_scholarship" table to ON DELETE CASCADE
ALTER TABLE takes_scholarship
DROP CONSTRAINT takes_scholarship_scholarship_id_fkey,
ADD CONSTRAINT takes_scholarship_scholarship_id_fkey
FOREIGN KEY (scholarship_id) REFERENCES Scholarship(scholarship_id) ON DELETE CASCADE;

-- Delete scholarships with annual hours requirement under 90
DELETE FROM Scholarship
WHERE AnnualHours < 90; 


-- ===================================================================
-- UPDATE 1: Reduce salaries by 80% for departments with budgets under 100,000
-- ===================================================================
UPDATE Employees
SET salary = salary * 0.2
WHERE department_id IN (
    SELECT ub.department_id
    FROM uses_budget ub
    JOIN Budget b ON ub.budget_id = b.budget_id
    GROUP BY ub.department_id
    HAVING SUM(b.total_amount) < 100000
);

-- ==============================================================================================================
-- UPDATE 2: Increase scholarship by 10% if student’s average payment exceeds current scholarship amount
-- ==============================================================================================================
UPDATE Scholarship
SET Amount = CASE
    WHEN (SELECT AVG(p.amount)
          FROM Payment p
          JOIN takes_scholarship ts ON p.StudentID = ts.StudentID
          WHERE ts.scholarship_id = Scholarship.scholarship_id) > Scholarship.Amount
    THEN Scholarship.Amount * 1.1
    ELSE Scholarship.Amount
END;


-- ==================================================================================================
-- UPDATE 3: Add "israel." prefix before the '@' in email addresses that don’t already include it
-- ==================================================================================================
UPDATE Student
SET Email = SUBSTRING(Email, 1, POSITION('@' IN Email) - 1) || 'israel.' || SUBSTRING(Email, POSITION('@' IN Email), LENGTH(Email))
WHERE Email NOT LIKE '%israel%';
