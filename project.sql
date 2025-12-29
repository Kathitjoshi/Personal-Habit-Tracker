-- ============================================================
-- Personal Habit Tracker Database Schema (Simplified Version)
-- Team Members: Kathit Joshi (PES2UG23CS264), Kavyansh Jain (PES2UG23CS268)
-- ============================================================

CREATE DATABASE IF NOT EXISTS project;
USE project;

-- ============================================================
-- TABLE CREATION
-- ============================================================

CREATE TABLE Customer (
    user_id INT PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone_no VARCHAR(15) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Habit (
    habit_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    frequency VARCHAR(20) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    CONSTRAINT fk_habit_customer FOREIGN KEY (user_id)
        REFERENCES Customer(user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT chk_frequency CHECK (frequency IN ('Daily', 'Weekly', 'Monthly'))
);

CREATE TABLE Goal (
    goal_id INT PRIMARY KEY,
    habit_id INT NOT NULL,
    deadline DATE NOT NULL,
    description TEXT NOT NULL,
    is_achieved BOOLEAN DEFAULT FALSE,
    CONSTRAINT fk_goal_habit FOREIGN KEY (habit_id)
        REFERENCES Habit(habit_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Logs (
    log_id INT PRIMARY KEY,
    habit_id INT NOT NULL,
    log_date DATE DEFAULT (CURRENT_DATE),
    notes TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'Pending',
    CONSTRAINT fk_logs_habit FOREIGN KEY (habit_id)
        REFERENCES Habit(habit_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT chk_status CHECK (status IN ('Completed', 'Pending', 'Skipped'))
);

-- ============================================================
-- SAMPLE DATA INSERTION
-- (Kept the sample data for testing the remaining logic)
-- ============================================================

INSERT INTO Customer (user_id, email, name, password, phone_no) VALUES
(101, 'john.doe@email.com', 'John Doe', 'hashed_password_123', '9876543210'),
(102, 'sarah.smith@email.com', 'Sarah Smith', 'hashed_password_456', '9876543211'),
(103, 'mike.johnson@email.com', 'Mike Johnson', 'hashed_password_789', '9876543212'),
(104, 'emma.wilson@email.com', 'Emma Wilson', 'hashed_password_abc', '9876543213'),
(105, 'alex.brown@email.com', 'Alex Brown', 'hashed_password_def', '9876543214');

INSERT INTO Habit (habit_id, user_id, name, start_date, frequency) VALUES
(201, 101, 'Morning Workout', '2024-09-01', 'Daily'),
(202, 101, 'Drink Water', '2024-09-01', 'Daily'),
(203, 102, 'Read Books', '2024-08-15', 'Daily'),
(204, 102, 'Meditation', '2024-08-20', 'Daily'),
(205, 103, 'Code Practice', '2024-09-01', 'Daily'),
(206, 104, 'Language Learning', '2024-08-25', 'Daily'),
(207, 105, 'Dancing', '2024-09-01', 'Daily');

INSERT INTO Goal (goal_id, habit_id, deadline, description) VALUES
(301, 201, '2024-12-31', 'Complete 30-minute workout daily for the entire year'),
(302, 202, '2024-10-31', 'Drink 8 glasses of water daily for 2 months'),
(303, 203, '2024-11-30', 'Read at least 30 minutes daily and complete 5 books'),
(304, 204, '2024-10-15', 'Practice meditation for 15 minutes daily for 6 weeks'),
(305, 205, '2024-12-31', 'Solve coding problems daily to improve programming skills'),
(306, 206, '2024-11-01', 'Complete Spanish basics course through daily practice'),
(307, 207, '2024-10-01', 'Complete learning Salsa at the end of the year');

INSERT INTO Logs (log_id, habit_id, log_date, notes, status) VALUES
(401, 201, '2024-10-01', 'Great cardio session with 20 minutes running', 'Completed'),
(402, 201, '2024-10-02', 'Strength training focused on upper body', 'Completed'),
(403, 201, '2024-10-03', 'Skipped due to illness', 'Skipped'),
(404, 201, '2024-10-04', 'Light yoga session due to tiredness', 'Completed'),
(405, 201, '2024-10-05', 'Full body workout completed successfully', 'Completed'),
(406, 202, '2024-10-01', 'Met daily water goal easily', 'Completed'),
(407, 202, '2024-10-02', 'Drank only 6 glasses, need to improve', 'Pending'),
(408, 202, '2024-10-03', 'Excellent hydration day', 'Completed'),
(409, 203, '2024-10-01', 'Read Atomic Habits chapter on habit stacking', 'Completed'),
(410, 203, '2024-10-02', 'Too busy with work, could not read', 'Skipped'),
(411, 203, '2024-10-03', 'Finished reading productivity articles', 'Completed'),
(412, 205, '2024-10-01', 'Solved 3 algorithm problems on arrays', 'Completed'),
(413, 205, '2024-10-02', 'Practiced data structures - linked lists', 'Completed'),
(414, 205, '2024-10-03', 'Working on dynamic programming concepts', 'Completed'),
(415, 206, '2024-10-01', 'Completed lesson on Spanish verb conjugation', 'Completed'),
(416, 207, '2024-10-01', 'Completed dancing lesson on Salsa', 'Completed');

-- ============================================================
-- STORED PROCEDURE (ONLY ONE)
-- ============================================================

DELIMITER //

-- Stored Procedure 1: MarkGoalAchieved
-- Purpose: Simplest procedure to demonstrate parameter usage and UPDATE statement.
CREATE PROCEDURE MarkGoalAchieved(IN p_goal_id INT)
BEGIN
    -- Update the Goal table to mark the specified goal as achieved.
    UPDATE Goal
    SET is_achieved = TRUE
    WHERE goal_id = p_goal_id;

    SELECT CONCAT('Goal ', p_goal_id, ' marked as achieved!') AS Message;
END;
//
DELIMITER ;

-- ============================================================
-- FUNCTION (ONLY ONE)
-- ============================================================

DELIMITER //

-- Function 1: GetHabitCompletionRate
-- Purpose: Calculates the completion rate (as a percentage) for a single habit.
CREATE FUNCTION GetHabitCompletionRate(p_habit_id INT)
RETURNS DECIMAL(5,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    -- Declare local variables, each with a separate DECLARE statement (best practice for compatibility)
    DECLARE total_logs INT DEFAULT 0;
    DECLARE completed_logs INT DEFAULT 0;
    DECLARE completion_rate DECIMAL(5,2) DEFAULT 0.00;

    -- Get total number of logs for the habit
    SELECT COUNT(*) INTO total_logs FROM Logs WHERE habit_id = p_habit_id;
    
    -- Get number of completed logs for the habit
    SELECT COUNT(*) INTO completed_logs FROM Logs WHERE habit_id = p_habit_id AND status = 'Completed';

    -- Check to prevent division by zero
    IF total_logs = 0 THEN
        RETURN 0.00;
    END IF;

    -- Calculate the completion rate
    SET completion_rate = (completed_logs * 100.0) / total_logs;
    RETURN completion_rate;
END;
//
DELIMITER ;

-- ============================================================
-- TRIGGER (ONLY ONE)
-- ============================================================

DELIMITER //

-- Trigger 1: before_log_insert
-- Purpose: Ensures a log cannot be created for a date before the habit's start date.
CREATE TRIGGER before_log_insert
BEFORE INSERT ON Logs
FOR EACH ROW
BEGIN
    DECLARE habit_start DATE;

    -- Fetch the start date of the habit associated with the new log.
    SELECT start_date INTO habit_start FROM Habit WHERE habit_id = NEW.habit_id;

    -- Check if the new log date is earlier than the habit's start date.
    IF NEW.log_date < habit_start THEN
        -- If it is, signal an error to stop the insert operation.
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Log date cannot be before habit start date';
    END IF;
END;
//
DELIMITER ;

-- ============================================================
-- COMPLEX QUERIES
-- (Kept complex queries as they are standard SQL and not functions/procedures)
-- ============================================================

-- 1. Join query - Get all habits with their goals
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
ORDER BY c.name, h.name;

-- 2. Nested query - Users with above average completion logs
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
ORDER BY completed_logs DESC;

-- 3. Aggregate query - Habit performance summary
SELECT 
    h.name AS habit_name,
    COUNT(l.log_id) AS total_logs,
    SUM(CASE WHEN l.status = 'Completed' THEN 1 ELSE 0 END) AS completed,
    SUM(CASE WHEN l.status = 'Skipped' THEN 1 ELSE 0 END) AS skipped,
    SUM(CASE WHEN l.status = 'Pending' THEN 1 ELSE 0 END) AS pending,
    ROUND(AVG(CASE WHEN l.status = 'Completed' THEN 100 ELSE 0 END), 2) AS avg_completion_rate
FROM Habit h
LEFT JOIN Logs l ON h.habit_id = l.habit_id
GROUP BY h.habit_id, h.name
HAVING COUNT(l.log_id) > 0
ORDER BY avg_completion_rate DESC;

-- 4. Find users who have overdue goals
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
ORDER BY days_overdue DESC;

-- ============================================================
-- FUNCTION & PROCEDURE TESTS (SIMPLIFIED)
-- ============================================================

-- Test the single Stored Procedure
CALL MarkGoalAchieved(301);

-- Test the single Function
SELECT GetHabitCompletionRate(201) AS completion_rate;

-- Test the Trigger (This log date is before habit 201 start date '2024-09-01' and should fail)
-- INSERT INTO Logs (log_id, habit_id, log_date, notes, status) VALUES (999, 201, '2024-08-30', 'Trigger test fail', 'Skipped');
-- Test a successful log insert (will pass the trigger check)
INSERT INTO Logs (log_id, habit_id, log_date, notes, status) VALUES (999, 201, CURRENT_DATE(), 'Trigger test pass', 'Completed');