-------------------------------------------------------------------------------------------------------------
-- Main Program: Seniority Salary Update Demonstration
-- This program tests the seniority salary update functionality by comparing
-- long-term employee salaries before and after applying the update procedure.
---------------------------------------------------------------------------------------------------------------
DO $$
DECLARE
    total_before NUMERIC;
    total_after NUMERIC;
BEGIN
    -- Before update
    total_before := get_long_term_department_salary(338);
    RAISE NOTICE 'Total long-term salaries BEFORE update: %', total_before;

    -- Call the procedure that updates the salary
    CALL update_seniority_salary(338);

    -- After update
    total_after := get_long_term_department_salary(338);
    RAISE NOTICE 'Total long-term salaries AFTER update: %', total_after;
END;
$$;
