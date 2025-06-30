import customtkinter as ctk
from tkinter import messagebox
from db import get_connection

def open_functions_screen():
    # Set the appearance mode to dark
    ctk.set_appearance_mode("dark")
    # Set the default color theme to blue
    ctk.set_default_color_theme("blue")

    # Create a new top-level window
    win = ctk.CTkToplevel()
    win.title("Run Functions")
    win.geometry("800x700")

    # Title label for the screen
    title_label = ctk.CTkLabel(win, text="Functions Screen", font=("Arial", 24))
    title_label.pack(pady=20)

    # Label for department ID input
    dept_label = ctk.CTkLabel(win, text="Department ID:")
    dept_label.pack()
    # Entry field for department ID
    dept_entry = ctk.CTkEntry(win, placeholder_text="Enter Department ID")
    dept_entry.pack(pady=5)

    def run_dept_salary():
        """
        Runs the 'get_long_term_department_salary' function from the database
        and displays the result in the output box.
        """
        try:
            conn = get_connection()
            cur = conn.cursor()
            # Execute the SQL function with the department ID
            cur.execute("SELECT get_long_term_department_salary(%s)", (dept_entry.get(),))
            result = cur.fetchone()[0]
            # Clear previous content and insert the new result
            output_box.delete("1.0", "end")
            output_box.insert("end", f"Total salary for long-term employees in department {dept_entry.get()}: {result}")
            conn.close()
        except Exception as e:
            # Show an error message if something goes wrong
            messagebox.showerror("Error", str(e))

    # Button to run the department salary function
    run_dept_btn = ctk.CTkButton(win, text="Run get_long_term_department_salary", command=run_dept_salary)
    run_dept_btn.pack(pady=10) # Moved this button up

    # Textbox to display output
    output_box = ctk.CTkTextbox(win, width=700, height=350)
    output_box.pack(pady=20)


    # Label for student ID input
    student_label = ctk.CTkLabel(win, text="Student ID:")
    student_label.pack(pady=(20, 0))
    # Entry field for student ID
    student_entry = ctk.CTkEntry(win, placeholder_text="Enter Student ID")
    student_entry.pack(pady=5)

    def run_student_aid():
        """
        Runs the 'count_and_sum_student_aid' function from the database
        and displays the result in the output box.
        """
        try:
            conn = get_connection()
            cur = conn.cursor()
            # Execute the SQL function with the student ID
            cur.execute("SELECT count_and_sum_student_aid(%s)", (student_entry.get(),))
            result = cur.fetchone()[0]
            # Clear previous content and insert the new result
            output_box.delete("1.0", "end")
            output_box.insert("end", f"Result for Student ID {student_entry.get()}:\n{result}")
            conn.close()
        except Exception as e:
            # Show an error message if something goes wrong
            messagebox.showerror("Error", str(e))

    # Button to run the student aid function
    run_aid_btn = ctk.CTkButton(win, text="Run count_and_sum_student_aid", command=run_student_aid)
    run_aid_btn.pack(pady=10)