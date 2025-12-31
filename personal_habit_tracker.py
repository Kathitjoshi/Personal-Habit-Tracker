"""
Personal Habit Tracker - Combined CLI and GUI Application (Fixed Version)
Team Members: Kathit Joshi (PES2UG23CS264), Kavyansh Jain (PES2UG23CS268)
NOTE: This Python file has been simplified to match the reduced SQL file 
      (1 Function: GetHabitCompletionRate, 1 Procedure: MarkGoalAchieved, 
      1 Trigger: before_log_insert).
"""

import pymysql
from pymysql import Error
from datetime import datetime, date
from tabulate import tabulate
import os
import sys
import re
import tkinter as tk
from tkinter import messagebox
import threading

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(text):
    """Print styled header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(70)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_info(text):
    """Print info message"""
    print(f"{Colors.YELLOW}ℹ {text}{Colors.END}")

def get_db_connection():
    """Establish database connection"""
    try:
        connection = pymysql.connect(
            host='localhost',
            database='project',
            user='root',  
            password='<my-password>',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.Cursor
        )
        return connection
    except Error as e:
        print_error(f"Error connecting to MySQL: {e}")
        print_error("Please ensure MySQL is running and credentials are correct.")
        return None

def display_main_menu():
    """Display main menu"""
    print_header("PERSONAL HABIT TRACKER")
    print(f"{Colors.BOLD}1.{Colors.END} Customer Management")
    print(f"{Colors.BOLD}2.{Colors.END} Habit Management")
    print(f"{Colors.BOLD}3.{Colors.END} Goal Management")
    print(f"{Colors.BOLD}4.{Colors.END} Log Management")
    print(f"{Colors.BOLD}5.{Colors.END} Reports & Analytics")
    print(f"{Colors.BOLD}6.{Colors.END} Advanced Queries")
    print(f"{Colors.BOLD}7.{Colors.END} Test Single Function & Trigger")
    print(f"{Colors.BOLD}0.{Colors.END} Exit")
    print(f"{Colors.CYAN}{'-'*70}{Colors.END}")

# --- Customer Management ---

def view_all_customers(connection):
    """View all customers"""
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT user_id, name, email, phone_no, created_at FROM Customer")
        results = cursor.fetchall()
        
        if results:
            headers = ["User ID", "Name", "Email", "Phone", "Created At"]
            print_header("ALL CUSTOMERS")
            print(tabulate(results, headers=headers, tablefmt="grid"))
        else:
            print_info("No customers found.")
        cursor.close()
    except Error as e:
        print_error(f"Error: {e}")

def add_customer(connection):
    """Add a new customer"""
    try:
        print_header("ADD NEW CUSTOMER")
        user_id = int(input("Enter User ID: "))
        name = input("Enter Name: ")
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        while True:
            email = input("Enter Email: ").strip()
            if re.match(email_pattern, email):
                break
            else:
                print_error("Invalid email format. Please enter a valid email address.")
        password = input("Enter Password: ")
        phone_pattern = r'^\d{10}$'
        while True:
            phone = input("Enter Phone Number (10 digits): ").strip()
            if re.match(phone_pattern, phone):
                break
            else:
                print_error("Invalid phone format. Please enter a 10-digit phone number.")

        
        cursor = connection.cursor()
        query = """INSERT INTO Customer (user_id, email, name, password, phone_no) 
                    VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(query, (user_id, email, name, password, phone))
        connection.commit()
        cursor.close()
        
        print_success("Customer added successfully!")
    except Error as e:
        print_error(f"Error: {e}")

