-----------------------------------------------------------------------------------------------------
-- This anonymous block demonstrates various operations related to student financial aid and payments,
-- including checking aid status, listing payments, and triggering aid updates via scholarship insertion.
-----------------------------------------------------------------------------------------------------
DO $$
DECLARE
    aid_info_before TEXT;
    aid_info_after TEXT;
    ref_cursor REFCURSOR;
    payment_rec RECORD;
    new_scholarship_id INT;
BEGIN
    -- 1) Function: How much financial aid before
    aid_info_before := count_and_sum_student_aid(355);
    RAISE NOTICE 'Aid Info BEFORE: %', aid_info_before;

    -- 2) Procedure: Display all student payments
    CALL get_student_payments(355, ref_cursor);

    LOOP
        FETCH ref_cursor INTO payment_rec;
        EXIT WHEN NOT FOUND;
        RAISE NOTICE 'Payment ID: %, Amount: %, Date: %',
            payment_rec.payment_id,
            payment_rec.amount,
            payment_rec.payment_date;
    END LOOP;
    CLOSE ref_cursor;

    -- 3) Select scholarship_id that student id doesn't already have
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
    ELSE
        RAISE NOTICE 'No new scholarship available for student id.';
    END IF;

    -- 4) Function: How much financial aid after — to verify the trigger worked!
    aid_info_after := count_and_sum_student_aid(355);
    RAISE NOTICE 'Aid Info AFTER: %', aid_info_after;

END;
$$;
