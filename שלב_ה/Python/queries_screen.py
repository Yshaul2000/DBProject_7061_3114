import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
from db import get_connection


def open_queries_screen():
    """
    Opens a new Tkinter Toplevel window for advanced database queries.
    This window allows users to select and run predefined SQL queries
    and view their results.
    """
    win = tk.Toplevel()
    win.title("הרצת שאילתות מתקדמות")  # Set window title (Hebrew: "Run Advanced Queries")
    win.geometry("1400x800")  # Set initial window size
    win.configure(bg='#2b2b2b')  # Set dark background color for the window

    # Create the main frame to hold all other widgets
    main_frame = tk.Frame(win, bg='#2b2b2b')
    main_frame.pack(fill='both', expand=True, padx=10, pady=10)

    # Left side - Query list frame
    left_frame = tk.Frame(main_frame, bg='#3c3c3c', width=450)
    left_frame.pack(side='left', fill='y', padx=(0, 10))
    left_frame.pack_propagate(False)  # Prevent frame from shrinking to fit contents

    # Run All Queries button
    run_all_btn = tk.Button(
        left_frame,
        text="▶ Run All Queries",  # Button text
        bg='#4a9eff',  # Background color (blue)
        fg='white',  # Foreground color (text)
        font=('Arial', 12, 'bold'),  # Font style
        height=2,  # Button height
        relief='flat',  # Flat button appearance
        cursor='hand2'  # Cursor changes to hand on hover
    )
    run_all_btn.pack(fill='x', padx=15, pady=15)

    # Frame for scrollable query list
    canvas = tk.Canvas(left_frame, bg='#3c3c3c', highlightthickness=0)
    scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg='#3c3c3c')

    # Bind the scrollable frame's size to update the canvas scroll region
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # Create a window in the canvas to put the scrollable frame
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Pack the canvas and scrollbar
    canvas.pack(side="left", fill="both", expand=True, padx=(15, 0))
    scrollbar.pack(side="right", fill="y", padx=(0, 15))

    # Right side - Results area frame
    right_frame = tk.Frame(main_frame, bg='#2b2b2b')
    right_frame.pack(side='right', fill='both', expand=True)

    # ScrolledText widget for displaying query results
    output = scrolledtext.ScrolledText(
        right_frame,
        width=80,  # Initial width
        height=40,  # Initial height
        bg='#1e1e1e',  # Dark background for text area
        fg='#ffffff',  # White foreground for text
        font=('Consolas', 10),  # Monospaced font for code/results
        insertbackground='white',  # Color of the text insertion cursor
        selectbackground='#404040',  # Background color for selected text
        relief='flat',  # Flat border
        bd=5  # Border width
    )
    output.pack(fill='both', expand=True, padx=10, pady=10)

    # List of predefined queries, each with a name, description, and SQL string
    queries = [
        {
            "name": "SELECT 1",
            "description": "Total payments by each student grouped by year",
            "sql": """SELECT s.StudentID, s.FirstName || ' ' || s.LastName AS FullName,
                       EXTRACT(YEAR FROM p.payment_date) AS PayYear,
                       SUM(p.amount) AS TotalPaid
                       FROM Student s JOIN Payment p ON s.StudentID = p.StudentID
                       GROUP BY s.StudentID, FullName, EXTRACT(YEAR FROM p.payment_date)
                       ORDER BY TotalPaid DESC;"""
        },
        {
            "name": "SELECT 2",
            "description": "Monthly income summary by payment type",
            "sql": """SELECT EXTRACT(YEAR FROM payment_date) AS PayYear,
                       EXTRACT(MONTH FROM payment_date) AS PayMonth,
                       type_payment, SUM(amount) AS TotalMonthlyIncome
                       FROM Payment
                       GROUP BY EXTRACT(YEAR FROM payment_date), EXTRACT(MONTH FROM payment_date), type_payment
                       ORDER BY PayYear DESC, PayMonth DESC;"""
        },
        {
            "name": "SELECT 3",
            "description": "Payments from the past month with type and topic",
            "sql": """SELECT s.StudentID, s.FirstName || ' ' || s.LastName AS FullName,
                       TO_CHAR(p.payment_date, 'YYYY-MM-DD') AS PaymentDate,
                       p.amount, p.type_payment, p.topic
                       FROM Student s JOIN Payment p ON s.StudentID = p.StudentID
                       WHERE p.payment_date >= CURRENT_DATE - INTERVAL '1 month';"""
        },
        {
            "name": "SELECT 4",
            "description": "Departments with total budgets over 50,000",
            "sql": """SELECT d.name AS DepartmentName, SUM(b.total_amount) AS TotalBudget
                       FROM Department d JOIN uses_budget ub ON d.department_id = ub.department_id
                       JOIN Budget b ON ub.budget_id = b.budget_id
                       GROUP BY d.name HAVING SUM(b.total_amount) > 50000;"""
        },
        {
            "name": "SELECT 5",
            "description": "Employees by hire year and department",
            "sql": """SELECT e.name AS EmployeeName,
                       EXTRACT(YEAR FROM e.hire_date) AS HireYear,
                       d.name AS DepartmentName,
                       e.salary
                       FROM Employees e JOIN Department d ON e.department_id = d.department_id
                       ORDER BY HireYear DESC;"""
        },
        {
            "name": "SELECT 6",
            "description": "Average payment amount by payment type",
            "sql": """SELECT type_payment,
                       AVG(amount) AS AvgAmount,
                       COUNT(*) AS NumPayments
                       FROM Payment
                       GROUP BY type_payment
                       ORDER BY AvgAmount DESC;"""
        },
        {
            "name": "SELECT 7",
            "description": "Students with financial aid but no scholarship",
            "sql": """SELECT s.StudentID, s.FirstName, s.LastName,
                       COUNT(ra.aid_id) AS AidCount
                       FROM Student s
                       LEFT JOIN takes_scholarship ts ON s.StudentID = ts.StudentID
                       JOIN receives_aid ra ON s.StudentID = ra.StudentID
                       WHERE ts.scholarship_id IS NULL
                       GROUP BY s.StudentID, s.FirstName, s.LastName;"""
        },
        {
            "name": "SELECT 8",
            "description": "Highest scholarship in each year",
            "sql": """SELECT sch.Name AS ScholarshipName,
                       EXTRACT(YEAR FROM ts.approval_date) AS ApprovalYear,
                       sch.Amount
                       FROM takes_scholarship ts
                       JOIN Scholarship sch ON ts.scholarship_id = sch.scholarship_id
                       WHERE sch.Amount = (
                         SELECT MAX(s2.Amount)
                         FROM Scholarship s2
                         JOIN takes_scholarship ts2 ON ts2.scholarship_id = s2.scholarship_id
                         WHERE EXTRACT(YEAR FROM ts2.approval_date) = EXTRACT(YEAR FROM ts.approval_date)
                       );"""
        },
        {
            "name": "SELECT 9",
            "description": "Students born from 2006 onwards",
            "sql": """SELECT StudentID, FirstName, LastName, dateofbirth
                      FROM Student
                      WHERE dateofbirth >= DATE '2006-01-01'
                      ORDER BY dateofbirth ASC;"""
        },
        {
            "name": "DELETE 1",
            "description": "Delete old payments older than 2 years with low amounts",
            "sql": """DELETE FROM Payment
                       WHERE payment_date < CURRENT_DATE - INTERVAL '2 years'
                         AND amount < (
                           SELECT AVG(p2.amount)
                           FROM Payment p2
                           WHERE p2.type_payment = Payment.type_payment
                         );"""
        },
        {
            "name": "DELETE 2",
            "description": "Delete employees with very high salaries (70,000 - 90,000)",
            "sql": """DELETE FROM Employees
                       WHERE salary BETWEEN 70000 AND 90000;"""
        },
        {
            "name": "DELETE 3",
            "description": "Delete scholarships with annual hours below 90",
            "sql": """DELETE FROM Scholarship
                       WHERE AnnualHours < 90;"""
        },
        {
            "name": "UPDATE 1",
            "description": "Reduce salaries by 80% for departments with budgets under 100,000",
            "sql": """UPDATE Employees
                       SET salary = salary * 0.2
                       WHERE department_id IN (
                         SELECT ub.department_id
                         FROM uses_budget ub
                         JOIN Budget b ON ub.budget_id = b.budget_id
                         GROUP BY ub.department_id
                         HAVING SUM(b.total_amount) < 100000
                       );"""
        },
        {
            "name": "UPDATE 2",
            "description": "Increase scholarship by 10% if student average payment is higher",
            "sql": """UPDATE Scholarship
                       SET Amount = CASE
                         WHEN (SELECT AVG(p.amount)
                               FROM Payment p
                               JOIN takes_scholarship ts ON p.StudentID = ts.StudentID
                               WHERE ts.scholarship_id = Scholarship.scholarship_id) > Scholarship.Amount
                         THEN Scholarship.Amount * 1.1
                         ELSE Scholarship.Amount
                       END;"""
        },
        {
            "name": "UPDATE 3",
            "description": "Add 'israel.' prefix in student emails if missing",
            "sql": """UPDATE Student
                       SET Email = SUBSTRING(Email, 1, POSITION('@' IN Email) - 1) || 'israel.' || SUBSTRING(Email, POSITION('@' IN Email), LENGTH(Email))
                       WHERE Email NOT LIKE '%israel%';"""
        }
    ]

    def run_query(query_sql, display_in_main=False):
        try:
            # Determine if the query is a SELECT statement
            is_select = query_sql.strip().upper().startswith("SELECT")
            # Get database connection. Use "mydatabase" for SELECT, "SaveStage2" for others.
            conn = get_connection("mydatabase" if is_select else "SaveStage2")
            cur = conn.cursor()  # Create a cursor object
            cur.execute(query_sql)  # Execute the SQL query

            if is_select:
                # Fetch all rows from the executed SELECT query
                rows = cur.fetchall()
                # Get column names from the cursor description
                columns = [desc[0] for desc in cur.description]

                # Format the output for SELECT queries
                col_width = 33
                header = "".join(col.ljust(col_width) for col in columns) + "\n"
                separator = "-" * (col_width * len(columns)) + "\n"
                result = header + separator

                # Add each row to the result string
                for row in rows:
                    result += "".join(str(cell).ljust(col_width) for cell in row) + "\n"

                if display_in_main:
                    # Display result in the main output area
                    output.delete(1.0, tk.END)  # Clear previous content
                    output.insert(tk.END, result)  # Insert new result
                else:
                    # Create a new Toplevel window for the query result
                    result_window = tk.Toplevel()
                    result_window.title("Query Result")
                    result_window.configure(bg='#2b2b2b')
                    result_box = scrolledtext.ScrolledText(
                        result_window,
                        width=130,
                        height=40,
                        bg='#1e1e1e',
                        fg='#ffffff',
                        font=('Consolas', 10)
                    )
                    result_box.pack(padx=10, pady=10)
                    result_box.insert(tk.END, result)
                    result_box.config(state='disabled')  # Make the text box read-only
            else:
                # For DML queries, get the number of affected rows
                affected = cur.rowcount
                conn.commit()  # Commit changes to the database

                result_text = f"Query executed successfully.\nRows affected: {affected}"

                if display_in_main:
                    # Display DML result in the main output area
                    output.delete(1.0, tk.END)
                    output.insert(tk.END, result_text)
                else:
                    # Create a new Toplevel window for DML query execution status
                    result_window = tk.Toplevel()
                    result_window.title("Query Executed")
                    result_window.configure(bg='#2b2b2b')
                    result_box = tk.Text(
                        result_window,
                        width=60,
                        height=10,
                        bg='#1e1e1e',
                        fg='#ffffff',
                        font=('Consolas', 10)
                    )
                    result_box.pack(padx=10, pady=10)
                    result_box.insert(tk.END, result_text)
                    result_box.config(state='disabled')  # Make the text box read-only

            conn.close()  # Close the database connection
        except Exception as e:
            # Display any database errors in a messagebox
            messagebox.showerror("Error", str(e))

    def run_all_queries():
        """
        Executes all predefined queries sequentially and displays their
        status and results in the main output area.
        """
        output.delete(1.0, tk.END)  # Clear the output area
        output.insert(tk.END, "Running all queries...\n\n")
        output.update()  # Update the display immediately

        for i, q in enumerate(queries, 1):
            output.insert(tk.END, f"=== {q['name']}: {q['description']} ===\n")
            output.update()
            try:
                run_query(q["sql"], display_in_main=True)  # Run query and display in main output
                output.insert(tk.END, f"\n✓ {q['name']} completed successfully\n\n")
            except Exception as e:
                output.insert(tk.END, f"\n✗ {q['name']} failed: {str(e)}\n\n")
            output.see(tk.END)  # Scroll to the end of the output
            output.update()

    # Configure the 'Run All Queries' button to call run_all_queries function
    run_all_btn.configure(command=run_all_queries)

    # Function to handle mouse wheel scrolling for the canvas
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # Bind mouse wheel event when mouse enters the canvas
    def bind_mousewheel(event):
        canvas.bind_all("<MouseWheel>", on_mousewheel)

    # Unbind mouse wheel event when mouse leaves the canvas
    def unbind_mousewheel(event):
        canvas.unbind_all("<MouseWheel>")

    # Bind enter and leave events to the canvas for mouse wheel control
    canvas.bind('<Enter>', bind_mousewheel)
    canvas.bind('<Leave>', unbind_mousewheel)

    # Function to create a click handler for each query frame
    def create_query_click_handler(query_sql, query_name, query_frame):
        def handler(event):
            # Change background color to indicate selection
            for widget in scrollable_frame.winfo_children():
                if isinstance(widget, tk.Frame):
                    widget.configure(bg='#4a4a4a')  # Default background for unselected
            query_frame.configure(bg='#5a5a5a')  # Highlight selected query

            # Run the selected query
            output.delete(1.0, tk.END)  # Clear output area
            output.insert(tk.END, f"Running {query_name}...\n\n")
            output.update()
            run_query(query_sql, display_in_main=True)  # Run and display in main output

        return handler

    # List to keep references to query frames (not strictly necessary for this code, but good practice)
    query_frames = []

    # Clear existing widgets in the scrollable frame before recreating (in case of re-initialization)
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    # Create and populate the query list in the left frame
    for i, q in enumerate(queries):
        # Frame for each individual query item
        query_frame = tk.Frame(scrollable_frame, bg='#4a4a4a', relief='flat', bd=1)
        query_frame.pack(fill='x', padx=10, pady=5)
        query_frames.append(query_frame)

        # Query title label
        title_label = tk.Label(
            query_frame,
            text=q["name"],
            bg='#4a4a4a',
            fg='#ffffff',
            font=('Arial', 11, 'bold'),
            anchor='w'  # Align text to the left
        )
        title_label.pack(fill='x', padx=10, pady=(8, 2))

        # Query description label
        desc_label = tk.Label(
            query_frame,
            text=q["description"],
            bg='#4a4a4a',
            fg='#cccccc',
            font=('Arial', 9),
            wraplength=380,  # Wrap text if it exceeds this width
            justify='left',  # Justify text to the left
            anchor='w'
        )
        desc_label.pack(fill='x', padx=10, pady=(0, 8))

        # Add click event handler to the query frame
        handler = create_query_click_handler(q["sql"], q["name"], query_frame)
        query_frame.bind("<Button-1>", handler)  # Bind left-click
        query_frame.configure(cursor='hand2')  # Change cursor on hover

        # Bind the same click handler to all child widgets within the query frame
        # This ensures clicking on text labels also triggers the query
        for child in query_frame.winfo_children():
            child.bind("<Button-1>", handler)
            child.configure(cursor='hand2')

    # Add initial welcome messages to the output area
    output.insert(tk.END, "Advanced Queries System Ready\n")
    output.insert(tk.END, "Click on any query to run it individually or use 'Run All Queries'\n")
    output.insert(tk.END, "=" * 60 + "\n\n")

