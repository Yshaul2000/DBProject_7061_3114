import customtkinter as ctk
from tkinter import messagebox
from db import get_connection

def open_reports_screen():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    win = ctk.CTkToplevel()
    win.title("Reports & Actions")
    win.geometry("700x600")

    title_label = ctk.CTkLabel(win, text="Reports & Actions", font=("Arial", 24))
    title_label.pack(pady=20)

    # Student ID field
    sid_label = ctk.CTkLabel(win, text="Student ID:")
    sid_label.pack()
    sid_entry = ctk.CTkEntry(win, placeholder_text="Enter Student ID")
    sid_entry.pack(pady=5)

    # Result box
    output_box = ctk.CTkTextbox(win, width=550, height=300)
    output_box.pack(pady=20)

    def run_count_sum():
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT count_and_sum_student_aid(%s)", (sid_entry.get(),))
            result = cur.fetchone()[0]
            output_box.delete("1.0", "end")
            output_box.insert("end", f"Count & Sum Aid for Student ID {sid_entry.get()}:\n{result}")
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run_get_payments():
        try:
            conn = get_connection()
            cur = conn.cursor()
            conn.autocommit = False

            cur.callproc('get_student_payments', [int(sid_entry.get()), 'my_cursor'])
            cur.execute("FETCH ALL FROM my_cursor;")
            rows = cur.fetchall()

            result = "Payments:\n"
            result += "payment_id\tamount\tpayment_date\n"
            for row in rows:
                result += "\t".join(str(cell) for cell in row) + "\n"

            output_box.delete("1.0", "end")
            output_box.insert("end", result)

            conn.commit()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Buttons
    btn_frame = ctk.CTkFrame(win)
    btn_frame.pack(pady=10)

    count_sum_btn = ctk.CTkButton(btn_frame, text="Count & Sum Aid", command=run_count_sum, width=200)
    count_sum_btn.grid(row=0, column=0, padx=10, pady=5)

    get_payments_btn = ctk.CTkButton(btn_frame, text="Get Payments", command=run_get_payments, width=200)
    get_payments_btn.grid(row=0, column=1, padx=10, pady=5)