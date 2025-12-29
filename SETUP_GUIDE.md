# 🎓 Attendance Management System - Complete Setup Guide

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Database Setup](#database-setup)
3. [Python Environment Setup](#python-environment-setup)
4. [Running the Application](#running-the-application)
5. [Features Overview](#features-overview)
6. [Troubleshooting](#troubleshooting)

---

## 🔧 System Requirements

- **XAMPP** (Apache + MySQL) - Already installed at `C:\Xammp`
- **Python 3.8+** - For backend API
- **Modern Web Browser** - Chrome, Firefox, or Edge
- **Internet Connection** - For loading external fonts and Chart.js library

---

## 💾 Database Setup

### Step 1: Start XAMPP Services

1. Open XAMPP Control Panel
2. Start **Apache** service
3. Start **MySQL** service

### Step 2: Create Database

1. Open your browser and go to: `http://localhost/phpmyadmin`
2. Click on "SQL" tab
3. Copy the entire content from `attendance_system_setup.sql`
4. Paste it into the SQL query box
5. Click "Go" to execute

**Or use MySQL command line:**

```bash
cd "C:\Xammp\htdocs\Attendance management System"
mysql -u root -p < attendance_system_setup.sql
```

### Step 3: Verify Database

After running the SQL script, you should see:

- ✅ Database: `attendance_system`
- ✅ Tables: `students` (23 records), `faculty` (5 records), `attendance`
- ✅ Views: `attendance_summary`

---

## 🐍 Python Environment Setup

### Step 1: Install Python Dependencies

Open PowerShell in the project directory and run:

```powershell
# Navigate to project directory
cd "C:\Xammp\htdocs\Attendance management System"

# Install required packages
pip install flask flask-cors mysql-connector-python python-dotenv
```

**Or use the requirements.txt:**

```powershell
pip install -r requirements.txt
```

### Step 2: Test Database Connection

```powershell
python db_config_new.py
```

You should see: `✅ Connected to database: attendance_system`

---

## 🚀 Running the Application

### Step 1: Start the Backend API Server

Open PowerShell and run:

```powershell
cd "C:\Xammp\htdocs\Attendance management System"
python api_server.py
```

You should see:

```
🚀 Starting Attendance Management System API...
📍 API will be available at: http://localhost:5000
 * Running on http://0.0.0.0:5000
```

**Keep this terminal window open!**

### Step 2: Access the Application

Open your browser and navigate to:

**Main Dashboard:**

```
file:///C:/Xammp/htdocs/Attendance%20management%20System/index.html
```

**Or use XAMPP (if Apache is running on port 80):**

```
http://localhost/Attendance%20management%20System/index.html
```

---

## ✨ Features Overview

### 1. 📝 Mark Attendance (`mark_attendance.html`)

**Features:**

- Select faculty and subject from dropdown
- Choose period (1-5) and date
- Mark attendance for all 23 students
- Options: Present, Absent, Late
- Quick actions: Mark All Present, Mark All Absent, Clear All
- Real-time validation and feedback

**How to Use:**

1. Select Faculty (e.g., "Ratchana B")
2. Subject auto-fills based on faculty
3. Select Period (1-5)
4. Select Date (defaults to today)
5. Click status buttons for each student
6. Click "Submit Attendance"

### 2. 📊 Analytics Dashboard (`analytics.html`)

**Features:**

- Overall attendance statistics
- Interactive charts (Bar, Line, Pie)
- Detailed student-wise report
- Attendance percentage calculation
- Auto-refresh every 30 seconds

**Chart Types:**

- **Bar Chart**: Compare Present/Absent/Late across students
- **Line Chart**: Trend visualization
- **Pie Chart**: Overall distribution

### 3. 📅 Daily Reports (`daily_report.html`)

**Features:**

- Period-wise attendance view
- Date filtering
- Summary statistics
- Subject and faculty information per period
- Color-coded status badges

**How to Use:**

1. Select a date
2. Click "Load Report"
3. View period-wise attendance for all students

---

## 🎯 System Configuration

### Period Timings

| Period    | Time          | Duration |
| --------- | ------------- | -------- |
| Period 1  | 09:00 - 09:50 | 50 mins  |
| Period 2  | 09:50 - 10:40 | 50 mins  |
| **Break** | 10:40 - 11:00 | 20 mins  |
| Period 3  | 11:00 - 11:50 | 50 mins  |
| Period 4  | 11:50 - 12:40 | 50 mins  |
| **Lunch** | 12:40 - 13:30 | 50 mins  |
| Period 5  | 13:30 - 15:10 | 100 mins |

### Subjects & Faculty

| Subject                       | Faculty     |
| ----------------------------- | ----------- |
| Machine Learning              | Ratchana B  |
| Big Data Analytics            | S. Karthiga |
| Computer Networks             | DSP         |
| Statistical Data Analysis     | Maniram     |
| Statistical Data Analysis Lab | Maniram     |

### Students

- **Total Students**: 23
- **Registration Numbers**: C3S48851 to C3S48874
- All student data is pre-loaded in the database

---

## 🔍 Troubleshooting

### Issue: "Failed to fetch students"

**Solution:**

1. Check if API server is running on port 5000
2. Restart the API server: `python api_server.py`
3. Check browser console for CORS errors

### Issue: "Database connection error"

**Solution:**

1. Verify MySQL is running in XAMPP
2. Check database credentials in `db_config_new.py`
3. Ensure database `attendance_system` exists
4. Test connection: `python db_config_new.py`

### Issue: "Port 5000 already in use"

**Solution:**

1. Find and kill the process using port 5000:

```powershell
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

2. Or change the port in `api_server.py` (last line)

### Issue: Charts not displaying

**Solution:**

1. Check internet connection (Chart.js loads from CDN)
2. Check browser console for JavaScript errors
3. Ensure API is returning data correctly

### Issue: "Module not found" errors

**Solution:**

```powershell
pip install --upgrade flask flask-cors mysql-connector-python
```

---

## 📱 Browser Compatibility

✅ **Tested and Working:**

- Google Chrome (Recommended)
- Microsoft Edge
- Mozilla Firefox
- Safari

---

## 🔐 Security Notes

**For Production Deployment:**

1. Change MySQL root password
2. Update `db_config_new.py` with secure credentials
3. Use environment variables for sensitive data
4. Enable HTTPS
5. Add authentication/authorization
6. Implement rate limiting on API endpoints

---

## 📊 Database Schema

### Students Table

```sql
- id (Primary Key)
- reg_no (Unique)
- name
- email (Unique)
- phone
- board
- marks
- cgpa
- join_date
- created_at
```

### Faculty Table

```sql
- id (Primary Key)
- name
- subject
- created_at
```

### Attendance Table

```sql
- id (Primary Key)
- student_id (Foreign Key → students.id)
- faculty_id (Foreign Key → faculty.id)
- subject
- date
- period (1-5)
- status (Present/Absent/Late)
- created_at
```

---

## 🎨 Design Features

- **Modern UI**: Gradient backgrounds, glassmorphism effects
- **Responsive**: Works on desktop, tablet, and mobile
- **Interactive**: Hover effects, smooth animations
- **Accessible**: Clear labels, high contrast, keyboard navigation
- **Professional**: Clean typography, consistent spacing

---

## 📞 Support

For issues or questions:

1. Check the logs: `attendance_system.log` and `attendance_api.log`
2. Review browser console for errors
3. Verify all services are running

---

## 🚀 Quick Start Checklist

- [ ] XAMPP Apache is running
- [ ] XAMPP MySQL is running
- [ ] Database `attendance_system` is created and populated
- [ ] Python dependencies are installed
- [ ] API server is running on port 5000
- [ ] Browser is open to `index.html`
- [ ] All features are accessible

---

**System Version**: 1.0.0  
**Last Updated**: December 29, 2025  
**Developed for**: Student Attendance Management with Analytics

---

## 🎓 Student Data Summary

All 23 students from your class are pre-loaded:

- Abzana V (C3S48851)
- Aishwarya Suruthi A (C3S48852)
- Harini J (C3S48853)
- ... and 20 more students

Complete with registration numbers, emails, phone numbers, board information, marks, and CGPA.

---

**Enjoy using the Attendance Management System! 🎉**
