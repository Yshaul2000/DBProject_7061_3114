# import customtkinter as ctk
# from queries_screen import open_queries_screen
# from functions_screen import open_functions_screen
# from procedures_screen import open_procedures_screen
# from fetch_all import open_fetch_table
# from main import open_main_menu

def more_option_screen(previous_win=None):
    import customtkinter as ctk
    from queries_screen import open_queries_screen
    from functions_screen import open_functions_screen
    from procedures_screen import open_procedures_screen
    from fetch_all import open_fetch_table
    from main import open_main_menu
    from main_programs_screen import open_main_programs_screen

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # סוגר את החלון הקודם (Main Menu)
    if previous_win is not None:
        previous_win.destroy()

    win = ctk.CTkToplevel()
    win.title("More Options")
    win.geometry("400x600")

    title_label = ctk.CTkLabel(win, text="Choose an option:", font=("Arial", 20))
    title_label.pack(pady=20)

    ctk.CTkButton(win, text="Run Queries", width=250, command=open_queries_screen).pack(pady=10)
    ctk.CTkButton(win, text="Run Functions", width=250, command=open_functions_screen).pack(pady=10)
    ctk.CTkButton(win, text="Run Procedures", width=250, command=open_procedures_screen).pack(pady=10)
    ctk.CTkButton(win, text="Run Fetch on Tables", width=250, command=open_fetch_table).pack(pady=10)

    # כפתור חדש: Run Main Programs
    ctk.CTkButton(win, text="Run Main Programs", width=250, command=lambda: [win.destroy(), open_main_programs_screen()]).pack(pady=10)

    # כפתור חזור שפותח מחדש את ה-Main Menu
    ctk.CTkButton(win, text="⬅ Back to Main Menu", width=250, command=lambda: [win.destroy(), open_main_menu()]).pack(pady=20)
