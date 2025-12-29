-- Data Science and Analytics Attendance System Database Setup
CREATE DATABASE IF NOT EXISTS ds_attendance_system;
USE ds_attendance_system;

-- Students table
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    join_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Faculty table
CREATE TABLE IF NOT EXISTS faculty (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    subject VARCHAR(100) NOT NULL,
    UNIQUE KEY (name, subject)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Attendance table
CREATE TABLE IF NOT EXISTS attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    faculty_id INT NOT NULL,
    subject VARCHAR(100) NOT NULL,
    date DATE NOT NULL,
    period INT NOT NULL, -- 1 to 5
    status ENUM('Present', 'Absent', 'Late') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (faculty_id) REFERENCES faculty(id) ON DELETE CASCADE,
    UNIQUE KEY unique_period_attendance (student_id, date, period)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insert Faculty and Subjects
INSERT IGNORE INTO faculty (name, subject) VALUES
('Ratchana B mam', 'Machine Learning'),
('S. Karthiga mam', 'Big Data Analytics'),
('DSP sir', 'Computer Networks'),
('Maniram sir', 'Statistical Data Analysis'),
('Maniram sir', 'Statistical Data Analysis Lab');

-- Insert 21 Students
INSERT IGNORE INTO students (name, email, join_date) VALUES
('Abishek R', 'abishek@example.com', CURDATE()),
('Akash S', 'akash@example.com', CURDATE()),
('Anitha K', 'anitha@example.com', CURDATE()),
('Bala Murali', 'bala@example.com', CURDATE()),
('Chitra P', 'chitra@example.com', CURDATE()),
('Deepak Kumar', 'deepak@example.com', CURDATE()),
('Divya Bharathi', 'divya@example.com', CURDATE()),
('Eswaran M', 'eswaran@example.com', CURDATE()),
('Gayathri S', 'gayathri@example.com', CURDATE()),
('Hariharan V', 'hariharan@example.com', CURDATE()),
('Ishwarya R', 'ishwarya@example.com', CURDATE()),
('Jeeva T', 'jeeva@example.com', CURDATE()),
('Karthick S', 'karthick@example.com', CURDATE()),
('Kavitha M', 'kavitha@example.com', CURDATE()),
('Logesh W', 'logesh@example.com', CURDATE()),
('Manoj Kumar', 'manoj@example.com', CURDATE()),
('Nandhini K', 'nandhini@example.com', CURDATE()),
('Praveen R', 'praveen@example.com', CURDATE()),
('Ramya S', 'ramya@example.com', CURDATE()),
('Sathish Kumar', 'sathish@example.com', CURDATE()),
('Yogeswari P', 'yogeswari@example.com', CURDATE());
