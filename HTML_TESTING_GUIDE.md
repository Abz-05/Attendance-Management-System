# Testing Guide - HTML Attendance System

## ⚠️ Important Prerequisites

The HTML attendance system requires a **web server with PHP and MySQL** to function properly. You cannot simply open the HTML file directly in a browser (file:// protocol) because:

1. The form submits to `attendance_form.php` which requires PHP processing
2. PHP needs to connect to MySQL database
3. AJAX requests from file:// protocol are restricted

## 🚀 Setup Instructions

### Option 1: Using XAMPP (Recommended)

1. **Install XAMPP** (if not already installed)

   - Download from: https://www.apachefriends.org/
   - Install to default location (C:\xampp)

2. **Copy Files to htdocs**

   ```powershell
   # Copy all PHP and HTML files
   Copy-Item "e:\git\Attendance management System\attendance.html" "C:\xampp\htdocs\attendance\"
   Copy-Item "e:\git\Attendance management System\attendance_form.php" "C:\xampp\htdocs\attendance\"
   Copy-Item "e:\git\Attendance management System\db_connect.php" "C:\xampp\htdocs\attendance\"
   ```

3. **Start XAMPP Services**

   - Open XAMPP Control Panel
   - Click "Start" for Apache
   - Click "Start" for MySQL
   - Both should show green "Running" status

4. **Setup Database**

   - Open phpMyAdmin: `http://localhost/phpmyadmin`
   - Import `database_setup.sql` (from the SQL tab)
   - Verify `attendance_system` database exists
   - Check that `users` and `attendance` tables are created

5. **Access the Application**
   - Open browser and navigate to: `http://localhost/attendance/attendance.html`

---

### Option 2: Using WAMP

1. **Install WAMP** (if not already installed)
2. **Copy files** to `C:\wamp\www\attendance\`
3. **Start WAMP services**
4. **Setup database** via phpMyAdmin
5. **Access**: `http://localhost/attendance/attendance.html`

---

### Option 3: Using VS Code Live Server + PHP (Advanced)

This won't work because Live Server doesn't process PHP files. You MUST use a PHP-enabled server like XAMPP or WAMP.

---

## 🧪 Testing Procedure

### Step 1: Verify Server is Running

Open browser and check:

- `http://localhost/` - Should show XAMPP/WAMP welcome page
- `http://localhost/phpmyadmin` - Should open phpMyAdmin

### Step 2: Test Database Connection

Create a test file `C:\xampp\htdocs\attendance\test_db.php`:

```php
<?php
require_once 'db_connect.php';

if ($conn->connect_error) {
    echo "❌ Connection failed: " . $conn->connect_error;
} else {
    echo "✅ Database connected successfully!<br>";

    // Check if tables exist
    $result = $conn->query("SHOW TABLES");
    echo "<br>Tables in database:<br>";
    while($row = $result->fetch_row()) {
        echo "- " . $row[0] . "<br>";
    }

    // Check users
    $users = $conn->query("SELECT COUNT(*) as count FROM users");
    $count = $users->fetch_assoc();
    echo "<br>Total users: " . $count['count'];
}
$conn->close();
?>
```

Access: `http://localhost/attendance/test_db.php`

**Expected Output**:

```
✅ Database connected successfully!

Tables in database:
- users
- attendance

Total users: 3
```

### Step 3: Open the Attendance Form

Navigate to: `http://localhost/attendance/attendance.html`

**You should see**:

- Beautiful gradient purple background
- White rounded card with form
- "📋 Attendance System" heading
- Three form fields:
  - Employee ID (number input)
  - Date (date picker, pre-filled with today)
  - Status (dropdown with Present/Absent/Leave)
- "Submit Attendance" button

### Step 4: Test Valid Submission

1. **Enter Employee ID**: `1` (from sample data)
2. **Date**: Keep today's date
3. **Status**: Select "Present"
4. **Click** "Submit Attendance"

**Expected Result**:

- Button text changes to "Submitting..."
- Green success message appears: "Attendance recorded successfully for John Doe!"
- Form resets
- Date remains today

### Step 5: Test Duplicate Prevention

1. Submit the same data again (ID: 1, same date, any status)

**Expected Result**:

- Red error message: "Attendance for this employee on this date already exists."

### Step 6: Test Invalid Employee ID

1. **Enter Employee ID**: `999`
2. **Select date and status**
3. **Submit**

**Expected Result**:

- Red error message: "Employee ID not found in the system."

### Step 7: Test Validation

1. Leave Employee ID empty and try to submit

**Expected Result**:

- Browser validation prevents submission
- Field highlights with "Please fill out this field"

### Step 8: Verify in Database

1. Open phpMyAdmin: `http://localhost/phpmyadmin`
2. Select `attendance_system` database
3. Click on `attendance` table
4. Click "Browse"

**Expected Result**:

- See your attendance records
- Shows: id, user_id, date, status, created_at

---

## 🐛 Common Issues & Solutions

### Issue 1: "Page not found" or "File not found"

**Cause**: Files not in correct directory or server not running

**Solutions**:

- Verify XAMPP/WAMP is running (Apache and MySQL green)
- Ensure files are in `C:\xampp\htdocs\attendance\`
- Check URL is `http://localhost/attendance/attendance.html` (NOT file:///)

### Issue 2: Form submits but nothing happens

**Cause**: JavaScript error or AJAX request failing

**Solutions**:

1. Open browser DevTools (F12)
2. Go to Console tab
3. Look for errors
4. Go to Network tab
5. Submit form and check if `attendance_form.php` request appears
6. Check request status code (should be 200)

### Issue 3: "Database connection failed"

**Cause**: MySQL not running or wrong credentials

**Solutions**:

- Start MySQL in XAMPP Control Panel
- Check `db_connect.php` credentials match your MySQL setup
- Default XAMPP: user='root', password='' (empty)
- Test connection with `test_db.php`

### Issue 4: "Table doesn't exist"

**Cause**: Database not set up

**Solutions**:

- Import `database_setup.sql` in phpMyAdmin
- Verify database name is `attendance_system`
- Check tables exist: `users` and `attendance`

### Issue 5: CORS or fetch errors

**Cause**: Trying to access from file:// instead of http://

**Solutions**:

- MUST use `http://localhost/attendance/attendance.html`
- CANNOT use file:// URL
- Requires web server (XAMPP/WAMP)

---

## ✅ Success Checklist

Before reporting issues, verify:

- [ ] XAMPP/WAMP is installed
- [ ] Apache service is running (green in control panel)
- [ ] MySQL service is running (green in control panel)
- [ ] Files are in `C:\xampp\htdocs\attendance\` (not E: drive)
- [ ] Database `attendance_system` exists
- [ ] Tables `users` and `attendance` exist
- [ ] Sample users are in database (IDs 1, 2, 3)
- [ ] Accessing via `http://localhost/attendance/attendance.html`
- [ ] Browser DevTools shows no JavaScript errors
- [ ] `test_db.php` shows successful connection

---

## 📸 What You Should See

### 1. XAMPP Control Panel

```
Apache: [Running] Port 80
MySQL:  [Running] Port 3306
```

### 2. Attendance Form (http://localhost/attendance/attendance.html)

```
┌─────────────────────────────────────────┐
│                                         │
│     📋 Attendance System                │
│     Record your daily attendance        │
│                                         │
│  Employee ID *                          │
│  [1                                  ]  │
│  Sample IDs: 1, 2, or 3                │
│                                         │
│  Date *                                 │
│  [2025-12-29                         ]  │
│                                         │
│  Attendance Status *                    │
│  [Present                          ▼]   │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │   Submit Attendance               │  │
│  └───────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

### 3. Success Message

```
┌─────────────────────────────────────────┐
│ ✓ Attendance recorded successfully for  │
│   John Doe!                              │
└─────────────────────────────────────────┘
```

### 4. Database (phpMyAdmin)

```
attendance table:
id | user_id | date       | status  | created_at
---+---------+------------+---------+--------------------
1  | 1       | 2025-12-29 | Present | 2025-12-29 14:50:00
```

---

## 🎯 Quick Test Command

If you want to quickly copy files to XAMPP, run this PowerShell command:

```powershell
# Create directory
New-Item -ItemType Directory -Force -Path "C:\xampp\htdocs\attendance"

# Copy files
Copy-Item "e:\git\Attendance management System\attendance.html" "C:\xampp\htdocs\attendance\"
Copy-Item "e:\git\Attendance management System\attendance_form.php" "C:\xampp\htdocs\attendance\"
Copy-Item "e:\git\Attendance management System\db_connect.php" "C:\xampp\htdocs\attendance\"

Write-Host "✅ Files copied successfully!"
Write-Host "Now open: http://localhost/attendance/attendance.html"
```

---

## 📞 Support

If you encounter issues:

1. Check browser console (F12 → Console tab)
2. Check network requests (F12 → Network tab)
3. Verify database connection with `test_db.php`
4. Check XAMPP error logs in `C:\xampp\apache\logs\error.log`
5. Ensure database is set up correctly in phpMyAdmin

---

**Remember**: You CANNOT test the PHP backend by simply opening the HTML file. You MUST use a web server like XAMPP or WAMP!