def update_customer(connection):
    """Update customer details"""
    try:
        print_header("UPDATE CUSTOMER")
        user_id = int(input("Enter User ID to update: "))
        
        print("\nWhat would you like to update?")
        print("1. Name")
        print("2. Email")
        print("3. Phone Number")
        print("4. Password")
        choice = input("Enter choice (1-4): ")
        
        cursor = connection.cursor()
        
        if choice == '1':
            new_name = input("Enter new name: ")
            cursor.execute("UPDATE Customer SET name = %s WHERE user_id = %s", (new_name, user_id))
        elif choice == '2':
            new_email = input("Enter new email: ")
            cursor.execute("UPDATE Customer SET email = %s WHERE user_id = %s", (new_email, user_id))
        elif choice == '3':
            new_phone = input("Enter new phone: ")
            cursor.execute("UPDATE Customer SET phone_no = %s WHERE user_id = %s", (new_phone, user_id))
        elif choice == '4':
            new_password = input("Enter new password: ")
            cursor.execute("UPDATE Customer SET password = %s WHERE user_id = %s", (new_password, user_id))
        else:
            print_error("Invalid choice!")
            return
        
        connection.commit()
        cursor.close()
        print_success("Customer updated successfully!")
    except Error as e:
        print_error(f"Error: {e}")

def delete_customer(connection):
    """Delete a customer"""
    try:
        print_header("DELETE CUSTOMER")
        user_id = int(input("Enter User ID to delete: "))
        confirm = input(f"Are you sure you want to delete user {user_id}? (yes/no): ")
        
        if confirm.lower() == 'yes':
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Customer WHERE user_id = %s", (user_id,))
            connection.commit()
            cursor.close()
            print_success("Customer deleted successfully!")
        else:
            print_info("Deletion cancelled.")
    except Error as e:
        print_error(f"Error: {e}")

def customer_menu(connection):
    """Customer management submenu"""
    while True:
        print_header("CUSTOMER MANAGEMENT")
        print("1. View All Customers")
        print("2. Add New Customer")
        print("3. Update Customer")
        print("4. Delete Customer")
        print("0. Back to Main Menu")
        print(f"{Colors.CYAN}{'-'*70}{Colors.END}")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            view_all_customers(connection)
        elif choice == '2':
            add_customer(connection)
        elif choice == '3':
            update_customer(connection)
        elif choice == '4':
            delete_customer(connection)
        elif choice == '0':
            break
        else:
            print_error("Invalid choice! Please try again.")
        
        input("\nPress Enter to continue...")

# --- Habit Management ---

def view_all_habits(connection):
    """View all habits"""
    try:
        cursor = connection.cursor()
        query = """
        SELECT h.habit_id, c.name, h.name, h.start_date, h.frequency, h.is_active
        FROM Habit h
        JOIN Customer c ON h.user_id = c.user_id
        ORDER BY h.habit_id
        """
        cursor.execute(query)
        results = cursor.fetchall()
        
        if results:
            headers = ["Habit ID", "User", "Habit Name", "Start Date", "Frequency", "Active"]
            print_header("ALL HABITS")
            print(tabulate(results, headers=headers, tablefmt="grid"))
        else:
            print_info("No habits found.")
        cursor.close()
    except Error as e:
        print_error(f"Error: {e}")

