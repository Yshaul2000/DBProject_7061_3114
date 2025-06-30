import customtkinter as ctk
from tkinter import messagebox
from db import get_connection

def open_payment_screen():
    # Set appearance and theme
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Create the payment window
    win = ctk.CTkToplevel()
    win.title("Payment CRUD")
    win.geometry("600x700")  # Increased height to fit all widgets comfortably

    # Title label
    title_label = ctk.CTkLabel(win, text="Payment CRUD", font=("Arial", 24))
    title_label.pack(pady=20)

    # Input fields
    id_label = ctk.CTkLabel(win, text="Payment ID*")
    id_label.pack()
    id_entry = ctk.CTkEntry(win, placeholder_text="Payment ID")
    id_entry.pack(pady=5)

    student_label = ctk.CTkLabel(win, text="Student ID")
    student_label.pack()
    student_entry = ctk.CTkEntry(win, placeholder_text="Student ID")
    student_entry.pack(pady=5)

    amount_label = ctk.CTkLabel(win, text="Amount")
    amount_label.pack()
    amount_entry = ctk.CTkEntry(win, placeholder_text="Amount")
    amount_entry.pack(pady=5)

    date_label = ctk.CTkLabel(win, text="Payment Date (YYYY-MM-DD)")
    date_label.pack()
    date_entry = ctk.CTkEntry(win, placeholder_text="YYYY-MM-DD")
    date_entry.pack(pady=5)

    type_label = ctk.CTkLabel(win, text="Type Payment")
    type_label.pack()
    type_entry = ctk.CTkEntry(win, placeholder_text="Type Payment")
    type_entry.pack(pady=5)

    topic_label = ctk.CTkLabel(win, text="Topic")
    topic_label.pack()
    topic_entry = ctk.CTkEntry(win, placeholder_text="Topic")
    topic_entry.pack(pady=5)

    status_label = ctk.CTkLabel(win, text="Payment Status")
    status_label.pack()
    status_entry = ctk.CTkEntry(win, placeholder_text="Payment Status")
    status_entry.pack(pady=5)

    # Function to insert new payment
    def insert():
        conn = get_connection()
        cur = conn.cursor()

        payment_id = id_entry.get().strip()
        if not payment_id:
            messagebox.showerror("Error", "Payment ID is required.")
            return

        # Check if payment already exists
        cur.execute("SELECT * FROM Payment WHERE payment_id=%s", (payment_id,))
        existing_payment = cur.fetchone()

        if existing_payment:
            messagebox.showerror("Error", "Payment already exists in the database.")
        else:
            # Insert new payment
            cur.execute("""
                INSERT INTO Payment (payment_id, StudentID, amount, payment_date, type_payment, topic, payment_status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (payment_id, student_entry.get().strip(), amount_entry.get().strip(), date_entry.get().strip(),
                  type_entry.get().strip(), topic_entry.get().strip(), status_entry.get().strip()))
            conn.commit()
            messagebox.showinfo("OK", "Inserted Payment")

        conn.close()

    # Function to update existing payment
    def update():
        conn = get_connection()
        cur = conn.cursor()

        payment_id = id_entry.get().strip()
        if not payment_id:
            messagebox.showerror("Error", "Payment ID is required.")
            return

        # Check if payment exists
        cur.execute("SELECT * FROM Payment WHERE payment_id=%s", (payment_id,))
        existing_payment = cur.fetchone()

        if not existing_payment:
            messagebox.showerror("Error", "Payment does not exist in the database.")
        else:
            # Update payment data
            cur.execute("""
                UPDATE Payment 
                SET StudentID=%s, amount=%s, payment_date=%s, type_payment=%s, topic=%s, payment_status=%s 
                WHERE payment_id=%s
            """, (student_entry.get().strip(), amount_entry.get().strip(), date_entry.get().strip(),
                  type_entry.get().strip(), topic_entry.get().strip(), status_entry.get().strip(), payment_id))
            conn.commit()
            messagebox.showinfo("OK", "Updated Payment")

        conn.close()

    # Function to delete a payment
    def delete():
        conn = get_connection()
        cur = conn.cursor()

        payment_id = id_entry.get().strip()
        if not payment_id:
            messagebox.showerror("Error", "Payment ID is required.")
            return

        # Check if payment exists
        cur.execute("SELECT * FROM Payment WHERE payment_id=%s", (payment_id,))
        existing_payment = cur.fetchone()

        if not existing_payment:
            messagebox.showerror("Error", "Payment does not exist in the database.")
        else:
            # Delete payment
            cur.execute("DELETE FROM Payment WHERE payment_id=%s", (payment_id,))
            conn.commit()
            messagebox.showinfo("OK", "Deleted Payment")

        conn.close()

    # Function to fetch and display a payment's details
    def fetch():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Payment WHERE payment_id=%s", (id_entry.get(),))
        row = cur.fetchone()
        if row:
            # Clear all input fields
            student_entry.delete(0, ctk.END)
            amount_entry.delete(0, ctk.END)
            date_entry.delete(0, ctk.END)
            type_entry.delete(0, ctk.END)
            topic_entry.delete(0, ctk.END)
            status_entry.delete(0, ctk.END)

            # Insert fetched data into the fields
            student_entry.insert(0, row[1])
            amount_entry.insert(0, row[2])
            date_entry.insert(0, row[3])
            type_entry.insert(0, row[4])
            topic_entry.insert(0, row[5])
            status_entry.insert(0, row[6])
            conn.close()
        else:
            messagebox.showerror("Not Found", "No such Payment")

    # Buttons frame
    btn_frame = ctk.CTkFrame(win)
    btn_frame.pack(pady=20)

    # CRUD buttons
    insert_btn = ctk.CTkButton(btn_frame, text="Insert", command=insert, width=120)
    insert_btn.grid(row=0, column=0, padx=10, pady=5)

    update_btn = ctk.CTkButton(btn_frame, text="Update", command=update, width=120)
    update_btn.grid(row=0, column=1, padx=10, pady=5)

    delete_btn = ctk.CTkButton(btn_frame, text="Delete", command=delete, width=120)
    delete_btn.grid(row=1, column=0, padx=10, pady=5)

    fetch_btn = ctk.CTkButton(btn_frame, text="Fetch", command=fetch, width=120)
    fetch_btn.grid(row=1, column=1, padx=10, pady=5)
