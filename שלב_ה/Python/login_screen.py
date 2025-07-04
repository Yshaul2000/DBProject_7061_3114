import tkinter as tk
from tkinter import messagebox
from main import open_main_menu

# Define correct username and password
CORRECT_USERNAME = "yshaul"
CORRECT_PASSWORD = "s2023"


def open_login():
    win = tk.Tk()
    win.title("🎓 University Management System - Login")

    # Set window size and position in the center
    win.geometry("800x600")
    win.configure(bg='#0d1b2a')  # Deep dark background
    win.resizable(False, False)

    # Center the window on the screen
    win.update_idletasks()
    x = (win.winfo_screenwidth() // 2) - (800 // 2)
    y = (win.winfo_screenheight() // 2) - (600 // 2)
    win.geometry(f"800x600+{x}+{y}")

    # Create left frame with a turquoise background
    left_frame = tk.Frame(win, bg='#20b2aa', width=400, height=600)
    left_frame.place(x=0, y=0)
    left_frame.pack_propagate(False)

    # Create right frame with the login form
    right_frame = tk.Frame(win, bg='#ffffff', width=400, height=600)
    right_frame.place(x=400, y=0)
    right_frame.pack_propagate(False)

    # === Left side - Design and welcome message ===
    # Main title
    welcome_label = tk.Label(left_frame,
                            text="Welcome !",
                            font=("Segoe UI", 32, "bold"),
                            fg="#ffffff",
                            bg="#20b2aa")
    welcome_label.place(x=50, y=150)

    # Subtitle
    subtitle_label = tk.Label(left_frame,
                             text="University Management System\nSecure Access Portal",
                             font=("Segoe UI", 16),
                             fg="#ffffff",
                             bg="#20b2aa",
                             justify="left")
    subtitle_label.place(x=50, y=220)

    # Decorative elements
    # Large circle
    canvas1 = tk.Canvas(left_frame, width=120, height=120, bg="#20b2aa", highlightthickness=0)
    canvas1.place(x=280, y=80)
    canvas1.create_oval(10, 10, 110, 110, fill="#17a085", outline="#ffffff", width=3)
    canvas1.create_text(60, 60, text="🎓", font=("Arial", 40), fill="#ffffff")

    # === Right side - Login form ===
    # Form title
    form_title = tk.Label(right_frame,
                         text="Sign In",
                         font=("Segoe UI", 28, "bold"),
                         fg="#0d1b2a",
                         bg="#ffffff")
    form_title.place(x=80, y=120)

    # Form subtitle
    form_subtitle = tk.Label(right_frame,
                            text="Enter your credentials to access the system",
                            font=("Segoe UI", 12),
                            fg="#666666",
                            bg="#ffffff")
    form_subtitle.place(x=80, y=170)

    # Container for input fields
    input_container = tk.Frame(right_frame, bg="#ffffff")
    input_container.place(x=80, y=220, width=240, height=200)

    # Username field
    username_label = tk.Label(input_container,
                             text="Username",
                             font=("Segoe UI", 11, "bold"),
                             fg="#333333",
                             bg="#ffffff")
    username_label.pack(anchor="w", pady=(0, 5))

    user_entry = tk.Entry(input_container,
                         font=("Segoe UI", 12),
                         width=25,
                         relief="solid",
                         bd=1,
                         bg="#f8f9fa",
                         fg="#333333",
                         insertbackground="#20b2aa")
    user_entry.pack(ipady=8, pady=(0, 20))

    # Password field
    password_label = tk.Label(input_container,
                             text="Password",
                             font=("Segoe UI", 11, "bold"),
                             fg="#333333",
                             bg="#ffffff")
    password_label.pack(anchor="w", pady=(0, 5))

    pass_entry = tk.Entry(input_container,
                         show="*",
                         font=("Segoe UI", 12),
                         width=25,
                         relief="solid",
                         bd=1,
                         bg="#f8f9fa",
                         fg="#333333",
                         insertbackground="#20b2aa")
    pass_entry.pack(ipady=8, pady=(0, 30))

    def do_login():
        username = user_entry.get().strip()
        password = pass_entry.get().strip()

        # Check if fields are not empty
        if not username or not password:
            messagebox.showerror("Login Failed", "Please enter both username and password!")
            return

        # Check if credentials are correct
        if username == CORRECT_USERNAME and password == CORRECT_PASSWORD:
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            win.destroy()
            open_main_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password!")
            # Clear the password field in case of error
            pass_entry.delete(0, tk.END)

    # Styled login button
    login_btn = tk.Button(input_container,
                         text="Sign In →",
                         command=do_login,
                         font=("Segoe UI", 12, "bold"),
                         bg="#20b2aa",
                         fg="white",
                         relief="flat",
                         bd=0,
                         width=20,
                         height=2,
                         cursor="hand2")
    login_btn.pack(pady=(0, 10))

    # Hover effect for the button
    def on_enter(e):
        login_btn.config(bg="#17a085")

    def on_leave(e):
        login_btn.config(bg="#20b2aa")

    login_btn.bind("<Enter>", on_enter)
    login_btn.bind("<Leave>", on_leave)

    # Focus effect for input fields
    def on_focus_in_user(e):
        user_entry.config(bg="#ffffff", bd=2, relief="solid")

    def on_focus_out_user(e):
        user_entry.config(bg="#f8f9fa", bd=1, relief="solid")

    def on_focus_in_pass(e):
        pass_entry.config(bg="#ffffff", bd=2, relief="solid")

    def on_focus_out_pass(e):
        pass_entry.config(bg="#f8f9fa", bd=1, relief="solid")

    user_entry.bind("<FocusIn>", on_focus_in_user)
    user_entry.bind("<FocusOut>", on_focus_out_user)
    pass_entry.bind("<FocusIn>", on_focus_in_pass)
    pass_entry.bind("<FocusOut>", on_focus_out_pass)

    # Allow login with Enter key
    def on_enter_key(event):
        do_login()

    win.bind('<Return>', on_enter_key)

    # General information on the left side
    info_label = tk.Label(left_frame,
                         text="Secure login required\nfor system access",
                         font=("Segoe UI", 10),
                         bg="#20b2aa",
                         fg="#ffffff",
                         justify="left")
    info_label.place(x=50, y=520)

    # Decorative separator line
    separator = tk.Frame(right_frame, bg="#e0e0e0", height=1, width=240)
    separator.place(x=80, y=460)

    # Help text
    help_label = tk.Label(right_frame,
                         text="Need help? Contact system administrator",
                         font=("Segoe UI", 9),
                         fg="#999999",
                         bg="#ffffff")
    help_label.place(x=80, y=480)

    # Focus on the username field
    user_entry.focus()

    win.mainloop()


if __name__ == "__main__":
    open_login()