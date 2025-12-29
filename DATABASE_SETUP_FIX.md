# 🔧 Quick Fix: Database Setup for Python System

## ❌ Current Error

```
ERROR: Unknown database 'attendance_system'
```

**Cause**: The database for the Python system hasn't been created yet.

---

## ✅ Solution: Import Database

You need to run the **python_database_setup.sql** file to create the database.

### Method 1: Using phpMyAdmin (Easiest)

1. **Open phpMyAdmin**: http://localhost/phpmyadmin

2. **Click "SQL" tab** at the top

3. **Open the SQL file**:

   - File location: `e:\git\Attendance management System\python_database_setup.sql`
   - Open it in Notepad

4. **Copy ALL the SQL** from the file

5. **Paste** into the SQL query box in phpMyAdmin

6. **Click "Go"** to execute

7. **Verify**: You should see "attendance_system" database in the left sidebar

---

### Method 2: Using MySQL Command Line

```powershell
# Navigate to MySQL bin directory
cd "C:\xampp\mysql\bin"

# Login to MySQL
.\mysql.exe -u root -p

# Run in MySQL prompt:
SOURCE e:\git\Attendance management System\python_database_setup.sql;

# Or paste the SQL content directly
```

---

### Method 3: Quick Command (PowerShell)

```powershell
# From your project directory:
cd "e:\git\Attendance management System"

# Import via MySQL command line (if no password):
& "C:\xampp\mysql\bin\mysql.exe" -u root -e "CREATE DATABASE IF NOT EXISTS attendance_system;"

# Then you can run the SQL file
Get-Content "python_database_setup.sql" | & "C:\xampp\mysql\bin\mysql.exe" -u root
```

---

## 📋 What the SQL Creates

The `python_database_setup.sql` file will create:

1. **Database**: `attendance_system`
2. **Tables**:
   - `students` (id, name, email, join_date, created_at)
   - `attendance` (id, student_id, date, status, created_at)
3. **Indexes** for better performance
4. **Foreign keys** for data integrity

---

## ✅ After Database Setup

Once you import the SQL, run the Python app again:

```powershell
python main.py
```

**You should see**:

```
============================================================
               ATTENDANCE MANAGEMENT SYSTEM
============================================================

Testing database connection...
✓ Database connection successful!

------------------------------------------------------------
MAIN MENU
------------------------------------------------------------
1. Add New Student
2. Add Multiple Students
...
```

---

## 🔍 Verify Database Creation

### Check in phpMyAdmin:

1. Open http://localhost/phpmyadmin
2. Look for `attendance_system` in left sidebar
3. Click on it
4. Should see `students` and `attendance` tables

### Check via MySQL:

```sql
SHOW DATABASES;
USE attendance_system;
SHOW TABLES;
```

---

## 🚀 Quick Start Commands

**After database is created**:

```powershell
# Activate virtual environment (if not already)
.\.venv\Scripts\Activate.ps1

# Run the Python application
python main.py

# Test: Add a student
# Menu → Option 1
# Name: Test Student
# Email: test@example.com
```

---

## 📞 Error Reference

| Error                                | Cause                   | Solution                                |
| ------------------------------------ | ----------------------- | --------------------------------------- |
| Unknown database 'attendance_system' | Database not created    | Import python_database_setup.sql        |
| Access denied                        | Wrong MySQL credentials | Update config.ini with correct password |
| Table doesn't exist                  | Tables not created      | Re-import python_database_setup.sql     |
| Connection refused                   | MySQL not running       | Start MySQL in XAMPP Control Panel      |

---

**Current Status**: ⏳ Database needs to be created  
**Next Step**: Import python_database_setup.sql via phpMyAdmin  
**Then**: Run `python main.py` again
