import customtkinter as ctk
from student_crud import open_student_screen  # Function to open the Student CRUD screen
from payment_crud import open_payment_screen  # Function to open the Payment CRUD screen
from takes_scholarship_crud import open_takes_scholarship_screen  # Function to open the Takes Scholarship CRUD screen
from reports_screen import open_reports_screen  # Function to open the Reports & Actions screen
from more_option import more_option_screen  # Function to open the More Options screen

def open_main_menu():
    # Set the appearance mode and default color theme for the application
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Create the main application window
    root = ctk.CTk()
    root.title("Main Menu")  # Set the window title
    root.geometry("350x450")  # Set the window size

    # Add a title label to the main menu
    title_label = ctk.CTkLabel(root, text="Main Menu", font=("Arial", 24))
    title_label.pack(pady=20)  # Add padding around the label

    # Add buttons for navigating to different screens
    ctk.CTkButton(root, text="Student CRUD", width=200, command=open_student_screen).pack(pady=8)
    ctk.CTkButton(root, text="Payment CRUD", width=200, command=open_payment_screen).pack(pady=8)
    ctk.CTkButton(root, text="Takes Scholarship CRUD", width=200, command=open_takes_scholarship_screen).pack(pady=8)
    ctk.CTkButton(root, text="Reports & Actions", width=200, command=open_reports_screen).pack(pady=8)
    ctk.CTkButton(root, text="More Options", width=200, command=lambda: more_option_screen(root)).pack(pady=8)

    # Start the main event loop for the application
    root.mainloop()

if __name__ == "__main__":
    from login_screen import open_login  # Import the login screen function
    open_login()  # Open the login screen