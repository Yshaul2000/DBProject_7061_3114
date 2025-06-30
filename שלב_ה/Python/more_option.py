def more_option_screen(previous_win=None):
    import customtkinter as ctk
    from queries_screen import open_queries_screen  # Function to open the Queries screen
    from functions_screen import open_functions_screen  # Function to open the Functions screen
    from procedures_screen import open_procedures_screen  # Function to open the Procedures screen
    from fetch_all import open_fetch_table  # Function to open the Fetch Tables screen
    from main import open_main_menu  # Function to open the Main Menu screen
    from main_programs_screen import open_main_programs_screen  # Function to open the Main Programs screen

    # Set the appearance mode and default color theme for the application
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Close the previous window (e.g., Main Menu) if it exists
    if previous_win is not None:
        previous_win.destroy()

    # Create a new window for the "More Options" screen
    win = ctk.CTkToplevel()
    win.title("More Options")  # Set the window title
    win.geometry("400x600")  # Set the window size

    # Add a title label to the screen
    title_label = ctk.CTkLabel(win, text="Choose an option:", font=("Arial", 20))
    title_label.pack(pady=20)  # Add padding around the label

    # Add buttons for navigating to different screens
    ctk.CTkButton(win, text="Run Queries", width=250, command=open_queries_screen).pack(pady=10)
    ctk.CTkButton(win, text="Run Functions", width=250, command=open_functions_screen).pack(pady=10)
    ctk.CTkButton(win, text="Run Procedures", width=250, command=open_procedures_screen).pack(pady=10)
    ctk.CTkButton(win, text="Run Fetch on Tables", width=250, command=open_fetch_table).pack(pady=10)

    # Add a new button to run main programs
    ctk.CTkButton(win, text="Run Main Programs", width=250, command=lambda: [win.destroy(), open_main_programs_screen()]).pack(pady=10)

    # Add a back button to return to the Main Menu
    ctk.CTkButton(win, text="⬅ Back to Main Menu", width=250, command=lambda: [win.destroy(), open_main_menu()]).pack(pady=20)