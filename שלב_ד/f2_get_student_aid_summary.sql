CREATE OR REPLACE FUNCTION count_and_sum_student_aid(p_student_id INT)
RETURNS TEXT AS $$
DECLARE
    -- This function calculates the number of aids and the total aid amount for a given student
    total_amount NUMERIC := 0;  -- Variable to accumulate total aid amount
    aid_count INT := 0;         -- Variable to count the number of aids
    r RECORD;                   -- Record to hold each row of the query result
BEGIN
    FOR r IN 
        SELECT f.aid_amount 
        FROM Financial_Aid f
        JOIN receives_aid ra ON f.aid_id = ra.aid_id
        WHERE ra.StudentID = p_student_id  -- Filter aids by student ID
    LOOP
        total_amount := total_amount + r.aid_amount;  -- Accumulate total amount
        aid_count := aid_count + 1;                   -- Increment aid count
    END LOOP;

    RETURN 'Student ' || p_student_id || ' has ' ||  aid_count ||  ' aids totaling ' || total_amount;
    -- Return a summary string containing student ID, aid count, and total amount

EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Error occurred';  -- Handle any unexpected error gracefully
END;
$$ LANGUAGE plpgsql;
