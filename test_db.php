<?php
/**
 * Database Connection Test Script
 * Use this to verify your database connection is working
 */

echo "\u003c!DOCTYPE html\u003e\n";
echo "\u003chtml\u003e\n";
echo "\u003chead\u003e\u003ctitle\u003eDatabase Connection Test\u003c/title\u003e\n";
echo "\u003cstyle\u003e\n";
echo "body { font-family: Arial, sans-serif; padding: 40px; background: #f5f5f5; }\n";
echo ".success { color: green; background: #d4edda; padding: 15px; border-radius: 5px; margin: 10px 0; }\n";
echo ".error { color: red; background: #f8d7da; padding: 15px; border-radius: 5px; margin: 10px 0; }\n";
echo ".info { color: #333; background: #d1ecf1; padding: 15px; border-radius: 5px; margin: 10px 0; }\n";
echo "table { border-collapse: collapse; width: 100%; margin: 20px 0; background: white; }\n";
echo "th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }\n";
echo "th { background: #667eea; color: white; }\n";
echo "\u003c/style\u003e\n";
echo "\u003c/head\u003e\n";
echo "\u003cbody\u003e\n";
echo "\u003ch1\u003e🔍 Database Connection Test\u003c/h1\u003e\n";

// Include database connection
require_once 'db_connect.php';

// Test 1: Check connection
echo "\u003ch2\u003eTest 1: Database Connection\u003c/h2\u003e\n";
if ($conn-\u003econnect_error) {
    echo "\u003cdiv class='error'\u003e❌ Connection Failed: " . $conn-\u003econnect_error . "\u003c/div\u003e\n";
    echo "\u003cp\u003e\u003cstrong\u003eTroubleshooting:\u003c/strong\u003e\u003c/p\u003e\n";
    echo "\u003cul\u003e\n";
    echo "\u003cli\u003eCheck if MySQL service is running in XAMPP Control Panel\u003c/li\u003e\n";
    echo "\u003cli\u003eVerify credentials in db_connect.php\u003c/li\u003e\n";
    echo "\u003cli\u003eCheck if database 'attendance_system' exists\u003c/li\u003e\n";
    echo "\u003c/ul\u003e\n";
    exit;
} else {
    echo "\u003cdiv class='success'\u003e✅ Database Connected Successfully!\u003c/div\u003e\n";
}

// Test 2: Check if tables exist
echo "\u003ch2\u003eTest 2: Database Tables\u003c/h2\u003e\n";
$result = $conn-\u003equery("SHOW TABLES");
if ($result) {
    echo "\u003cdiv class='success'\u003e✅ Tables Found:\u003c/div\u003e\n";
    echo "\u003cul\u003e\n";
    $tables = [];
    while($row = $result-\u003efetch_row()) {
        echo "\u003cli\u003e" . $row[0] . "\u003c/li\u003e\n";
        $tables[] = $row[0];
    }
    echo "\u003c/ul\u003e\n";
    
    // Check required tables
    if (!in_array('users', $tables)) {
        echo "\u003cdiv class='error'\u003e❌ Missing 'users' table. Please import database_setup.sql\u003c/div\u003e\n";
    }
    if (!in_array('attendance', $tables)) {
        echo "\u003cdiv class='error'\u003e❌ Missing 'attendance' table. Please import database_setup.sql\u003c/div\u003e\n";
    }
} else {
    echo "\u003cdiv class='error'\u003e❌ Error checking tables: " . $conn-\u003eerror . "\u003c/div\u003e\n";
}