def add_habit(connection):
    """Add a new habit"""
    try:
        print_header("ADD NEW HABIT")
        habit_id = int(input("Enter Habit ID: "))
        user_id = int(input("Enter User ID: "))
        name = input("Enter Habit Name: ")
        start_date = input("Enter Start Date (YYYY-MM-DD): ")
        
        print("\nSelect Frequency:")
        print("1. Daily")
        print("2. Weekly")
        print("3. Monthly")
        freq_choice = input("Enter choice (1-3): ")
        
        frequency_map = {'1': 'Daily', '2': 'Weekly', '3': 'Monthly'}
        frequency = frequency_map.get(freq_choice, 'Daily')
        
        cursor = connection.cursor()
        query = """INSERT INTO Habit (habit_id, user_id, name, start_date, frequency) 
                   VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(query, (habit_id, user_id, name, start_date, frequency))
        connection.commit()
        cursor.close()
        
        print_success("Habit added successfully!")
    except Error as e:
        print_error(f"Error: {e}")

def delete_habit(connection):
    """Delete a habit"""
    try:
        print_header("DELETE HABIT")
        habit_id = int(input("Enter Habit ID to delete: "))
        confirm = input(f"Are you sure you want to delete habit {habit_id}? (yes/no): ")
        
        if confirm.lower() == 'yes':
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Habit WHERE habit_id = %s", (habit_id,))
            connection.commit()
            cursor.close()
            print_success("Habit deleted successfully!")
        else:
            print_info("Deletion cancelled.")
    except Error as e:
        print_error(f"Error: {e}")

def habit_menu(connection):
    """Habit management submenu"""
    while True:
        print_header("HABIT MANAGEMENT")
        print("1. View All Habits")
        print("2. Add New Habit")
        print("3. Delete Habit")
        print("0. Back to Main Menu")
        print(f"{Colors.CYAN}{'-'*70}{Colors.END}")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            view_all_habits(connection)
        elif choice == '2':
            add_habit(connection)
        elif choice == '3':
            delete_habit(connection)
        elif choice == '0':
            break
        else:
            print_error("Invalid choice! Please try again.")
        
        input("\nPress Enter to continue...")

# --- Goal Management ---

def view_all_goals(connection):
    """View all goals"""
    try:
        cursor = connection.cursor()
        query = """
        SELECT g.goal_id, h.name, g.description, g.deadline, g.is_achieved
        FROM Goal g
        JOIN Habit h ON g.habit_id = h.habit_id
        ORDER BY g.goal_id
        """
        cursor.execute(query)
        results = cursor.fetchall()
        
        if results:
            headers = ["Goal ID", "Habit", "Description", "Deadline", "Achieved"]
            print_header("ALL GOALS")
            print(tabulate(results, headers=headers, tablefmt="grid"))
        else:
            print_info("No goals found.")
        cursor.close()
    except Error as e:
        print_error(f"Error: {e}")

def add_goal(connection):
    """Add a new goal"""
    try:
        print_header("ADD NEW GOAL")
        goal_id = int(input("Enter Goal ID: "))
        habit_id = int(input("Enter Habit ID: "))
        description = input("Enter Goal Description: ")
        deadline = input("Enter Deadline (YYYY-MM-DD): ")
        
        cursor = connection.cursor()
        query = """INSERT INTO Goal (goal_id, habit_id, deadline, description) 
                   VALUES (%s, %s, %s, %s)"""
        cursor.execute(query, (goal_id, habit_id, deadline, description))
        connection.commit()
        cursor.close()
        
        print_success("Goal added successfully!")
    except Error as e:
        print_error(f"Error: {e}")

def mark_goal_achieved(connection):
    """Mark a goal as achieved using stored procedure"""
    try:
        print_header("MARK GOAL AS ACHIEVED")
        goal_id = int(input("Enter Goal ID to mark as achieved: "))
        
        cursor = connection.cursor()
        cursor.callproc('MarkGoalAchieved', [goal_id])
        
        for result in cursor.stored_results():
            message = result.fetchone()
            if message:
                print_success(message[0])
        
        connection.commit()
        cursor.close()
    except Error as e:
        print_error(f"Error: {e}")

def goal_menu(connection):
    """Goal management submenu"""
    while True:
        print_header("GOAL MANAGEMENT")
        print("1. View All Goals")
        print("2. Add New Goal")
        print("3. Mark Goal as Achieved")
        print("0. Back to Main Menu")
        print(f"{Colors.CYAN}{'-'*70}{Colors.END}")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            view_all_goals(connection)
        elif choice == '2':
            add_goal(connection)
        elif choice == '3':
            mark_goal_achieved(connection)
        elif choice == '0':
            break
        else:
            print_error("Invalid choice! Please try again.")
        
        input("\nPress Enter to continue...")

# --- Log Management ---

def view_all_logs(connection):
    """View recent logs"""
    try:
        cursor = connection.cursor()
        query = """
        SELECT l.log_id, h.name, l.log_date, l.status, l.notes
        FROM Logs l
        JOIN Habit h ON l.habit_id = h.habit_id
        ORDER BY l.log_date DESC
        LIMIT 50
        """
        cursor.execute(query)
        results = cursor.fetchall()
        
        if results:
            headers = ["Log ID", "Habit", "Date", "Status", "Notes"]
            print_header("RECENT LOGS (50)")
            print(tabulate(results, headers=headers, tablefmt="grid"))
        else:
            print_info("No logs found.")
        cursor.close()
    except Error as e:
        print_error(f"Error: {e}")

def view_logs_by_habit(connection):
    """View logs for a specific habit"""
    try:
        print_header("VIEW LOGS BY HABIT")
        habit_id = int(input("Enter Habit ID: "))
        
        cursor = connection.cursor()
        query = """
        SELECT l.log_id, l.log_date, l.status, l.notes
        FROM Logs l
        WHERE l.habit_id = %s
        ORDER BY l.log_date DESC
        """
        cursor.execute(query, (habit_id,))
        results = cursor.fetchall()
        
        if results:
            headers = ["Log ID", "Date", "Status", "Notes"]
            print_header(f"LOGS FOR HABIT {habit_id}")
            print(tabulate(results, headers=headers, tablefmt="grid"))
        else:
            print_info("No logs found for this habit.")
        cursor.close()
    except Error as e:
        print_error(f"Error: {e}")

def add_log(connection):
    """Add a new log entry"""
    try:
        print_header("ADD NEW LOG")
        log_id = int(input("Enter Log ID: "))
        habit_id = int(input("Enter Habit ID: "))
        log_date = input("Enter Log Date (YYYY-MM-DD) or press Enter for today: ").strip()
        
        if not log_date:
            log_date = date.today().strftime('%Y-%m-%d')
        
        print("\nSelect Status:")
        print("1. Completed")
        print("2. Pending")
        print("3. Skipped")
        status_choice = input("Enter choice (1-3): ")
        
        status_map = {'1': 'Completed', '2': 'Pending', '3': 'Skipped'}
        status = status_map.get(status_choice, 'Pending')
        
        notes = input("Enter Notes: ")
        
        cursor = connection.cursor()
        query = """INSERT INTO Logs (log_id, habit_id, log_date, notes, status) 
                   VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(query, (log_id, habit_id, log_date, notes, status))
        connection.commit()
        cursor.close()
        
        print_success("Log added successfully!")
    except Error as e:
        print_error(f"Error: {e}")

