CREATE OR REPLACE PROCEDURE display_student_payments(
    p_student_id INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    payment_rec RECORD;
    total_payments DECIMAL(10,2) := 0;
    payment_count INT := 0;
BEGIN
    -- Input validation
    IF p_student_id IS NULL OR p_student_id <= 0 THEN
        RAISE EXCEPTION 'Invalid student ID: %', p_student_id;
    END IF;
    
    RAISE NOTICE '=== Student Payments Report for Student ID: % ===', p_student_id;
    RAISE NOTICE 'Payment ID | Amount | Payment Date';
    RAISE NOTICE '----------------------------------------';
    
    -- Loop through all payments for the given student ID
    FOR payment_rec IN 
        SELECT payment_id, amount, payment_date
        FROM Payment
        WHERE studentid = p_student_id
        ORDER BY payment_date DESC
    LOOP
        RAISE NOTICE '% | % | %', 
            payment_rec.payment_id,
            payment_rec.amount,
            payment_rec.payment_date;
        
        total_payments := total_payments + payment_rec.amount;
        payment_count := payment_count + 1;
    END LOOP;
    
    -- Summary
    IF payment_count = 0 THEN
        RAISE NOTICE 'No payments found for student ID: %', p_student_id;
    ELSE
        RAISE NOTICE '----------------------------------------';
        RAISE NOTICE 'Total Payments: % | Total Amount: %', payment_count, total_payments;
    END IF;
    
EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Error displaying payments for student ID %: %', p_student_id, SQLERRM;
        RAISE;
END;
$$;
