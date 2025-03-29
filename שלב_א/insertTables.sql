INSERT INTO Department (department_id, name, description) VALUES 
(1, 'HR', 'Human Resources'),
(2, 'IT', 'Information Technology'),
(3, 'Finance', 'Financial Department');

INSERT INTO Employees (employee_id, name, salary, hire_date, department_id) VALUES 
(101, 'Alice Green', 7500.00, '2023-05-10', 1),
(102, 'Bob White', 8500.00, '2022-07-15', 2),
(103, 'Charlie Black', 9200.00, '2021-09-20', 3);

INSERT INTO Budget (budget_id, total_amount, budget_year) VALUES 
(201, 500000.00, 2024),
(202, 600000.00, 2025),
(203, 700000.00, 2026);

INSERT INTO uses_budget (department_id, budget_id) VALUES 
(1, 201),
(2, 202),
(3, 203);

INSERT INTO Student (StudentID, FirstName, LastName, Email) VALUES 
(301, 'Daniel', 'Smith', 'daniel.smith@example.com'),
(302, 'Emma', 'Johnson', 'emma.johnson@example.com'),
(303, 'Michael', 'Brown', 'michael.brown@example.com');

INSERT INTO Payment (payment_id, StudentID, amount, payment_date, type_payment, topic) VALUES 
(401, 301, 2000.00, '2024-01-15', 'Credit Card', 'Tuition'),
(402, 302, 2500.00, '2024-02-10', 'Bank Transfer', 'Lab Fees'),
(403, 303, 1800.00, '2024-03-05', 'PayPal', 'Library Fees');

INSERT INTO Scholarship (scholarship_id, Name, Amount, AnnualHours) VALUES 
(501, 'Academic Excellence', 5000.00, 10),
(502, 'Athletic Scholarship', 4500.00, 8),
(503, 'Need-Based Aid', 4000.00, 12);

INSERT INTO takes_scholarship (scholarship_id, StudentID, approval_date) VALUES 
(501, 301, '2024-01-20'),
(502, 302, '2024-02-15'),
(503, 303, '2024-03-10');

INSERT INTO Financial_Aid (aid_id, aid_type, aid_amount, approval_date, repayment_due) VALUES 
(601, 'Grant', 3000.00, '2024-01-05', NULL),
(602, 'Loan', 5000.00, '2024-02-10', '2025-02-10'),
(603, 'Work-Study', 2000.00, '2024-03-15', NULL);

INSERT INTO receives_aid (StudentID, aid_id, application_date) VALUES 
(301, 601, '2024-01-01'),
(302, 602, '2024-02-05'),
(303, 603, '2024-03-10');