def update_log_status(connection):
    """Update log status"""
    try:
        print_header("UPDATE LOG STATUS")
        log_id = int(input("Enter Log ID to update: "))
        
        print("\nSelect New Status:")
        print("1. Completed")
        print("2. Pending")
        print("3. Skipped")
        status_choice = input("Enter choice (1-3): ")
        
        status_map = {'1': 'Completed', '2': 'Pending', '3': 'Skipped'}
        new_status = status_map.get(status_choice, 'Pending')
        
        cursor = connection.cursor()
        cursor.execute("UPDATE Logs SET status = %s WHERE log_id = %s", (new_status, log_id))
        connection.commit()
        cursor.close()
        
        print_success("Log status updated successfully!")
    except Error as e:
        print_error(f"Error: {e}")

def log_menu(connection):
    """Log management submenu"""
    while True:
        print_header("LOG MANAGEMENT")
        print("1. View All Recent Logs")
        print("2. View Logs by Habit")
        print("3. Add New Log")
        print("4. Update Log Status")
        print("0. Back to Main Menu")
        print(f"{Colors.CYAN}{'-'*70}{Colors.END}")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            view_all_logs(connection)
        elif choice == '2':
            view_logs_by_habit(connection)
        elif choice == '3':
            add_log(connection)
        elif choice == '4':
            update_log_status(connection)
        elif choice == '0':
            break
        else:
            print_error("Invalid choice! Please try again.")
        
        input("\nPress Enter to continue...")

# --- Reports & Analytics ---

