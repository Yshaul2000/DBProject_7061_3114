import customtkinter as ctk
from tkinter import messagebox
from db import get_connection

def open_main_programs_screen():
    # Create a new window for running main programs
    win = ctk.CTkToplevel()
    win.title("Run Main Programs")
    win.geometry("1000x700")

    # Large output box for displaying results
    output = ctk.CTkTextbox(win, width=800, height=400)
    output.pack(pady=20)

    # === Main Program 1: Student Financial Aid Demo ===
    student_frame = ctk.CTkFrame(win)
    student_frame.pack(pady=10)

    # Input field for Student ID
    ctk.CTkLabel(student_frame, text="Student ID:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=5)
    student_entry = ctk.CTkEntry(student_frame, width=200)
    student_entry.grid(row=0, column=1, padx=10, pady=5)

    def run_financial_aid_demo():
        try:
            conn = get_connection()  # Establish database connection
            cur = conn.cursor()

            # SQL program to manage student financial aid
            main_program = f"""
            DO $$
            DECLARE
                aid_info_before TEXT;
                aid_info_after TEXT;
                new_scholarship_id INT;
            BEGIN
                aid_info_before := count_and_sum_student_aid({student_entry.get()});
                RAISE NOTICE 'Aid Info BEFORE: %', aid_info_before;

                CALL display_student_payments({student_entry.get()});

                SELECT scholarship_id INTO new_scholarship_id
                FROM Scholarship
                WHERE scholarship_id NOT IN (
                    SELECT scholarship_id
                    FROM takes_scholarship
                    WHERE StudentID = {student_entry.get()}
                )
                LIMIT 1;

                IF new_scholarship_id IS NOT NULL THEN
                    INSERT INTO takes_scholarship (scholarship_id, StudentID, approval_date)
                    VALUES (new_scholarship_id, {student_entry.get()}, CURRENT_DATE);
                    RAISE NOTICE 'Added scholarship_id % for student %', new_scholarship_id, {student_entry.get()};
                ELSE
                    RAISE NOTICE 'No new scholarship available for student %', {student_entry.get()};
                END IF;

                aid_info_after := count_and_sum_student_aid({student_entry.get()});
                RAISE NOTICE 'Aid Info AFTER: %', aid_info_after;
            END;
            $$;
            """
            cur.execute(main_program)  # Execute the SQL program
            conn.commit()  # Commit changes to the database

            notices = conn.notices  # Retrieve notices from the database
            output.delete("1.0", "end")  # Clear the output box
            output.insert("1.0", f"Student Financial Aid Demo completed for Student ID {student_entry.get()}:\n\n")

            # Display notices in the output box
            if notices:
                for notice in notices:
                    output.insert("end", notice + "\n")
            else:
                output.insert("end", "Program executed successfully - check database for changes\n")

            conn.close()  # Close the database connection

        except Exception as e:
            messagebox.showerror("Error", str(e))  # Show error message if an exception occurs

    # Button to run the financial aid demo
    ctk.CTkButton(student_frame, text="Run Student Financial Aid Demo", command=run_financial_aid_demo).grid(row=1, column=0, columnspan=2, pady=10)

    # === Main Program 2: Seniority Salary Update ===
    dept_frame = ctk.CTkFrame(win)
    dept_frame.pack(pady=10)

    # Input field for Department ID
    ctk.CTkLabel(dept_frame, text="Department ID:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=5)
    dept_entry = ctk.CTkEntry(dept_frame, width=200)
    dept_entry.grid(row=0, column=1, padx=10, pady=5)

    def run_seniority_salary_demo():
        try:
            conn = get_connection()  # Establish database connection
            cur = conn.cursor()

            # SQL program to update seniority salaries
            main_program = f"""
            DO $$
            DECLARE
                total_before NUMERIC;
                total_after NUMERIC;
            BEGIN
                total_before := get_long_term_department_salary({dept_entry.get()});
                RAISE NOTICE 'Total long-term salaries BEFORE update: %', total_before;

                CALL update_seniority_salary({dept_entry.get()});

                total_after := get_long_term_department_salary({dept_entry.get()});
                RAISE NOTICE 'Total long-term salaries AFTER update: %', total_after;
            END;
            $$;
            """
            cur.execute(main_program)  # Execute the SQL program
            conn.commit()  # Commit changes to the database

            notices = conn.notices  # Retrieve notices from the database
            output.delete("1.0", "end")  # Clear the output box
            output.insert("1.0", f"Seniority Salary Update Demo completed for Department ID {dept_entry.get()}:\n\n")

            # Display notices in the output box
            if notices:
                for notice in notices:
                    output.insert("end", notice + "\n")
            else:
                output.insert("end", "Program executed successfully - check database for changes\n")

            conn.close()  # Close the database connection

        except Exception as e:
            messagebox.showerror("Error", str(e))  # Show error message if an exception occurs

    # Button to run the seniority salary demo
    ctk.CTkButton(dept_frame, text="Run Seniority Salary Update Demo", command=run_seniority_salary_demo).grid(row=1, column=0, columnspan=2, pady=10)