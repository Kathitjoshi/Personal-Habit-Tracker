"""
Personal Habit Tracker - CLI Application
Team Members: Kathit Joshi (PES2UG23CS264), Kavyansh Jain (PES2UG23CS268)
NOTE: This Python file has been simplified to match the reduced SQL file 
      (1 Function: GetHabitCompletionRate, 1 Procedure: MarkGoalAchieved, 
      1 Trigger: before_log_insert).
"""

import mysql.connector
from mysql.connector import Error
from datetime import datetime, date
from tabulate import tabulate
import os
import sys
import re

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
        connection = mysql.connector.connect(
            host='localhost',
            database='project',
            user='root',  
            password='<password>'   
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print_error(f"Error connecting to MySQL: {e}")
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

# --- Customer Management (No changes needed) ---

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

# --- Habit Management (Modified to remove missing procedures) ---

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

# NOTE: AddNewHabit and GetUserHabitSummary procedures were removed from the SQL. 
# Re-implementing Add New Habit with direct SQL for full functionality.
def add_habit_direct(connection):
    """Add habit using direct SQL (since AddNewHabit proc was removed/simplified out)"""
    try:
        print_header("ADD NEW HABIT (Direct SQL)")
        habit_id = int(input("Enter Habit ID: "))
        user_id = int(input("Enter User ID: "))
        name = input("Enter Habit Name: ")
        start_date = input("Enter Start Date (YYYY-MM-DD): ")
        
        print("\nFrequency Options:")
        print("1. Daily")
        print("2. Weekly")
        print("3. Monthly")
        freq_choice = input("Select frequency (1-3): ")
        
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

# NOTE: GetUserHabitSummary procedure was removed from the SQL. Removed the corresponding menu item.

def delete_habit(connection):
    """Delete a habit (Tests the single before_habit_delete trigger if still in SQL)"""
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
        # This will catch the 'Cannot delete habit with active goals' error if the trigger is present
        print_error(f"Error: {e}") 

def habit_menu(connection):
    """Habit management submenu"""
    while True:
        print_header("HABIT MANAGEMENT")
        print("1. View All Habits")
        print("2. Add New Habit")
        print("3. Delete Habit (Tests Trigger if active goals exist)")
        print("0. Back to Main Menu")
        print(f"{Colors.CYAN}{'-'*70}{Colors.END}")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            view_all_habits(connection)
        elif choice == '2':
            add_habit_direct(connection)
        elif choice == '3':
            delete_habit(connection)
        elif choice == '0':
            break
        else:
            print_error("Invalid choice! Please try again.")
        
        input("\nPress Enter to continue...")

# --- Goal Management (Modified to reflect MarkGoalAchieved is the ONLY procedure) ---

def view_all_goals(connection):
    """View all goals"""
    try:
        cursor = connection.cursor()
        query = """
        SELECT g.goal_id, h.name, g.description, g.deadline, g.is_achieved
        FROM Goal g
        JOIN Habit h ON g.habit_id = h.habit_id
        ORDER BY g.deadline
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
        deadline = input("Enter Deadline (YYYY-MM-DD): ")
        description = input("Enter Goal Description: ")
        
        cursor = connection.cursor()
        query = "INSERT INTO Goal (goal_id, habit_id, deadline, description) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (goal_id, habit_id, deadline, description))
        connection.commit()
        cursor.close()
        
        print_success("Goal added successfully!")
    except Error as e:
        print_error(f"Error: {e}")

def mark_goal_achieved(connection):
    """Mark goal as achieved using the MarkGoalAchieved stored procedure"""
    try:
        print_header("MARK GOAL AS ACHIEVED (Stored Procedure)")
        goal_id = int(input("Enter Goal ID: "))
        
        cursor = connection.cursor()
        # This is the single, remaining stored procedure
        cursor.callproc('MarkGoalAchieved', [goal_id])
        
        for result in cursor.stored_results():
            print_success(result.fetchone()[0])
        
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
        print("3. Mark Goal as Achieved (Stored Procedure)")
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

# --- Log Management (Modified to reflect ONLY one trigger: before_log_insert) ---

def view_all_logs(connection):
    """View all logs"""
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
            print_header("RECENT LOGS (Last 50)")
            print(tabulate(results, headers=headers, tablefmt="grid"))
        else:
            print_info("No logs found.")
        cursor.close()
    except Error as e:
        print_error(f"Error: {e}")

def add_log(connection):
    """Add a new log (Tests the single before_log_insert trigger)"""
    try:
        print_header("ADD NEW LOG (Tests 'before_log_insert' Trigger)")
        log_id = int(input("Enter Log ID: "))
        habit_id = int(input("Enter Habit ID: "))
        
        # Prompt for a date that might be before the habit's start date to test the trigger
        print_info("Enter a log date *before* the habit's start date (e.g., 2024-08-30 for habit 201) to test the trigger.")
        log_date = input("Enter Log Date (YYYY-MM-DD) [Press Enter for today]: ")
        if not log_date:
            log_date = date.today().strftime('%Y-%m-%d')
        
        print("\nStatus Options:")
        print("1. Completed")
        print("2. Pending")
        print("3. Skipped")
        status_choice = input("Select status (1-3): ")
        
        status_map = {'1': 'Completed', '2': 'Pending', '3': 'Skipped'}
        status = status_map.get(status_choice, 'Pending')
        
        notes = input("Enter notes (optional): ")
        
        cursor = connection.cursor()
        query = """INSERT INTO Logs (log_id, habit_id, log_date, notes, status) 
                    VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(query, (log_id, habit_id, log_date, notes, status))
        connection.commit()
        cursor.close()
        
        print_success("Log added successfully! ('before_log_insert' trigger passed/executed)")
    except Error as e:
        # This catches the SQLSTATE '45000' error from the trigger
        print_error(f"Error: {e}")

def update_log_status(connection):
    """Update log status"""
    try:
        print_header("UPDATE LOG STATUS")
        log_id = int(input("Enter Log ID to update: "))
        
        print("\nNew Status Options:")
        print("1. Completed")
        print("2. Pending")
        print("3. Skipped")
        status_choice = input("Select new status (1-3): ")
        
        status_map = {'1': 'Completed', '2': 'Pending', '3': 'Skipped'}
        new_status = status_map.get(status_choice, 'Pending')
        
        cursor = connection.cursor()
        cursor.execute("UPDATE Logs SET status = %s WHERE log_id = %s", (new_status, log_id))
        connection.commit()
        cursor.close()
        
        print_success("Log status updated!")
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
            print(tabulate(results, headers=headers, tablefmt="grid"))
        else:
            print_info("No logs found for this habit.")
        cursor.close()
    except Error as e:
        print_error(f"Error: {e}")

def log_menu(connection):
    """Log management submenu"""
    while True:
        print_header("LOG MANAGEMENT")
        print("1. View All Recent Logs")
        print("2. View Logs by Habit")
        print("3. Add New Log (Tests 'before_log_insert' Trigger)")
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

# --- Reports & Analytics (No changes needed, queries are standard SQL) ---

def user_performance_summary(connection):
    """View user performance summary"""
    try:
        cursor = connection.cursor()
        query = """
        SELECT 
            c.user_id,
            c.name,
            COUNT(DISTINCT h.habit_id) AS total_habits,
            COUNT(CASE WHEN l.status = 'Completed' THEN 1 END) AS completed_logs,
            COUNT(CASE WHEN l.status = 'Skipped' THEN 1 END) AS skipped_logs,
            ROUND(AVG(CASE WHEN l.status = 'Completed' THEN 100 ELSE 0 END), 2) AS avg_completion_rate
        FROM Customer c
        LEFT JOIN Habit h ON c.user_id = h.user_id
        LEFT JOIN Logs l ON h.habit_id = l.habit_id
        GROUP BY c.user_id, c.name
        ORDER BY avg_completion_rate DESC
        """
        cursor.execute(query)
        results = cursor.fetchall()
        
        if results:
            headers = ["User ID", "Name", "Total Habits", "Completed", "Skipped", "Completion %"]
            print_header("USER PERFORMANCE SUMMARY")
            print(tabulate(results, headers=headers, tablefmt="grid"))
        else:
            print_info("No data found.")
        cursor.close()
    except Error as e:
        print_error(f"Error: {e}")

def habit_performance_report(connection):
    """Aggregate query - Habit performance"""
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
            headers = ["Habit", "Total", "Completed", "Skipped", "Pending", "Rate %"]
            print_header("HABIT PERFORMANCE REPORT")
            print(tabulate(results, headers=headers, tablefmt="grid"))
        else:
            print_info("No data available.")
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

# --- Advanced Queries (No changes needed, queries are standard SQL) ---

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

# --- Simplified Testing Menu (Updated to ONLY test remaining 1 function and 1 trigger) ---

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


def main():
    """Main function"""
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
                # Renamed the menu item to reflect the simplified structure
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
        if connection.is_connected():
            connection.close()
            print_success("Database connection closed.")

if __name__ == "__main__":
    main()