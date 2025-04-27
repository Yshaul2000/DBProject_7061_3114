-- Start of rollback transaction
BEGIN;

-- Perform the update (add 'israel-' before '@' in emails)
UPDATE Student
SET Email = SUBSTRING(Email, 1, POSITION('@' IN Email) - 1) || 'israel-' || SUBSTRING(Email, POSITION('@' IN Email), LENGTH(Email))
WHERE Email NOT LIKE '%israel-%';

-- Check current state after update (before rollback)
SELECT StudentID, Email FROM Student WHERE Email LIKE '%israel-%';

-- Rollback the transaction to undo the update
ROLLBACK;

-- Check state again to confirm emails returned to original form
SELECT StudentID, Email FROM Student WHERE Email NOT LIKE '%israel-%';


-- Start of commit transaction
BEGIN;

-- Update: Add 77 NIS to the Amount of scholarships with exactly 77 AnnualHours
UPDATE Scholarship
SET Amount = Amount + 77
WHERE AnnualHours = 77;

-- Preview: See the scholarships that were updated BEFORE committing
SELECT scholarship_id, Name, Amount, AnnualHours
FROM Scholarship
WHERE AnnualHours = 77;

-- Finalize the update
COMMIT;

-- Confirm the changes AFTER committing
SELECT scholarship_id, Name, Amount, AnnualHours
FROM Scholarship
WHERE AnnualHours = 77;




