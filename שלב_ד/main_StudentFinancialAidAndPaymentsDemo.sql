-----------------------------------------------------------------------------------------------------
-- This main demonstrates various operations related to student financial aid and payments,
-- including checking aid status, listing payments, and triggering aid updates via scholarship insertion.
-----------------------------------------------------------------------------------------------------
DO $$
DECLARE
    aid_info_before TEXT;
    aid_info_after TEXT;
    new_scholarship_id INT;
BEGIN
    -- 1) Function: How much financial aid before
    aid_info_before := count_and_sum_student_aid(355);
    RAISE NOTICE 'Aid Info BEFORE: %', aid_info_before;
    
    -- 2) Procedure: Display all student payments (much simpler now!)
    CALL display_student_payments(355);
    
    -- 3) Select scholarship_id that student doesn't already have
    SELECT scholarship_id INTO new_scholarship_id
    FROM Scholarship
    WHERE scholarship_id NOT IN (
        SELECT scholarship_id
        FROM takes_scholarship
        WHERE StudentID = 355
    )
    LIMIT 1;
    
    -- Insert only if a new scholarship was found
    IF new_scholarship_id IS NOT NULL THEN
        INSERT INTO takes_scholarship (scholarship_id, StudentID, approval_date)
        VALUES (new_scholarship_id, 355, CURRENT_DATE);
        RAISE NOTICE 'Added scholarship_id % for student 355', new_scholarship_id;
    ELSE
        RAISE NOTICE 'No new scholarship available for student 355';
    END IF;
    
    -- 4) Function: How much financial aid after — to verify the trigger worked!
    aid_info_after := count_and_sum_student_aid(355);
    RAISE NOTICE 'Aid Info AFTER: %', aid_info_after;
    
END;
$$;