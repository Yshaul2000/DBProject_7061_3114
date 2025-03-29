CREATE TABLE Department (
    department_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(255)
);

CREATE TABLE Employees (
    employee_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    salary NUMERIC(10,2) NOT NULL,
    hire_date DATE NOT NULL,
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES Department(department_id)
);

CREATE TABLE Budget (
    budget_id INT PRIMARY KEY,
    total_amount NUMERIC(15,2) NOT NULL,
    budget_year INT NOT NULL
);

CREATE TABLE uses_budget (
    department_id INT,
    budget_id INT,
    PRIMARY KEY (department_id, budget_id),
    FOREIGN KEY (department_id) REFERENCES Department(department_id),
    FOREIGN KEY (budget_id) REFERENCES Budget(budget_id)
);

CREATE TABLE Student (
    StudentID INT PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Email VARCHAR(100) NOT NULL
);

CREATE TABLE Payment (
    payment_id INT PRIMARY KEY,
    StudentID INT,
    amount NUMERIC(10,2) NOT NULL,
    payment_date DATE NOT NULL,
    type_payment VARCHAR(50) NOT NULL,
    topic VARCHAR(100),
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID)
);

CREATE TABLE Scholarship (
    scholarship_id INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Amount NUMERIC(10,2) NOT NULL,
    AnnualHours INT NOT NULL
);

CREATE TABLE takes_scholarship (
    scholarship_id INT,
    StudentID INT,
    approval_date DATE NOT NULL,
    PRIMARY KEY (scholarship_id, StudentID),
    FOREIGN KEY (scholarship_id) REFERENCES Scholarship(scholarship_id),
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID)
);

CREATE TABLE Financial_Aid (
    aid_id INT PRIMARY KEY,
    aid_type VARCHAR(50) NOT NULL,
    aid_amount NUMERIC(10,2) NOT NULL,
    approval_date DATE NOT NULL,
    repayment_due DATE
);

CREATE TABLE receives_aid (
    StudentID INT,
    aid_id INT,
    application_date DATE NOT NULL,
    PRIMARY KEY (StudentID, aid_id),
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID),
    FOREIGN KEY (aid_id) REFERENCES Financial_Aid(aid_id)
);
