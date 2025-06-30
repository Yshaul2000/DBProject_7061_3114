import customtkinter as ctk
from tkinter import messagebox
from db import get_connection

def open_takes_scholarship_screen():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    win = ctk.CTkToplevel()
    win.title("Takes_Scholarship CRUD")
    win.geometry("500x450")

    # כותרת
    title_label = ctk.CTkLabel(win, text="Takes_Scholarship CRUD", font=("Arial", 24))
    title_label.pack(pady=20)

    # שדות
    schol_label = ctk.CTkLabel(win, text="Scholarship ID*")
    schol_label.pack()
    schol_entry = ctk.CTkEntry(win, placeholder_text="Scholarship ID")
    schol_entry.pack(pady=5)

    student_label = ctk.CTkLabel(win, text="Student ID*")
    student_label.pack()
    student_entry = ctk.CTkEntry(win, placeholder_text="Student ID")
    student_entry.pack(pady=5)

    date_label = ctk.CTkLabel(win, text="Approval Date (YYYY-MM-DD)")
    date_label.pack()
    date_entry = ctk.CTkEntry(win, placeholder_text="YYYY-MM-DD")
    date_entry.pack(pady=5)

    def insert():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO takes_scholarship (scholarship_id, StudentID, approval_date)
            VALUES (%s, %s, %s)
        """, (schol_entry.get(), student_entry.get(), date_entry.get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("OK", "Inserted Takes_Scholarship")

    def update():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE takes_scholarship 
            SET approval_date=%s
            WHERE scholarship_id=%s AND StudentID=%s
        """, (date_entry.get(), schol_entry.get(), student_entry.get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("OK", "Updated Takes_Scholarship")

    def delete():
        conn = get_connection()
        cur = conn.cursor()

        scholarship_id = schol_entry.get()
        student_id = student_entry.get()

        cur.execute("""
            DELETE FROM takes_scholarship
            WHERE scholarship_id = %s AND studentid = %s
        """, (scholarship_id, student_id))

        if cur.rowcount == 0:
            messagebox.showwarning("Not Found", "No matching record found in takes_scholarship.")
        else:
            conn.commit()
            messagebox.showinfo("OK", "Deleted from takes_scholarship successfully.")

        conn.close()

    def fetch():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM takes_scholarship
            WHERE scholarship_id=%s AND StudentID=%s
        """, (schol_entry.get(), student_entry.get()))
        row = cur.fetchone()
        if row:
            date_entry.delete(0, ctk.END)
            date_entry.insert(0, row[2])
        else:
            messagebox.showerror("Not Found", "No such record")
        conn.close()

    # כפתורים ב-Frame מסודר
    btn_frame = ctk.CTkFrame(win)
    btn_frame.pack(pady=20)

    insert_btn = ctk.CTkButton(btn_frame, text="Insert", command=insert, width=120)
    insert_btn.grid(row=0, column=0, padx=10, pady=5)

    update_btn = ctk.CTkButton(btn_frame, text="Update", command=update, width=120)
    update_btn.grid(row=0, column=1, padx=10, pady=5)

    delete_btn = ctk.CTkButton(btn_frame, text="Delete", command=delete, width=120)
    delete_btn.grid(row=1, column=0, padx=10, pady=5)

    fetch_btn = ctk.CTkButton(btn_frame, text="Fetch", command=fetch, width=120)
    fetch_btn.grid(row=1, column=1, padx=10, pady=5)
