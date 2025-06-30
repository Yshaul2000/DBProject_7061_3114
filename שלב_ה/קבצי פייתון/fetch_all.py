import customtkinter as ctk
from tkinter import messagebox
from db import get_connection

def open_fetch_table():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    win = ctk.CTkToplevel()
    win.title("Select All - Show Tables")
    win.geometry("900x520")

    # אזור גלילה
    container = ctk.CTkFrame(win)
    container.pack(fill="both", expand=True, padx=10, pady=10)

    canvas = ctk.CTkCanvas(container, width=350, height=450)
    scrollbar = ctk.CTkScrollbar(container, orientation="vertical", command=canvas.yview)
    scrollable_frame = ctk.CTkFrame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # רשימת הטבלאות
    tables = [
        ("Department", "SELECT * FROM Department;"),
        ("Employees", "SELECT * FROM Employees;"),
        ("Budget", "SELECT * FROM Budget;"),
        ("uses_budget", "SELECT * FROM uses_budget;"),
        ("Student", "SELECT * FROM Student;"),
        ("Payment", "SELECT * FROM Payment;"),
        ("Scholarship", "SELECT * FROM Scholarship;"),
        ("takes_scholarship", "SELECT * FROM takes_scholarship;"),
        ("Financial_Aid", "SELECT * FROM Financial_Aid;"),
        ("receives_aid", "SELECT * FROM receives_aid;")
    ]

    def run_query_in_new_window(query_sql, table_name):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(query_sql)
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]

            result_window = ctk.CTkToplevel()
            result_window.title(f"Results - {table_name}")
            result_window.geometry("800x500")

            result_box = ctk.CTkTextbox(result_window, width=750, height=450)
            result_box.pack(padx=20, pady=20)

            col_width = 20
            header = "".join(col.ljust(col_width) for col in columns) + "\n"
            separator = "-" * (col_width * len(columns)) + "\n"
            result = header + separator

            for row in rows:
                result += "".join(str(cell).ljust(col_width) for cell in row) + "\n"

            result_box.insert("0.0", result)
            result_box.configure(state="disabled")

            conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run_all_tables():
        try:
            conn = get_connection()
            cur = conn.cursor()

            result_window = ctk.CTkToplevel()
            result_window.title("Results - All Tables")
            result_window.geometry("800x500")

            result_box = ctk.CTkTextbox(result_window, width=750, height=450)
            result_box.pack(padx=20, pady=20)

            for table_name, sql in tables:
                result_box.insert("end", f"===== {table_name} =====\n")
                cur.execute(sql)
                rows = cur.fetchall()
                columns = [desc[0] for desc in cur.description]

                col_width = 20
                header = "".join(col.ljust(col_width) for col in columns) + "\n"
                separator = "-" * (col_width * len(columns)) + "\n"
                result = header + separator

                for row in rows:
                    result += "".join(str(cell).ljust(col_width) for cell in row) + "\n"

                result_box.insert("end", result + "\n")

            result_box.configure(state="disabled")
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # כפתור להריץ הכל
    run_all_btn = ctk.CTkButton(scrollable_frame, text="▶ Run All Tables", command=run_all_tables)
    run_all_btn.grid(row=0, column=0, columnspan=2, pady=15, padx=20, sticky="ew")

    row_idx = 1
    for table_name, sql in tables:
        label = ctk.CTkLabel(scrollable_frame, text=table_name, font=("Arial", 12, "bold"))
        label.grid(row=row_idx, column=0, padx=20, pady=8, sticky="w")

        button = ctk.CTkButton(
            scrollable_frame,
            text="Run",
            command=lambda s=sql, t=table_name: run_query_in_new_window(s, t)
        )
        button.grid(row=row_idx, column=1, padx=10, pady=8)

        row_idx += 1
