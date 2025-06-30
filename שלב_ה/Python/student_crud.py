import customtkinter as ctk
from tkinter import messagebox
from db import get_connection

def open_student_screen():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    win = ctk.CTkToplevel()
    win.title("Student CRUD")
    win.geometry("500x500")

    # כותרת
    title_label = ctk.CTkLabel(win, text="Student CRUD", font=("Arial", 24))
    title_label.pack(pady=20)

    # שדות
    id_label = ctk.CTkLabel(win, text="ID*")
    id_label.pack()
    id_entry = ctk.CTkEntry(win, placeholder_text="Student ID")
    id_entry.pack(pady=5)

    fn_label = ctk.CTkLabel(win, text="First Name")
    fn_label.pack()
    fn_entry = ctk.CTkEntry(win, placeholder_text="First Name")
    fn_entry.pack(pady=5)

    ln_label = ctk.CTkLabel(win, text="Last Name")
    ln_label.pack()
    ln_entry = ctk.CTkEntry(win, placeholder_text="Last Name")
    ln_entry.pack(pady=5)

    email_label = ctk.CTkLabel(win, text="Email")
    email_label.pack()
    email_entry = ctk.CTkEntry(win, placeholder_text="Email")
    email_entry.pack(pady=5)

    # פעולות CRUD
    def insert():
        conn = get_connection()
        cur = conn.cursor()

        student_id = id_entry.get().strip()
        if not student_id:
            messagebox.showerror("Error", "Student ID is required.")
            return

        # בדיקה אם הסטודנט כבר קיים
        cur.execute("SELECT * FROM Student WHERE StudentID=%s", (student_id,))
        existing_student = cur.fetchone()

        if existing_student:
            messagebox.showerror("Error", "Student already exists in the database.")
        else:
            cur.execute("INSERT INTO Student VALUES (%s, %s, %s, %s)",
                        (student_id, fn_entry.get().strip(), ln_entry.get().strip(), email_entry.get().strip()))
            conn.commit()
            messagebox.showinfo("OK", "Inserted")

        conn.close()

    def update():
        conn = get_connection()
        cur = conn.cursor()

        student_id = id_entry.get().strip()
        if not student_id:
            messagebox.showerror("Error", "Student ID is required.")
            return

        # בדיקה אם הסטודנט קיים
        cur.execute("SELECT * FROM Student WHERE StudentID=%s", (student_id,))
        existing_student = cur.fetchone()

        if not existing_student:
            messagebox.showerror("Error", "Student does not exist in the database.")
        else:
            cur.execute("UPDATE Student SET FirstName=%s, LastName=%s, Email=%s WHERE StudentID=%s",
                        (fn_entry.get().strip(), ln_entry.get().strip(), email_entry.get().strip(), student_id))
            conn.commit()
            messagebox.showinfo("OK", "Updated")

        conn.close()

    def delete():
        conn = get_connection()
        cur = conn.cursor()

        student_id = id_entry.get().strip()
        if not student_id:
            messagebox.showerror("Error", "Student ID is required.")
            return

        # בדיקה אם הסטודנט קיים
        cur.execute("SELECT * FROM Student WHERE StudentID=%s", (student_id,))
        existing_student = cur.fetchone()

        if not existing_student:
            messagebox.showerror("Error", "Student does not exist in the database.")
        else:
            # מחיקת רשומות תלויות קודם
            cur.execute("DELETE FROM payment WHERE studentid = %s", (student_id,))
            cur.execute("DELETE FROM takes_scholarship WHERE studentid = %s", (student_id,))
            cur.execute("DELETE FROM scholarship_log WHERE studentid = %s", (student_id,))
            cur.execute("DELETE FROM receives_aid WHERE studentid = %s", (student_id,))

            # ואז מחיקת הסטודנט עצמו
            cur.execute("DELETE FROM student WHERE studentid = %s", (student_id,))
            conn.commit()
            messagebox.showinfo("OK", "Deleted Student and all related records.")

        conn.close()

    def fetch():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Student WHERE StudentID=%s", (id_entry.get(),))
        row = cur.fetchone()
        if row:
            fn_entry.delete(0, ctk.END)
            ln_entry.delete(0, ctk.END)
            email_entry.delete(0, ctk.END)
            fn_entry.insert(0, row[1])
            ln_entry.insert(0, row[2])
            email_entry.insert(0, row[3])
        else:
            messagebox.showerror("Not found", "No such student")
        conn.close()

    # כפתורים מסודרים יפה
    btn_frame = ctk.CTkFrame(win)
    btn_frame.pack(pady=20)

    insert_btn = ctk.CTkButton(btn_frame, text="Insert", command=insert, width=100)
    insert_btn.grid(row=0, column=0, padx=10, pady=5)

    update_btn = ctk.CTkButton(btn_frame, text="Update", command=update, width=100)
    update_btn.grid(row=0, column=1, padx=10, pady=5)

    delete_btn = ctk.CTkButton(btn_frame, text="Delete", command=delete, width=100)
    delete_btn.grid(row=1, column=0, padx=10, pady=5)

    fetch_btn = ctk.CTkButton(btn_frame, text="Fetch", command=fetch, width=100)
    fetch_btn.grid(row=1, column=1, padx=10, pady=5)
