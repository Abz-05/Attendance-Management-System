# Python Attendance Management System

A comprehensive Python-based attendance management system with MySQL database integration, featuring automated student registration, bulk operations, and detailed reporting.

## 🌟 Features

- **Automated Student Management**: Auto-add new students with validation
- **Bulk Operations**: Import multiple students and mark attendance in bulk
- **Interactive Menu**: User-friendly command-line interface
- **Comprehensive Logging**: Track all operations with detailed logs
- **Error Handling**: Graceful error management throughout
- **Attendance Analytics**: View summaries and statistics
- **Database Integration**: Robust MySQL connectivity with connection pooling

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher** ([Download Python](https://www.python.org/downloads/))
- **MySQL Server 5.7 or higher** (or MariaDB)
- **pip** (Python package installer, included with Python)

### Verify Python Installation

```powershell
python --version
```

Should output: `Python 3.8.x` or higher

### Verify MySQL Installation

```powershell
mysql --version
```

## 🚀 Installation & Setup

### Step 1: Install Python Dependencies

Navigate to the project directory and install required packages:

```powershell
cd "e:\git\Attendance management System"
pip install -r requirements.txt
```

This will install:

- `mysql-connector-python` - MySQL database connector
- `python-dateutil` - Date manipulation utilities

### Step 2: Setup MySQL Database

#### Option A: Using phpMyAdmin (Recommended)

1. Open phpMyAdmin: `http://localhost/phpmyadmin`
2. Click on the **SQL** tab
3. Open `python_database_setup.sql` and copy its contents
4. Paste into the SQL query box
5. Click **Go** to execute

#### Option B: Using MySQL Command Line

```powershell
mysql -u root -p < python_database_setup.sql
```

This creates:

- `attendance_system` database
- `students` table (id, name, email, join_date, created_at)
- `attendance` table (id, student_id, date, status, created_at)

### Step 3: Configure Database Connection

Edit `config.ini` and update database credentials if needed:

```ini
[database]
host = localhost
user = root
password =           # Add your MySQL password here
database = attendance_system
port = 3306
```

**Important**: If your MySQL has a password, add it to the `password` field!

### Step 4: Verify Setup

Test the database connection:

```powershell
python main.py
```

You should see:

```
Testing database connection...
✓ Database connection successful!
```

## 📖 Usage Guide

### Running the Application

```powershell
python main.py
```

### Main Menu Options

```
MAIN MENU
------------------------------------------------------------
1. Add New Student
2. Add Multiple Students
3. View All Students
4. Mark Daily Attendance
5. Mark Bulk Attendance
6. View Today's Attendance
7. View Attendance by Date
8. View Student Attendance History
9. View Student Attendance Summary
0. Exit
------------------------------------------------------------
```

### Common Workflows

#### 1. Adding a New Student

```
Menu → Option 1
Enter student name: John Doe
Enter student email: john.doe@example.com
Use custom join date? (y/n): n
```

- Auto-assigns today's date as join date
- Validates email format
- Prevents duplicate emails

#### 2. Bulk Import Students from CSV

First, prepare a CSV file like `sample_students.csv`:

```csv
name,email
Student Name,student@example.com
Another Student,another@example.com
```

Then use Option 2 to add multiple students manually, or modify the code to import from CSV.

#### 3. Marking Daily Attendance

```
Menu → Option 4
Enter student ID: 1
Use custom date? (y/n): n
Select status (1-3): 1
```

Status options:

- 1 = Present
- 2 = Absent
- 3 = Leave

#### 4. Bulk Attendance for All Students

```
Menu → Option 5
```

System will show all students and prompt for each student's status.

#### 5. Viewing Attendance Summary

```
Menu → Option 9
Enter student ID: 1
```

Displays:

- Total attendance days
- Present/Absent/Leave counts
- Attendance percentage

## 🗂️ Project Structure

```
e:\git\Attendance management System\
│
├── main.py                      # Main application entry point
├── student_manager.py           # Student management module
├── attendance_manager.py        # Attendance management module
├── db_config.py                 # Database configuration
├── logger_config.py             # Logging configuration
│
├── config.ini                   # Configuration file
├── requirements.txt             # Python dependencies
│
├── python_database_setup.sql    # Database setup script
├── sample_students.csv          # Sample data for testing
│
├── attendance_system.log        # Application log file (auto-created)
│
└── PYTHON_README.md            # This file
```

## 🗄️ Database Schema

### Students Table

| Column     | Type         | Description               |
| ---------- | ------------ | ------------------------- |
| id         | INT (PK, AI) | Auto-increment student ID |
| name       | VARCHAR(100) | Student name              |
| email      | VARCHAR(100) | Unique email address      |
| join_date  | DATE         | Date student joined       |
| created_at | TIMESTAMP    | Record creation timestamp |

### Attendance Table

| Column     | Type         | Description                  |
| ---------- | ------------ | ---------------------------- |
| id         | INT (PK, AI) | Auto-increment attendance ID |
| student_id | INT (FK)     | Foreign key to students.id   |
| date       | DATE         | Attendance date              |
| status     | ENUM(P/A/L)  | Present/Absent/Leave         |
| created_at | TIMESTAMP    | Record creation timestamp    |

**Constraints**:

- Unique constraint on (student_id, date) - prevents duplicate attendance
- Foreign key with CASCADE delete
- Indexed columns for performance

## 🔧 Configuration Options

### config.ini Sections

#### [database]

- `host`: MySQL server host (default: localhost)
- `user`: MySQL username (default: root)
- `password`: MySQL password (update this!)
- `database`: Database name (attendance_system)
- `port`: MySQL port (default: 3306)

#### [logging]

- `level`: Log level (DEBUG, INFO, WARNING, ERROR)
- `file`: Log file path (attendance_system.log)
- `format`: Log message format

#### [application]

- `timezone`: Application timezone (Asia/Kolkata)
- `date_format`: Date format for display (%Y-%m-%d)

## 📝 Module Documentation

### student_manager.py

**Key Functions**:

- `add_student(name, email, join_date)` - Add single student
- `add_students_bulk(students_list)` - Add multiple students
- `get_all_students()` - Retrieve all students
- `get_student_by_id(student_id)` - Get specific student
- `get_student_by_email(email)` - Find by email

**Features**:

- Email validation (regex pattern)
- Duplicate prevention
- Auto-join date assignment
- Comprehensive error handling

### attendance_manager.py

**Key Functions**:

- `mark_attendance(student_id, date, status)` - Mark single attendance
- `mark_bulk_attendance(attendance_list)` - Bulk marking
- `get_attendance_by_date(date)` - View by date
- `get_student_attendance(student_id, start, end)` - Student history
- `get_attendance_summary(student_id)` - Statistics

**Features**:

- Status validation (Present/Absent/Leave)
- Duplicate prevention (same student, same date)
- Date parsing and validation
- Attendance percentage calculation

### db_config.py

**Features**:

- Connection pooling (5 connections)
- Auto-reconnection
- Configuration from config.ini
- Connection health check

### logger_config.py

**Features**:

- File and console logging
- Configurable log levels
- Formatted timestamps
- UTF-8 encoding support

## 🔍 Troubleshooting

### Common Issues

#### 1. ModuleNotFoundError: No module named 'mysql'

**Solution**:

```powershell
pip install mysql-connector-python
```

#### 2. Database connection failed

**Solutions**:

- Verify MySQL service is running
- Check credentials in `config.ini`
- Ensure database exists: `CREATE DATABASE attendance_system`
- Test connection: `mysql -u root -p`

#### 3. Access denied for user 'root'@'localhost'

**Solution**:
Update password in `config.ini`:

```ini
[database]
password = your_mysql_password
```

#### 4. Table doesn't exist

**Solution**:
Re-run database setup script:

```powershell
mysql -u root -p < python_database_setup.sql
```

#### 5. ImportError on imports

**Solution**:
Ensure you're in the project directory:

```powershell
cd "e:\git\Attendance management System"
python main.py
```

### Viewing Logs

Check `attendance_system.log` file for detailed error information:

```powershell
type attendance_system.log
```

## 🧪 Testing

### Test Database Connection

```powershell
python -c "from db_config import DatabaseConfig; print(DatabaseConfig.test_connection())"
```

### Test Student Addition

```python
from student_manager import StudentManager
success, msg, sid = StudentManager.add_student("Test Student", "test@example.com")
print(msg)
```

### Test Attendance Marking

```python
from attendance_manager import AttendanceManager
success, msg = AttendanceManager.mark_attendance(1, None, 'Present')
print(msg)
```

## 🚀 Advanced Features

### Import Students from CSV

Add this function to `main.py`:

```python
import csv

def import_students_from_csv():
    filename = input("Enter CSV filename: ")
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        students = [(row['name'], row['email']) for row in reader]
    return StudentManager.add_students_bulk(students)
```

### Export Attendance to CSV

```python
import csv
from datetime import date

records = AttendanceManager.get_attendance_by_date(date.today())
with open('attendance_export.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['student_id', 'name', 'status'])
    writer.writeheader()
    writer.writerows(records)
```

## 📊 Sample Workflows

### Workflow 1: Daily Attendance Setup

1. Start application: `python main.py`
2. View all students (Option 3)
3. Mark bulk attendance (Option 5)
4. View today's attendance (Option 6)

### Workflow 2: New Student Onboarding

1. Add new student (Option 1)
2. Mark their first attendance (Option 4)
3. View student summary (Option 9)

### Workflow 3: Monthly Report

1. View student attendance history (Option 8)
2. Check attendance summary (Option 9)
3. Export data (custom function)

## 🔐 Security Best Practices

1. **Never commit config.ini with passwords** to version control
2. **Use environment variables** for sensitive data
3. **Implement user authentication** for production use
4. **Sanitize all user inputs** (already implemented)
5. **Use HTTPS** for any web deployment

## 📈 Future Enhancements

- Web interface (Flask/Django)
- User authentication and roles
- Email notifications for absences
- QR code-based attendance
- Mobile app integration
- Advanced analytics and charts
- PDF report generation
- Scheduled automatic backups

## 🤝 Contributing

Feel free to enhance this project! Some ideas:

- Add GUI using Tkinter
- Implement REST API
- Add unit tests
- Create Docker containerization

## 📄 License

This project is open-source and available for educational purposes.

## 💡 Tips

- **Run from E: drive**: All paths are relative, no need to move to C:
- **Check logs**: Always review `attendance_system.log` for issues
- **Backup database**: Regularly export your database
- **Test first**: Use sample data before production

## 🆘 Support

For issues or questions:

1. Check this README
2. Review error logs in `attendance_system.log`
3. Verify database connection with `main.py`
4. Ensure all dependencies are installed

---

**Happy Coding! 🎓📊**

---

## Quick Start Checklist

- [ ] Python 3.8+ installed
- [ ] MySQL server running
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Database created (`python_database_setup.sql` executed)
- [ ] `config.ini` configured with correct credentials
- [ ] Run `python main.py` to start
- [ ] Test connection successful
- [ ] Ready to use!