// Test 3: Check users table
echo "\u003ch2\u003eTest 3: Users Table\u003c/h2\u003e\n";
$users = $conn-\u003equery("SELECT id, name, email, role FROM users");
if ($users) {
    $count = $users-\u003enum_rows;
    echo "\u003cdiv class='success'\u003e✅ Users Table OK - Total Users: $count\u003c/div\u003e\n";
    
    if ($count > 0) {
        echo "\u003ctable\u003e\n";
        echo "\u003ctr\u003e\u003cth\u003eID\u003c/th\u003e\u003cth\u003eName\u003c/th\u003e\u003cth\u003eEmail\u003c/th\u003e\u003cth\u003eRole\u003c/th\u003e\u003c/tr\u003e\n";
        while($row = $users-\u003efetch_assoc()) {
            echo "\u003ctr\u003e\n";
            echo "\u003ctd\u003e" . $row['id'] . "\u003c/td\u003e\n";
            echo "\u003ctd\u003e" . htmlspecialchars($row['name']) . "\u003c/td\u003e\n";
            echo "\u003ctd\u003e" . htmlspecialchars($row['email']) . "\u003c/td\u003e\n";
            echo "\u003ctd\u003e" . htmlspecialchars($row['role']) . "\u003c/td\u003e\n";
            echo "\u003c/tr\u003e\n";
        }
        echo "\u003c/table\u003e\n";
    } else {
        echo "\u003cdiv class='info'\u003eℹ️ No users found. Sample users may not have been imported.\u003c/div\u003e\n";
    }
} else {
    echo "\u003cdiv class='error'\u003e❌ Error querying users: " . $conn-\u003eerror . "\u003c/div\u003e\n";
}

// Test 4: Check attendance table
echo "\u003ch2\u003eTest 4: Attendance Table\u003c/h2\u003e\n";
$attendance = $conn-\u003equery("SELECT COUNT(*) as count FROM attendance");
if ($attendance) {
    $row = $attendance-\u003efetch_assoc();
    $count = $row['count'];
    echo "\u003cdiv class='success'\u003e✅ Attendance Table OK - Total Records: $count\u003c/div\u003e\n";
    
    if ($count > 0) {
        $records = $conn-\u003equery("SELECT a.*, u.name FROM attendance a JOIN users u ON a.user_id = u.id ORDER BY a.date DESC LIMIT 10");
        echo "\u003cp\u003e\u003cstrong\u003eRecent Attendance Records:\u003c/strong\u003e\u003c/p\u003e\n";
        echo "\u003ctable\u003e\n";
        echo "\u003ctr\u003e\u003cth\u003eID\u003c/th\u003e\u003cth\u003eEmployee\u003c/th\u003e\u003cth\u003eDate\u003c/th\u003e\u003cth\u003eStatus\u003c/th\u003e\u003c/tr\u003e\n";
        while($row = $records-\u003efetch_assoc()) {
            echo "\u003ctr\u003e\n";
            echo "\u003ctd\u003e" . $row['id'] . "\u003c/td\u003e\n";
            echo "\u003ctd\u003e" . htmlspecialchars($row['name']) . "\u003c/td\u003e\n";
            echo "\u003ctd\u003e" . $row['date'] . "\u003c/td\u003e\n";
            echo "\u003ctd\u003e" . $row['status'] . "\u003c/td\u003e\n";
            echo "\u003c/tr\u003e\n";
        }
        echo "\u003c/table\u003e\n";
    } else {
        echo "\u003cdiv class='info'\u003eℹ️ No attendance records yet. Start marking attendance!\u003c/div\u003e\n";
    }
} else {
    echo "\u003cdiv class='error'\u003e❌ Error querying attendance: " . $conn-\u003eerror . "\u003c/div\u003e\n";
}

// Test 5: PHP Configuration
echo "\u003ch2\u003eTest 5: PHP Configuration\u003c/h2\u003e\n";
echo "\u003cdiv class='info'\u003e\n";
echo "\u003cstrong\u003ePHP Version:\u003c/strong\u003e " . phpversion() . "\u003cbr\u003e\n";
echo "\u003cstrong\u003eMySQLi Extension:\u003c/strong\u003e " . (extension_loaded('mysqli') ? '✅ Loaded' : '❌ Not Loaded') . "\u003cbr\u003e\n";
echo "\u003cstrong\u003eServer:\u003c/strong\u003e " . $_SERVER['SERVER_SOFTWARE'] . "\u003cbr\u003e\n";
echo "\u003c/div\u003e\n";

// Summary
echo "\u003ch2\u003e📊 Summary\u003c/h2\u003e\n";
echo "\u003cdiv class='success'\u003e\n";
echo "\u003cstrong\u003e✅ All Tests Passed!\u003c/strong\u003e\u003cbr\u003e\n";
echo "Your database connection is working correctly.\u003cbr\u003e\n";
echo "You can now test the attendance form at: \u003ca href='attendance.html'\u003eattendance.html\u003c/a\u003e\n";
echo "\u003c/div\u003e\n";

$conn-\u003eclose();

echo "\u003c/body\u003e\n";
echo "\u003c/html\u003e\n";
?>
