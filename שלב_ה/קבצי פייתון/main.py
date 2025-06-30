import customtkinter as ctk
from student_crud import open_student_screen
from payment_crud import open_payment_screen
from takes_scholarship_crud import open_takes_scholarship_screen
from reports_screen import open_reports_screen
from more_option import more_option_screen

def open_main_menu():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Main Menu")
    root.geometry("350x450")

    title_label = ctk.CTkLabel(root, text="Main Menu", font=("Arial", 24))
    title_label.pack(pady=20)

    ctk.CTkButton(root, text="Student CRUD", width=200, command=open_student_screen).pack(pady=8)
    ctk.CTkButton(root, text="Payment CRUD", width=200, command=open_payment_screen).pack(pady=8)
    ctk.CTkButton(root, text="Takes Scholarship CRUD", width=200, command=open_takes_scholarship_screen).pack(pady=8)
    ctk.CTkButton(root, text="Reports & Actions", width=200, command=open_reports_screen).pack(pady=8)
    ctk.CTkButton(root, text="More Options", width=200, command=lambda: more_option_screen(root)).pack(pady=8)

    root.mainloop()

if __name__ == "__main__":
    from login_screen import open_login
    open_login()
