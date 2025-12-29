<?php
/**
 * Database Connection File
 * This file establishes a connection to the MySQL database
 */

// Database configuration
define('DB_HOST', 'localhost');
define('DB_USER', 'root');           // Change this to your MySQL username
define('DB_PASS', '');                // Change this to your MySQL password
define('DB_NAME', 'attendance_system');

// Create connection
$conn = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME);

// Check connection
if ($conn->connect_error) {
    die(json_encode([
        'success' => false,
        'message' => 'Database connection failed: ' . $conn->connect_error
    ]));
}

// Set charset to utf8mb4 for better character support
$conn->set_charset("utf8mb4");

// Optional: Set timezone (adjust as needed)
date_default_timezone_set('Asia/Kolkata');

?>
