# Attendance Management System

A simple web-based attendance management system built with HTML, PHP, and MySQL. This system allows users to submit attendance records through a user-friendly web interface.

## 📋 Features

- **User-friendly Interface**: Clean, modern HTML form with responsive design
- **Secure Backend**: PHP with prepared statements to prevent SQL injection
- **Data Validation**: Both client-side and server-side validation
- **Real-time Feedback**: AJAX-based form submission with instant feedback
- **Database Management**: MySQL database with proper relationships and constraints
- **Sample Data**: Pre-populated with test users for immediate testing

## 🗂️ Project Structure

```
Attendance management System/
├── attendance.html          # Frontend form for attendance submission
├── attendance_form.php      # Backend handler for form processing
├── db_connect.php          # Database connection configuration
├── database_setup.sql      # Database and tables creation script
└── README.md              # This file
```

## 🚀 Installation Instructions

### Prerequisites

- Web server (Apache/Nginx) with PHP support
- MySQL/MariaDB database server
- phpMyAdmin (recommended) or MySQL command-line client
- PHP 7.0 or higher
- Web browser

### Step 1: Setup Database

1. Open **phpMyAdmin** in your web browser (usually at `http://localhost/phpmyadmin`)
2. Click on the **"SQL"** tab at the top
3. Open the `database_setup.sql` file in a text editor
4. Copy the entire contents of the file
5. Paste it into the SQL query box in phpMyAdmin
6. Click **"Go"** to execute the script

Alternatively, using MySQL command line:

```bash
mysql -u root -p < database_setup.sql
```

The script will:

- Create the `attendance_system` database
- Create `users` and `attendance` tables
- Insert 3 sample users (IDs: 1, 2, 3)
- Set up foreign key relationships

### Step 2: Configure Database Connection

1. Open `db_connect.php` in a text editor
2. Update the database credentials if needed:
   ```php
   define('DB_HOST', 'localhost');     // Your MySQL host
   define('DB_USER', 'root');           // Your MySQL username
   define('DB_PASS', '');               // Your MySQL password
   define('DB_NAME', 'attendance_system');
   ```
3. Save the file

### Step 3: Deploy Files

1. Copy all project files to your web server's document root:
   - **XAMPP**: `C:\xampp\htdocs\attendance\`
   - **WAMP**: `C:\wamp\www\attendance\`
   - **Custom**: Your web server's configured document root

### Step 4: Start Web Server

1. Start your web server (Apache) and MySQL service
   - **XAMPP**: Open XAMPP Control Panel, start Apache and MySQL
   - **WAMP**: Start WAMP Server
2. Ensure both services are running (green status)

### Step 5: Access the Application

1. Open your web browser
2. Navigate to: `http://localhost/attendance/attendance.html`
3. The attendance form should load successfully

## 📖 Usage Guide

### Submitting Attendance

1. **Employee ID**: Enter a valid employee ID (Sample IDs: 1, 2, or 3)
2. **Date**: Select the date (defaults to today)
3. **Status**: Choose from Present, Absent, or Leave
4. Click **"Submit Attendance"**

### Success Response

- Green message confirming attendance was recorded
- Form resets automatically
- Employee name is displayed in the confirmation

### Error Handling

- Red message for validation errors
- Duplicate attendance prevention
- Invalid employee ID detection

## 🗄️ Database Schema

### Users Table

```sql
id          INT (Primary Key, Auto Increment)
name        VARCHAR(100)
email       VARCHAR(100) UNIQUE
password    VARCHAR(255)
role        VARCHAR(50)
created_at  TIMESTAMP
```

### Attendance Table

```sql
id          INT (Primary Key, Auto Increment)
user_id     INT (Foreign Key → users.id)
date        DATE
status      ENUM('Present', 'Absent', 'Leave')
created_at  TIMESTAMP
```

### Sample Users (Pre-populated)

| ID  | Name       | Email                  | Role     |
| --- | ---------- | ---------------------- | -------- |
| 1   | John Doe   | john.doe@example.com   | employee |
| 2   | Jane Smith | jane.smith@example.com | employee |
| 3   | Admin User | admin@example.com      | admin    |

**Note**: Sample password for all users is `password` (hashed in database)

## 🔧 Troubleshooting

### Database Connection Failed

- **Problem**: Error message about database connection
- **Solution**:
  - Verify MySQL service is running
  - Check credentials in `db_connect.php`
  - Ensure `attendance_system` database exists

### Employee ID Not Found

- **Problem**: "Employee ID not found in the system"
- **Solution**: Use sample IDs (1, 2, or 3) or add new users via phpMyAdmin

### Attendance Already Exists

- **Problem**: "Attendance for this employee on this date already exists"
- **Solution**: Each employee can only have one attendance record per date. Change the date or employee ID.

### Form Not Submitting

- **Problem**: Nothing happens when clicking submit
- **Solution**:
  - Check browser console for JavaScript errors (F12)
  - Ensure `attendance_form.php` is in the same directory
  - Verify web server is running

### Blank Page or 404 Error

- **Problem**: Page not loading
- **Solution**:
  - Verify files are in the correct web server directory
  - Check file permissions
  - Ensure URL is correct (e.g., `http://localhost/attendance/attendance.html`)

## 🔐 Security Features

- **Prepared Statements**: Protection against SQL injection
- **Input Validation**: Both client and server-side validation
- **Data Sanitization**: All user inputs are sanitized
- **Password Hashing**: User passwords are hashed with bcrypt
- **Unique Constraints**: Prevents duplicate attendance entries

## 🎨 Features & Enhancements

### Current Features

- Modern gradient design with glassmorphism effect
- Responsive layout for mobile and desktop
- Smooth animations and transitions
- Real-time form validation
- AJAX submission without page reload
- Automatic form reset on success
- Auto-hiding success/error messages

### Potential Enhancements

- User authentication and login system
- Attendance history view
- Admin dashboard for managing users
- Export attendance reports (CSV/PDF)
- Email notifications
- Bulk attendance upload
- Calendar view for attendance
- Leave request management

## 📝 API Response Format

### Success Response

```json
{
  "success": true,
  "message": "Attendance recorded successfully for John Doe!",
  "data": {
    "employee_name": "John Doe",
    "employee_id": 1,
    "date": "2025-12-29",
    "status": "Present"
  }
}
```

### Error Response

```json
{
  "success": false,
  "message": "Employee ID not found in the system."
}
```

## 🤝 Contributing

Feel free to fork this project and submit pull requests for any improvements.

## 📄 License

This project is open source and available for educational purposes.

## 👨‍💻 Support

For issues or questions, please check the troubleshooting section or review the code comments for additional guidance.

---

**Happy Coding! 🚀**