def user_performance_summary(connection):
    """Generate user performance summary"""
    try:
        cursor = connection.cursor()
        query = """
        SELECT 
            c.user_id,
            c.name,
            COUNT(DISTINCT h.habit_id) AS total_habits,
            COUNT(l.log_id) AS total_logs,
            SUM(CASE WHEN l.status = 'Completed' THEN 1 ELSE 0 END) AS completed_logs,
            ROUND(AVG(CASE WHEN l.status = 'Completed' THEN 100 ELSE 0 END), 2) AS avg_completion_rate
        FROM Customer c
        LEFT JOIN Habit h ON c.user_id = h.user_id
        LEFT JOIN Logs l ON h.habit_id = l.habit_id
        GROUP BY c.user_id, c.name
        HAVING COUNT(l.log_id) > 0
        ORDER BY avg_completion_rate DESC
        """
        cursor.execute(query)
        results = cursor.fetchall()
        
        if results:
            headers = ["User ID", "Name", "Habits", "Total Logs", "Completed", "Completion %"]
            print_header("USER PERFORMANCE SUMMARY")
            print(tabulate(results, headers=headers, tablefmt="grid"))
        else:
            print_info("No performance data found.")
        cursor.close()
    except Error as e:
        print_error(f"Error: {e}")

def habit_performance_report(connection):
    """Generate habit performance report"""
    try:
        cursor = connection.cursor()
        query = """
        SELECT 
            h.name AS habit_name,
            COUNT(l.log_id) AS total_logs,
            SUM(CASE WHEN l.status = 'Completed' THEN 1 ELSE 0 END) AS completed,
            SUM(CASE WHEN l.status = 'Skipped' THEN 1 ELSE 0 END) AS skipped,
            SUM(CASE WHEN l.status = 'Pending' THEN 1 ELSE 0 END) AS pending,
            ROUND(AVG(CASE WHEN l.status = 'Completed' THEN 100 ELSE 0 END), 2) AS completion_rate
        FROM Habit h
        LEFT JOIN Logs l ON h.habit_id = l.habit_id
        GROUP BY h.habit_id, h.name
        HAVING COUNT(l.log_id) > 0
        ORDER BY completion_rate DESC
        """
        cursor.execute(query)
        results = cursor.fetchall()
        
        if results:
            headers = ["Habit", "Total Logs", "Completed", "Skipped", "Pending", "Completion %"]
            print_header("HABIT PERFORMANCE REPORT")
            print(tabulate(results, headers=headers, tablefmt="grid"))
        else:
            print_info("No performance data found.")
        cursor.close()
    except Error as e:
        print_error(f"Error: {e}")

def reports_menu(connection):
    """Reports and analytics submenu"""
    while True:
        print_header("REPORTS & ANALYTICS")
        print("1. User Performance Summary")
        print("2. Habit Performance Report")
        print("0. Back to Main Menu")
        print(f"{Colors.CYAN}{'-'*70}{Colors.END}")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            user_performance_summary(connection)
        elif choice == '2':
            habit_performance_report(connection)
        elif choice == '0':
            break
        else:
            print_error("Invalid choice! Please try again.")
        
        input("\nPress Enter to continue...")

# --- Advanced Queries ---

def users_above_average(connection):
    """Nested query - Users with above average performance"""
    try:
        cursor = connection.cursor()
        query = """
        SELECT 
            c.user_id,
            c.name,
            COUNT(CASE WHEN l.status = 'Completed' THEN 1 END) AS completed_logs
        FROM Customer c
        JOIN Habit h ON c.user_id = h.user_id
        JOIN Logs l ON h.habit_id = l.habit_id
        GROUP BY c.user_id, c.name
        HAVING COUNT(CASE WHEN l.status = 'Completed' THEN 1 END) > (
            SELECT AVG(completed_count)
            FROM (
                SELECT COUNT(CASE WHEN status = 'Completed' THEN 1 END) AS completed_count
                FROM Logs
                GROUP BY habit_id
            ) AS avg_table
        )
        ORDER BY completed_logs DESC
        """
        cursor.execute(query)
        results = cursor.fetchall()
        
        if results:
            headers = ["User ID", "Name", "Completed Logs"]
            print_header("USERS WITH ABOVE AVERAGE PERFORMANCE")
            print(tabulate(results, headers=headers, tablefmt="grid"))
        else:
            print_info("No users found above average.")
        cursor.close()
    except Error as e:
        print_error(f"Error: {e}")

