# Personal Habit Tracker

A comprehensive database-driven habit tracking application built with MySQL and Python, featuring both CLI and GUI interfaces for flexible user interaction.

## Overview

The Personal Habit Tracker is a full-featured database management system that helps users build and maintain positive habits through structured tracking, goal setting, and performance analytics. Built as a DBMS course project, it demonstrates practical implementation of advanced database concepts including normalized schema design, stored procedures, user-defined functions, triggers, and complex SQL queries.

## Team Members

- **Kathit Joshi** (PES2UG23CS264)



## Key Features

### User Management
- User registration with email and phone validation
- Profile updates for name, email, phone, and password
- Account deletion with automatic cascading cleanup
- Complete customer directory viewing

### Habit Management
- Create habits with customizable frequencies (Daily/Weekly/Monthly)
- Track habit start dates and active status
- View all habits with associated user information
- Delete habits with automatic cleanup of related data

### Goal Management
- Set specific goals with deadlines and descriptions
- Track goal achievement status
- Mark goals as achieved using stored procedures
- Monitor progress relative to deadlines

### Log Management
- Daily activity logging with status tracking (Completed/Pending/Skipped)
- Add custom notes to each log entry
- View recent logs across all habits
- Filter logs by specific habit
- Update log status to reflect progress

### Analytics and Reports
- Calculate habit completion rates using database functions
- Generate user performance summaries with statistics
- Create habit performance reports
- Identify above-average performers
- Display habits with associated goals
- Report overdue goals with days-overdue calculation

### Data Integrity
- Foreign key constraints for referential integrity
- Check constraints for valid values
- Trigger-based validation for log dates
- Cascading deletes for data consistency
- Input validation with regex patterns
- Transaction management

## Technology Stack

### Database
- MySQL Server 8.0 - Relational database management
- MySQL Workbench 8.0 - Database design and administration

### Programming
- Python 3.9+ - Application logic and interface
- SQL - Queries, procedures, functions, and triggers

### Libraries
- **PyMySQL** - Pure Python MySQL client (PyInstaller compatible)
- **tabulate** - Formatted table output for CLI
- **tkinter** - Built-in GUI framework
- **re** - Input validation with regex
- **datetime** - Date and time handling
- **threading** - Multi-threaded GUI execution

### Tools
- Visual Studio Code - Code editor
- Git - Version control
- GitHub - Repository hosting
- PyInstaller - Executable creation

## Database Schema

### Tables

**Customer**
- Primary Key: user_id
- Fields: email (unique), name, password, phone_no, created_at
- Stores user account information

**Habit**
- Primary Key: habit_id
- Foreign Key: user_id references Customer
- Fields: name, start_date, frequency, is_active
- Tracks user habits with frequency settings

**Goal**
- Primary Key: goal_id
- Foreign Key: habit_id references Habit
- Fields: deadline, description, is_achieved
- Manages habit-specific goals

**Logs**
- Primary Key: log_id
- Foreign Key: habit_id references Habit
- Fields: log_date, notes, status
- Records daily habit completion

## Database Objects

### Stored Procedure: MarkGoalAchieved
Updates goal achievement status and provides confirmation.

```sql
CALL MarkGoalAchieved(goal_id);
```

### Function: GetHabitCompletionRate
Calculates habit completion percentage with zero-division handling.

```sql
SELECT GetHabitCompletionRate(habit_id);
```

### Trigger: before_log_insert
Validates log dates to ensure they are not before habit start dates.

## Installation

### Prerequisites
- Python 3.9 or higher
- MySQL Server 8.0 or higher
- pip package manager

### Setup Steps

1. **Clone the Repository**
```bash
git clone https://github.com/Kathitjoshi/Personal-Habit-Tracker.git
cd Personal-Habit-Tracker
```

2. **Install Python Dependencies**
```bash
pip install PyMySQL tabulate
```

3. **Set Up MySQL Database**
```bash
mysql -u root -p < project.sql
```

Or manually run the SQL file in MySQL Workbench.

4. **Configure Database Connection**

Edit `personal_habit_tracker_fixed.py` and update the password on line 62:
```python
password='your_mysql_password'
```

5. **Run the Application**
```bash
python personal_habit_tracker_fixed.py
```

## Usage

### Running the Application

**Interactive Mode (Default)**
```bash
python personal_habit_tracker_fixed.py
```
Choose CLI or GUI when prompted.

**Direct CLI Mode**
```bash
python personal_habit_tracker_fixed.py --cli
```

**Direct GUI Mode**
```bash
python personal_habit_tracker_fixed.py --gui
```

### Main Features

1. **Customer Management** - Add, view, update, or delete users
2. **Habit Management** - Create and manage user habits
3. **Goal Management** - Set and track goals with deadlines
4. **Log Management** - Record and view daily activity logs
5. **Reports & Analytics** - View performance statistics
6. **Advanced Queries** - Execute complex database queries
7. **Testing Module** - Test functions, triggers, and procedures

## Building Executable

### Create Standalone Application

1. **Install PyInstaller**
```bash
pip install pyinstaller
```

2. **Build the Executable**
```bash
pyinstaller --onefile --console --name="PersonalHabitTracker" --hidden-import=pymysql personal_habit_tracker_fixed.py
```

3. **Locate the Executable**
```
dist/PersonalHabitTracker.exe
```

### For GUI-Only Version
```bash
pyinstaller --onefile --noconsole --name="PersonalHabitTracker_GUI" --hidden-import=pymysql personal_habit_tracker_fixed.py
```

## Advanced SQL Queries

### Users Above Average Performance
Identifies users with above-average habit completion using nested queries.

### Habits with Goals
Displays comprehensive habit information with associated goals using JOIN operations.

### Habit Performance Statistics
Generates detailed metrics using aggregate functions.

### Overdue Goals
Finds goals past their deadline using date-based filtering.

## Project Structure

```
personal-habit-tracker/
├── personal_habit_tracker_fixed.py  # Main application file
├── project.sql                      # Database schema and sample data
├── README.md                        # Project documentation
├── Report.pdf                       # Detailed project report
├── PERSONAL_HABIT_TRACKER.pdf       # ER diagram and schema
├── BUILD_GUIDE.md                   # Deployment instructions
└── install_pymysql.bat              # Quick setup script
```

## Sample Data

The project includes sample data for testing:
- 5 customer records
- 7 habit records
- 7 goal records
- 16 log records

## Screenshots

The application features:
- Color-coded CLI output for better readability
- Formatted table displays using tabulate
- Dark-themed GUI with modern styling
- Input validation with helpful error messages
- Confirmation dialogs for destructive operations

## Contributing

For issues or suggestions, please open an issue on GitHub.

## License

MIT License

## Acknowledgments

- PES University for providing the learning environment
- Database Management Systems course instructors
- MySQL and Python communities
- Open-source libraries: PyMySQL, tabulate, tkinter

## Contact

**Repository:** [https://github.com/Kathitjoshi/Personal-Habit-Tracker](https://github.com/Kathitjoshi/Personal-Habit-Tracker)

For queries or support, please contact the team members through GitHub.

---

**Built with Python, MySQL, and dedication to database management excellence.**
