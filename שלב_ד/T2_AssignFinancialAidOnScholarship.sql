-- Purpose: Auto-inserts financial aid EVERY TIME a student receives a new scholarship
-- (regardless of existing aid records)
CREATE OR REPLACE FUNCTION trg_scholarship_to_aid()
RETURNS TRIGGER AS $$
DECLARE
    -- Variable to store the selected aid ID
    v_aid_id INT;
BEGIN
    -- Get an aid_id from Financial_Aid table (always add new aid)
    SELECT aid_id
    INTO v_aid_id
    FROM Financial_Aid
    LIMIT 1; -- Take the first available aid
    
    -- Always insert a new record into receives_aid table
    INSERT INTO receives_aid (StudentID, aid_id, application_date)
    VALUES (NEW.StudentID, v_aid_id, NEW.approval_date);
    
    -- Return NEW to allow the original operation to proceed normally
    RETURN NEW;
    
-- Exception handling: Catch any errors that might occur during execution
EXCEPTION
    WHEN OTHERS THEN
        -- Log error message without stopping the main operation
        RAISE NOTICE 'Trigger error: %', SQLERRM; -- SQLERRM contains the error message
        -- Return NEW to allow the original operation to continue despite the error
        RETURN NEW;
END;
$$ LANGUAGE plpgsql; -- Written in PL/pgSQL procedural language

-- Drop existing trigger if it exists
DROP TRIGGER IF EXISTS auto_aid_on_scholarship ON takes_scholarship;

-- Create the trigger on takes_scholarship table
CREATE TRIGGER auto_aid_on_scholarship
AFTER INSERT ON takes_scholarship
FOR EACH ROW
EXECUTE FUNCTION trg_scholarship_to_aid();