def habits_with_goals(connection):
    """Join query - Habits with their goals"""
    try:
        cursor = connection.cursor()
        query = """
        SELECT 
            c.name AS user_name,
            h.name AS habit_name,
            h.frequency,
            g.description AS goal_description,
            g.deadline,
            g.is_achieved
        FROM Customer c
        JOIN Habit h ON c.user_id = h.user_id
        LEFT JOIN Goal g ON h.habit_id = g.habit_id
        ORDER BY c.name, h.name
        """
        cursor.execute(query)
        results = cursor.fetchall()
        
        if results:
            headers = ["User", "Habit", "Frequency", "Goal", "Deadline", "Achieved"]
            print_header("HABITS WITH GOALS (JOIN QUERY)")
            print(tabulate(results, headers=headers, tablefmt="grid"))
        else:
            print_info("No data found.")
        cursor.close()
    except Error as e:
        print_error(f"Error: {e}")

def overdue_goals(connection):
    """Find users with overdue goals"""
    try:
        cursor = connection.cursor()
        query = """
        SELECT DISTINCT
            c.user_id,
            c.name,
            g.goal_id,
            g.description,
            g.deadline,
            DATEDIFF(CURRENT_DATE, g.deadline) AS days_overdue
        FROM Customer c
        JOIN Habit h ON c.user_id = h.user_id
        JOIN Goal g ON h.habit_id = g.habit_id
        WHERE g.deadline < CURRENT_DATE AND g.is_achieved = FALSE
        ORDER BY days_overdue DESC
        """
        cursor.execute(query)
        results = cursor.fetchall()
        
        if results:
            headers = ["User ID", "Name", "Goal ID", "Description", "Deadline", "Days Overdue"]
            print_header("OVERDUE GOALS")
            print(tabulate(results, headers=headers, tablefmt="grid"))
        else:
            print_info("No overdue goals found.")
        cursor.close()
    except Error as e:
        print_error(f"Error: {e}")

def advanced_queries_menu(connection):
    """Advanced queries submenu"""
    while True:
        print_header("ADVANCED QUERIES")
        print("1. Users with Above Average Performance (Nested Query)")
        print("2. Habits with Goals (Join Query)")
        print("3. Overdue Goals")
        print("0. Back to Main Menu")
        print(f"{Colors.CYAN}{'-'*70}{Colors.END}")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            users_above_average(connection)
        elif choice == '2':
            habits_with_goals(connection)
        elif choice == '3':
            overdue_goals(connection)
        elif choice == '0':
            break
        else:
            print_error("Invalid choice! Please try again.")
        
        input("\nPress Enter to continue...")

# --- Testing Menu ---

def test_single_function_trigger(connection):
    """Test the single remaining function and trigger"""
    while True:
        print_header("TEST SINGLE FUNCTION & TRIGGER")
        print(f"1. Test Function: {Colors.BOLD}GetHabitCompletionRate{Colors.END}")
        print(f"2. Test Trigger: {Colors.BOLD}before_log_insert{Colors.END} (Add Log)")
        print(f"3. Test Procedure: {Colors.BOLD}MarkGoalAchieved{Colors.END} (Goal Menu)")
        print("0. Back to Main Menu")
        print(f"{Colors.CYAN}{'-'*70}{Colors.END}")
        
        choice = input("Enter your choice: ")
        
        try:
            if choice == '1':
                # Test GetHabitCompletionRate
                habit_id = int(input("Enter Habit ID to check completion rate (e.g., 201): "))
                cursor = connection.cursor()
                cursor.execute("SELECT GetHabitCompletionRate(%s)", (habit_id,))
                result = cursor.fetchone()
                print_success(f"Completion Rate for Habit {habit_id}: {result[0]}%")
                cursor.close()
            elif choice == '2':
                # Test before_log_insert (Add Log)
                add_log(connection)
            elif choice == '3':
                # Redirect to Goal Menu to test MarkGoalAchieved Procedure
                goal_menu(connection)
            elif choice == '0':
                break
            else:
                print_error("Invalid choice! Please try again.")
        except Error as e:
            print_error(f"Error during test: {e}")
            
        input("\nPress Enter to continue...")

# --- CLI Main Function ---

