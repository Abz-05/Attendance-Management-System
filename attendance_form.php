<?php
/**
 * Attendance Form Handler
 * This file processes attendance form submissions
 */

// Set header for JSON response
header('Content-Type: application/json');

// Include database connection
require_once 'db_connect.php';

// Check if request method is POST
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    echo json_encode([
        'success' => false,
        'message' => 'Invalid request method. Please use POST.'
    ]);
    exit;
}

// Get and sanitize input data
$employee_id = isset($_POST['employee_id']) ? intval($_POST['employee_id']) : 0;
$date = isset($_POST['date']) ? trim($_POST['date']) : '';
$status = isset($_POST['status']) ? trim($_POST['status']) : '';

// Validation
$errors = [];

if ($employee_id <= 0) {
    $errors[] = 'Valid Employee ID is required.';
}

if (empty($date)) {
    $errors[] = 'Date is required.';
} elseif (!preg_match('/^\d{4}-\d{2}-\d{2}$/', $date)) {
    $errors[] = 'Invalid date format. Use YYYY-MM-DD.';
}

if (!in_array($status, ['Present', 'Absent', 'Leave'])) {
    $errors[] = 'Invalid attendance status.';
}

// If there are validation errors, return them
if (!empty($errors)) {
    echo json_encode([
        'success' => false,
        'message' => implode(' ', $errors)
    ]);
    exit;
}

// Check if user exists
$check_user = $conn->prepare("SELECT id, name FROM users WHERE id = ?");
$check_user->bind_param("i", $employee_id);
$check_user->execute();
$user_result = $check_user->get_result();

if ($user_result->num_rows === 0) {
    echo json_encode([
        'success' => false,
        'message' => 'Employee ID not found in the system.'
    ]);
    $check_user->close();
    exit;
}

$user_data = $user_result->fetch_assoc();
$check_user->close();

// Check if attendance already exists for this user and date
$check_attendance = $conn->prepare("SELECT id FROM attendance WHERE user_id = ? AND date = ?");
$check_attendance->bind_param("is", $employee_id, $date);
$check_attendance->execute();
$attendance_result = $check_attendance->get_result();

if ($attendance_result->num_rows > 0) {
    echo json_encode([
        'success' => false,
        'message' => 'Attendance for this employee on this date already exists.'
    ]);
    $check_attendance->close();
    exit;
}
$check_attendance->close();

// Insert attendance record using prepared statement
$stmt = $conn->prepare("INSERT INTO attendance (user_id, date, status) VALUES (?, ?, ?)");
$stmt->bind_param("iss", $employee_id, $date, $status);

if ($stmt->execute()) {
    echo json_encode([
        'success' => true,
        'message' => 'Attendance recorded successfully for ' . htmlspecialchars($user_data['name']) . '!',
        'data' => [
            'employee_name' => $user_data['name'],
            'employee_id' => $employee_id,
            'date' => $date,
            'status' => $status
        ]
    ]);
} else {
    echo json_encode([
        'success' => false,
        'message' => 'Error recording attendance: ' . $stmt->error
    ]);
}

// Close statement and connection
$stmt->close();
$conn->close();
?>
