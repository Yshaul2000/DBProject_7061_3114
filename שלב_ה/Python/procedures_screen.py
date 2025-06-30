import customtkinter as ctk
from tkinter import messagebox
from db import get_connection

def open_procedures_screen():
    # General design settings
    ctk.set_appearance_mode("dark")  # Can also be "light" or "system"
    ctk.set_default_color_theme("blue")  # Can also be green, dark-blue, etc.

    # New window
    win = ctk.CTkToplevel()
    win.title("Run Procedures")
    win.geometry("650x650")  # Sets a slightly smaller size

    # Main title
    title_label = ctk.CTkLabel(win, text="Procedures Screen", font=("Arial", 24))
    title_label.pack(pady=20)

    # === Procedure 1: update_seniority_salary ===
    # Label for department ID
    dept_label = ctk.CTkLabel(win, text="Department ID:")
    dept_label.pack(pady=(10, 0))

    # Entry field for department ID
    dept_entry = ctk.CTkEntry(win, placeholder_text="Enter Department ID")
    dept_entry.pack(pady=5)

    def run_update_salary():
        """
        Executes the 'update_seniority_salary' stored procedure in the database
        for the given Department ID and displays a success message or error.
        """
        try:
            conn = get_connection()
            cur = conn.cursor()
            # Call the stored procedure
            cur.execute("CALL update_seniority_salary(%s)", (dept_entry.get(),))
            conn.commit()  # Commit the changes to the database
            # Clear output box and insert success message
            output_box.delete("1.0", "end")
            output_box.insert("end", f"Procedure update_seniority_salary executed for Department ID {dept_entry.get()}")
            conn.close()
        except Exception as e:
            # Show an error message if something goes wrong
            messagebox.showerror("Error", str(e))

    # Button to run the update_seniority_salary procedure
    run_salary_btn = ctk.CTkButton(win, text="Run update_seniority_salary", command=run_update_salary)
    run_salary_btn.pack(pady=10) # Moved this button up

    # Output textbox with a smaller size
    output_box = ctk.CTkTextbox(win, width=600, height=250)
    output_box.pack(pady=20)


    # === Procedure 2: display_student_payments (NOTICE) ===
    # Label for student ID
    student_label = ctk.CTkLabel(win, text="Student ID:")
    student_label.pack(pady=(20, 0))

    # Entry field for student ID
    student_entry = ctk.CTkEntry(win, placeholder_text="Enter Student ID")
    student_entry.pack(pady=5)

    def run_display_student_payments():
        """
        Executes the 'display_student_payments' stored procedure for the given Student ID.
        It captures and displays any NOTICE messages returned by the procedure.
        """
        try:
            conn = get_connection()
            cur = conn.cursor()

            # Clear previous notices
            conn.notices.clear()

            # Call the stored procedure
            cur.execute("CALL display_student_payments(%s)", (int(student_entry.get()),))

            # Get any notices (messages) from the connection
            notices = conn.notices
            output_box.delete("1.0", "end")

            if notices:
                for msg in notices:
                    output_box.insert("end", msg.strip() + '\n')
            else:
                output_box.insert("end", f"No notices received for Student ID {student_entry.get()}")

            conn.close()

        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")

    # Button to run the display_student_payments procedure
    run_display_btn = ctk.CTkButton(win, text="Run display_student_payments", command=run_display_student_payments)
    run_display_btn.pack(pady=10)

# Self-contained test for direct execution
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.title("Main Window")
    root.geometry("400x200")

    open_btn = ctk.CTkButton(root, text="Open Procedures Screen", command=open_procedures_screen)
    open_btn.pack(pady=50)

    root.mainloop()