def main_cli():
    """Main CLI function"""
    connection = get_db_connection()
    
    if not connection:
        print_error("Failed to connect to database. Exiting...")
        sys.exit(1)
    
    print_success("Connected to database successfully!")
    
    try:
        while True:
            clear_screen()
            display_main_menu()
            choice = input(f"\n{Colors.BOLD}Enter your choice: {Colors.END}")
            
            if choice == '1':
                customer_menu(connection)
            elif choice == '2':
                habit_menu(connection)
            elif choice == '3':
                goal_menu(connection)
            elif choice == '4':
                log_menu(connection)
            elif choice == '5':
                reports_menu(connection)
            elif choice == '6':
                advanced_queries_menu(connection)
            elif choice == '7':
                test_single_function_trigger(connection)
            elif choice == '0':
                print_info("Thank you for using Personal Habit Tracker!")
                break
            else:
                print_error("Invalid choice! Please try again.")
                input("\nPress Enter to continue...")
    
    except KeyboardInterrupt:
        print_info("\n\nProgram interrupted by user.")
    
    finally:
        if connection and connection.open:
            connection.close()
            print_success("Database connection closed.")

# --- GUI Functions ---

def run_thread(func, conn):
    """Run function in a separate thread"""
    threading.Thread(target=func, args=(conn,), daemon=True).start()

def main_gui():
    """Main GUI function"""
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

# --- Mode Selection GUI ---

def select_mode_gui():
    """Show a GUI window to select between CLI and GUI mode"""
    root = tk.Tk()
    root.title("Personal Habit Tracker - Mode Selection")
    root.geometry("400x300")
    root.configure(bg="#1e1e2e")
    root.resizable(False, False)
    
    selected_mode = {"mode": None}
    
    def select_cli():
        selected_mode["mode"] = "cli"
        root.destroy()
    
    def select_gui():
        selected_mode["mode"] = "gui"
        root.destroy()
    
    tk.Label(
        root,
        text="Personal Habit Tracker",
        font=("Helvetica", 18, "bold"),
        fg="white",
        bg="#1e1e2e"
    ).pack(pady=30)
    
    tk.Label(
        root,
        text="Select Interface Mode",
        font=("Helvetica", 12),
        fg="gray",
        bg="#1e1e2e"
    ).pack(pady=10)
    
    btn_style = {
        "width": 25,
        "height": 2,
        "bg": "#313244",
        "fg": "white",
        "font": ("Helvetica", 11),
        "activebackground": "#45475a"
    }
    
    tk.Button(
        root,
        text="CLI Mode (Command Line)",
        command=select_cli,
        **btn_style
    ).pack(pady=10)
    
    tk.Button(
        root,
        text="GUI Mode (Graphical)",
        command=select_gui,
        **btn_style
    ).pack(pady=10)
    
    root.mainloop()
    return selected_mode["mode"]

# --- Entry Point ---

if __name__ == "__main__":
    import sys
    
    # Check if running from command line with arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--gui":
            main_gui()
        elif sys.argv[1] == "--cli":
            main_cli()
        else:
            print("Usage: personal_habit_tracker.py [--cli|--gui]")
            sys.exit(1)
    else:
        # Check if stdin is available (running in console)
        try:
            if sys.stdin and sys.stdin.isatty():
                # Console mode - show text menu
                print("\nPersonal Habit Tracker")
                print("=" * 50)
                print("Choose interface mode:")
                print("1. CLI (Command Line Interface)")
                print("2. GUI (Graphical User Interface)")
                print("=" * 50)
                
                choice = input("\nEnter your choice (1 or 2): ").strip()
                
                if choice == "1":
                    main_cli()
                elif choice == "2":
                    main_gui()
                else:
                    print("Invalid choice. Defaulting to GUI mode...")
                    main_gui()
            else:
                # No console available - use GUI selector
                mode = select_mode_gui()
                if mode == "cli":
                    main_cli()
                elif mode == "gui":
                    main_gui()
                else:
                    # User closed the window - exit
                    sys.exit(0)
        except:
            # If any error occurs, default to GUI mode selector
            mode = select_mode_gui()
            if mode == "cli":
                main_cli()
            elif mode == "gui":
                main_gui()
            else:

                sys.exit(0)
