import tkinter as tk
from tkinter import messagebox
import threading

# IMPORT ONLY CLI FUNCTIONS
from code import (
    get_db_connection,
    customer_menu,
    habit_menu,
    goal_menu,
    log_menu,
    reports_menu,
    advanced_queries_menu,
    test_single_function_trigger
)

def run_thread(func, conn):
    threading.Thread(target=func, args=(conn,), daemon=True).start()

def main():
    conn = get_db_connection()
    if not conn:
        messagebox.showerror("Error", "Database connection failed")
        return

    root = tk.Tk()
    root.title("Personal Habit Tracker")
    root.geometry("500x600")
    root.configure(bg="#1e1e2e")

    tk.Label(
        root,
        text="Personal Habit Tracker",
        font=("Helvetica", 20, "bold"),
        fg="white",
        bg="#1e1e2e"
    ).pack(pady=20)

    tk.Label(
        root,
        text="DBMS Project – Tkinter Interface",
        fg="gray",
        bg="#1e1e2e"
    ).pack(pady=5)

    btn = {
        "width": 35,
        "height": 2,
        "bg": "#313244",
        "fg": "white",
        "font": ("Helvetica", 10),
        "activebackground": "#45475a"
    }

    tk.Button(root, text="Customer Management",
              command=lambda: run_thread(customer_menu, conn),
              **btn).pack(pady=5)

    tk.Button(root, text="Habit Management",
              command=lambda: run_thread(habit_menu, conn),
              **btn).pack(pady=5)

    tk.Button(root, text="Goal Management",
              command=lambda: run_thread(goal_menu, conn),
              **btn).pack(pady=5)

    tk.Button(root, text="Log Management",
              command=lambda: run_thread(log_menu, conn),
              **btn).pack(pady=5)

    tk.Button(root, text="Reports & Analytics",
              command=lambda: run_thread(reports_menu, conn),
              **btn).pack(pady=5)

    tk.Button(root, text="Advanced Queries",
              command=lambda: run_thread(advanced_queries_menu, conn),
              **btn).pack(pady=5)

    tk.Button(root, text="Test Function / Trigger / Procedure",
              command=lambda: run_thread(test_single_function_trigger, conn),
              **btn).pack(pady=5)

    tk.Button(
        root,
        text="Exit",
        command=root.destroy,
        bg="#f38ba8",
        fg="black",
        width=35,
        height=2,
        font=("Helvetica", 10, "bold")
    ).pack(pady=25)

    root.mainloop()
    conn.close()

if __name__ == "__main__":
    main()
