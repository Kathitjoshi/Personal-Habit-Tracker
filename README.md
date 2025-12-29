# Personal Habit Tracker

A database-driven habit tracking system built with MySQL, Python, and Tkinter that enables users to create, monitor, and analyze their daily habits through structured tracking mechanisms, goal setting, and performance analytics.


## Overview

The Personal Habit Tracker provides complete lifecycle management from user registration to performance analytics. Users can create multiple habits with customizable frequencies, set specific goals with deadlines, maintain detailed daily logs, and analyze performance through comprehensive reports.**Note: Don't forget to change password section in code.py to your mysql server's**

## Features

### User Management
- User registration with email and phone validation
- Profile updates for name, email, phone, and password
- Account deletion with cascading cleanup
- View all registered customers

### Habit Management
- Create habits with start date and frequency (Daily/Weekly/Monthly)
- View all habits with user information
- Delete habits with automatic cleanup

### Goal Management
- Create goals with deadlines and descriptions
- View all goals with achievement status
- Mark goals as achieved via stored procedure

### Logging System
- Create log entries with status (Completed/Pending/Skipped) and notes
- View recent logs across all habits
- View logs filtered by specific habit
- Update log status

### Analytics and Reports
- Calculate habit completion rates
- Generate user performance summaries
- Generate habit performance reports
- Identify above-average performers
- Display habits with associated goals
- Identify and report overdue goals

## Technology Stack

### Database
- MySQL Server 8.0
- MySQL Workbench 8.0

### Programming Languages
- SQL (queries, procedures, functions, triggers)
- Python 3.9

### Python Libraries
- mysql-connector-python 8.0.33 (database connectivity)
- tabulate 0.9.0 (formatted table output)
- tkinter (GUI interface)
- re (input validation)
- datetime (date handling)

## Database Schema

### Tables

**Customer**
- user_id (Primary Key)
- email (Unique)
- name
- password
- phone_no
- created_at

**Habit**
- habit_id (Primary Key)
- user_id (Foreign Key)
- name
- start_date
- frequency (Daily/Weekly/Monthly)
- is_active

**Goal**
- goal_id (Primary Key)
- habit_id (Foreign Key)
- deadline
- description
- is_achieved

**Logs**
- log_id (Primary Key)
- habit_id (Foreign Key)
- log_date
- notes
- status (Completed/Pending/Skipped)

## Database Objects

### Stored Procedure

**MarkGoalAchieved**
- Updates goal achievement status
- Parameters: goal_id
- Sets is_achieved to TRUE for specified goal

```sql
CALL MarkGoalAchieved(301);
```

### Function

**GetHabitCompletionRate**
- Calculates habit completion percentage
- Parameters: habit_id
- Returns: DECIMAL(5,2)
- Handles zero division cases

```sql
SELECT GetHabitCompletionRate(201);
```

### Trigger

**before_log_insert**
- Validates log dates against habit start dates
- Prevents insertion if log_date is before habit start_date
- Ensures data integrity

## Installation

### Prerequisites
- Python 3.9 or higher
- MySQL Server 8.0 or higher
- pip (Python package manager)

### Setup Steps

1. Clone the repository
```bash
git clone https://github.com/Kathitjoshi/Personal-Habit-Tracker.git
cd Personal-Habit-Tracker
```

2. Install required Python packages
```bash
pip install mysql-connector-python tabulate
```

3. Set up the database
- Open MySQL Workbench or MySQL command line
- Run the project.sql file to create the database and tables
```bash
mysql -u your_username -p < project.sql
```

4. Configure database connection
- Open code.py
- Update the database connection parameters:
```python
connection = mysql.connector.connect(
    host='localhost',
    user='your_username',
    password='your_password',
    database='project'
)
```

## Usage

### Running the CLI Application
```bash
python code.py
```

### Running the GUI Application
```bash
python gui.py
```

### Main Menu Options

1. Customer Management - Add, view, update, or delete customers
2. Habit Management - Manage user habits
3. Goal Management - Set and track goals
4. Log Management - Record and view daily logs
5. Reports & Analytics - View performance statistics
6. Advanced Queries - Run complex database queries
7. Test Function/Trigger/Procedure - Test database objects

## Key Queries

### Above Average Users
Finds users with completed logs above the average:
```sql
SELECT c.user_id, c.name, 
       COUNT(CASE WHEN l.status = 'Completed' THEN 1 END) AS completed_logs
FROM Customer c
JOIN Habit h ON c.user_id = h.user_id
JOIN Logs l ON h.habit_id = l.habit_id
GROUP BY c.user_id, c.name
HAVING COUNT(CASE WHEN l.status = 'Completed' THEN 1 END) > (
    SELECT AVG(completed_count)
    FROM (
        SELECT COUNT(CASE WHEN status = 'Completed' THEN 1 END) AS completed_count
        FROM Logs GROUP BY habit_id
    ) AS avg_table
)
ORDER BY completed_logs DESC;
```

### Habit Performance Statistics
```sql
SELECT h.name AS habit_name,
       COUNT(l.log_id) AS total_logs,
       SUM(CASE WHEN l.status = 'Completed' THEN 1 ELSE 0 END) AS completed,
       SUM(CASE WHEN l.status = 'Skipped' THEN 1 ELSE 0 END) AS skipped,
       SUM(CASE WHEN l.status = 'Pending' THEN 1 ELSE 0 END) AS pending,
       ROUND(AVG(CASE WHEN l.status = 'Completed' THEN 100 ELSE 0 END), 2) AS completion_rate
FROM Habit h
LEFT JOIN Logs l ON h.habit_id = l.habit_id
GROUP BY h.habit_id, h.name
HAVING COUNT(l.log_id) > 0
ORDER BY completion_rate DESC;
```

## Data Integrity Features

- Foreign key constraints for referential integrity
- Check constraints for valid frequency and status values
- Trigger validation for log dates
- Cascading deletes for maintaining consistency
- Transaction management for data consistency
- Input validation for all user entries

## Project Structure

```
personal-habit-tracker/
├── project.sql          # Complete database schema and queries
├── code.py              # Python CLI application
├── gui.py               # Tkinter GUI application
├── README.md            # Project documentation
└── Report.pdf           # Detailed project report
```

## Contributing

This is an academic project for Database Management Systems course. For any issues or suggestions, please contact the team members.



## Contact

- Kathit Joshi - Check profile for contact
