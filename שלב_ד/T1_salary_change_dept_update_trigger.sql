-- Purpose: This code creates a PostgreSQL trigger system that automatically updates 
-- department descriptions whenever an employee's salary is changed.
-- The trigger responds to salary modifications and marks the affected department 
-- as having been updated due to the salary change.

-- Function definition: Creates the trigger function that will be executed
-- when the trigger conditions are met
CREATE OR REPLACE FUNCTION trg_update_department_description()
RETURNS TRIGGER AS $$
BEGIN
    -- Update the Department table's description field
    -- Set a standard message indicating the department was affected by a salary change
    UPDATE Department
    SET description = 'Updated due to salary change'
    WHERE department_id = NEW.department_id; -- Use the department_id from the modified employee record
    
    -- Return NEW to allow the original UPDATE operation to proceed normally
    RETURN NEW;
END;
$$ LANGUAGE plpgsql; -- Written in PL/pgSQL procedural language

-- Trigger creation: Sets up the actual trigger that will call the function above
CREATE TRIGGER update_department_description_trigger
AFTER UPDATE OF salary ON Employees -- Fires after salary column is updated in Employees table
FOR EACH ROW -- Execute once for each row that gets updated
WHEN (OLD.salary <> NEW.salary) -- Only trigger when salary value actually changes (not just any update)
EXECUTE FUNCTION trg_update_department_description(); -- Call the function defined above