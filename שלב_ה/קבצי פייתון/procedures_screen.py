import customtkinter as ctk
from tkinter import messagebox
from db import get_connection

def open_procedures_screen():
    # הגדרות עיצוב כלליות
    ctk.set_appearance_mode("dark")  # אפשר גם "light" או "system"
    ctk.set_default_color_theme("blue")  # אפשר גם green, dark-blue וכו'

    # חלון חדש
    win = ctk.CTkToplevel()
    win.title("Run Procedures")
    win.geometry("650x650")  # קובע גודל יותר קטן

    # כותרת ראשית
    title_label = ctk.CTkLabel(win, text="Procedures Screen", font=("Arial", 24))
    title_label.pack(pady=20)

    # === פרוצדורה 1: update_seniority_salary ===
    dept_label = ctk.CTkLabel(win, text="Department ID:")
    dept_label.pack(pady=(10, 0))

    dept_entry = ctk.CTkEntry(win, placeholder_text="Enter Department ID")
    dept_entry.pack(pady=5)

    # תיבת תוצאה בגודל קטן יותר
    output_box = ctk.CTkTextbox(win, width=600, height=250)
    output_box.pack(pady=20)

    def run_update_salary():
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("CALL update_seniority_salary(%s)", (dept_entry.get(),))
            conn.commit()
            output_box.delete("1.0", "end")
            output_box.insert("end", f"Procedure update_seniority_salary executed for Department ID {dept_entry.get()}")
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    run_salary_btn = ctk.CTkButton(win, text="Run update_seniority_salary", command=run_update_salary)
    run_salary_btn.pack(pady=10)

    # === פרוצדורה 2: display_student_payments (NOTICE) ===
    student_label = ctk.CTkLabel(win, text="Student ID:")
    student_label.pack(pady=(20, 0))

    student_entry = ctk.CTkEntry(win, placeholder_text="Enter Student ID")
    student_entry.pack(pady=5)

    def run_display_student_payments():
        try:
            conn = get_connection()
            cur = conn.cursor()

            # איפוס ההודעות הקודמות
            conn.notices.clear()

            # קריאה לפרוצדורה
            cur.execute("CALL display_student_payments(%s)", (int(student_entry.get()),))

            notices = conn.notices
            output_box.delete("1.0", "end")

            if notices:
                for msg in notices:
                    output_box.insert("end", msg.strip() + '\n')
            else:
                output_box.insert("end", f"No notices received for Student ID {student_entry.get()}")

            conn.close()

        except Exception as e:
            messagebox.showerror("Error", f"שגיאה: {str(e)}")

    run_display_btn = ctk.CTkButton(win, text="Run display_student_payments", command=run_display_student_payments)
    run_display_btn.pack(pady=10)

# בדיקה עצמאית להפעלה ישירה
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.title("Main Window")
    root.geometry("400x200")

    open_btn = ctk.CTkButton(root, text="Open Procedures Screen", command=open_procedures_screen)
    open_btn.pack(pady=50)

    root.mainloop()
