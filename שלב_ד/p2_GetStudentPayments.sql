CREATE OR REPLACE PROCEDURE get_student_payments(
    p_student_id INT,
    OUT ref_payments REFCURSOR  -- Output parameter: a reference cursor to return the payment records
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Open a cursor for selecting payment details for the given student ID
    OPEN ref_payments FOR
    SELECT payment_id, amount, payment_date
    FROM Payment
    WHERE StudentID = p_student_id;

EXCEPTION
    WHEN OTHERS THEN
        -- Handle any unexpected error by raising a warning
        RAISE WARNING 'Error opening payments cursor';
END;
$$;
