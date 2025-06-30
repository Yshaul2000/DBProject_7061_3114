import customtkinter as ctk
from tkinter import messagebox
from db import get_connection

def open_functions_screen():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    win = ctk.CTkToplevel()
    win.title("Run Functions")
    win.geometry("700x600")

    # כותרת
    title_label = ctk.CTkLabel(win, text="Functions Screen", font=("Arial", 24))
    title_label.pack(pady=20)

    # === פונקציה 1: get_long_term_department_salary ===
    dept_label = ctk.CTkLabel(win, text="Department ID:")
    dept_label.pack()
    dept_entry = ctk.CTkEntry(win, placeholder_text="Enter Department ID")
    dept_entry.pack(pady=5)

    output_box = ctk.CTkTextbox(win, width=650, height=300)
    output_box.pack(pady=20)

    def run_dept_salary():
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT get_long_term_department_salary(%s)", (dept_entry.get(),))
            result = cur.fetchone()[0]
            output_box.delete("1.0", "end")
            output_box.insert("end", f"Total salary for long-term employees in department {dept_entry.get()}: {result}")
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    run_dept_btn = ctk.CTkButton(win, text="Run get_long_term_department_salary", command=run_dept_salary)
    run_dept_btn.pack(pady=10)

    # === פונקציה 2: count_and_sum_student_aid ===
    student_label = ctk.CTkLabel(win, text="Student ID:")
    student_label.pack(pady=(20, 0))
    student_entry = ctk.CTkEntry(win, placeholder_text="Enter Student ID")
    student_entry.pack(pady=5)

    def run_student_aid():
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT count_and_sum_student_aid(%s)", (student_entry.get(),))
            result = cur.fetchone()[0]
            output_box.delete("1.0", "end")
            output_box.insert("end", f"Result for Student ID {student_entry.get()}:\n{result}")
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    run_aid_btn = ctk.CTkButton(win, text="Run count_and_sum_student_aid", command=run_student_aid)
    run_aid_btn.pack(pady=10)
