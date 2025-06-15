-- Purpose: This procedure updates the salaries of employees within a specific department based on their seniority.
-- Employees with more than 5 years of tenure receive a 20% salary increase,
-- and employees with more than 2 years (but not more than 5) receive a 10% salary increase.

CREATE OR REPLACE PROCEDURE update_seniority_salary(p_dept_id INT)
LANGUAGE plpgsql
AS $$
DECLARE
    r RECORD; -- Declare a record variable to iterate through employee data
BEGIN
    -- Loop through each employee in the specified department
    FOR r IN SELECT employee_id, hire_date FROM Employees WHERE department_id = p_dept_id
    LOOP
        -- Check if the employee's tenure is greater than 5 years
        IF AGE(NOW(), r.hire_date) > INTERVAL '5 years' THEN
            -- Update salary: increase by 20% for employees with more than 5 years seniority
            UPDATE Employees
            SET salary = salary * 1.20
            WHERE employee_id = r.employee_id;
        -- Check if the employee's tenure is greater than 2 years (but not more than 5 years)
        ELSIF AGE(NOW(), r.hire_date) > INTERVAL '2 years' THEN
            -- Update salary: increase by 10% for employees with more than 2 years seniority
            UPDATE Employees
            SET salary = salary * 1.10
            WHERE employee_id = r.employee_id;
        END IF;
    END LOOP;

    -- Raise a notice message indicating successful completion for the department
    RAISE NOTICE 'Salary updates done for department %', p_dept_id;

EXCEPTION
    -- Catch any exceptions that occur during the procedure execution
    WHEN OTHERS THEN
        -- Raise a warning if an error occurs, providing a general error message
        RAISE WARNING 'Error in procedure update_seniority_salary';
END;
$$;