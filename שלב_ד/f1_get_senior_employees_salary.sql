-- Purpose: This function calculates the total salary of long-term employees (2+ years) 
-- in a specific department. It uses a cursor to iterate through employees and 
-- accumulates salaries only for those who have been employed for more than 2 years.

-- Function definition: Returns total salary for long-term employees in a department
CREATE OR REPLACE FUNCTION get_long_term_department_salary(p_dept_id INT)
RETURNS NUMERIC AS $$
DECLARE
    -- Cursor to iterate through employees in the specified department
    emp_cursor REFCURSOR;
    -- Variable to store individual employee salary from cursor
    emp_salary NUMERIC;
    -- Variable to store individual employee hire date from cursor
    emp_hire_date DATE;
    -- Accumulator variable to store total salary sum (initialized to 0)
    total_salary NUMERIC := 0;
BEGIN
    -- Open cursor with query to get salary and hire_date for all employees in department
    OPEN emp_cursor FOR 
        SELECT salary, hire_date FROM Employees WHERE department_id = p_dept_id;
    
    -- Loop through all employees in the department
    LOOP
        -- Fetch next employee record into variables
        FETCH emp_cursor INTO emp_salary, emp_hire_date;
        -- Exit loop when no more records to process
        EXIT WHEN NOT FOUND;
        
        -- Check if employee has been working for more than 2 years
        -- AGE() calculates the time difference between current date and hire date
        IF AGE(NOW(), emp_hire_date) > INTERVAL '2 years' THEN
            -- Add this employee's salary to the total (only for long-term employees)
            total_salary := total_salary + emp_salary;
        END IF;
    END LOOP;
    
    -- Close the cursor to free resources
    CLOSE emp_cursor;
    
    -- Return the accumulated total salary of long-term employees
    RETURN total_salary;
    
-- Exception handling: Return 0 if any error occurs during execution
EXCEPTION
    WHEN OTHERS THEN
        -- Return 0 as default value in case of any database errors
        RETURN 0;
END;
$$ LANGUAGE plpgsql; -- Written in PL/pgSQL procedural language