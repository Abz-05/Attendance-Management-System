-- Attendance Management System Database Setup
-- Drop database if exists and create fresh
DROP DATABASE IF EXISTS attendance_system;
CREATE DATABASE attendance_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE attendance_system;

-- Students Table
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reg_no VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15) NOT NULL,
    board VARCHAR(50),
    marks INT,
    cgpa DECIMAL(4,2),
    join_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_reg_no (reg_no),
    INDEX idx_name (name)
) ENGINE=InnoDB;

-- Faculty Table
CREATE TABLE faculty (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    subject VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_faculty_subject (name, subject)
) ENGINE=InnoDB;

-- Attendance Table
CREATE TABLE attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    faculty_id INT NOT NULL,
    subject VARCHAR(100) NOT NULL,
    date DATE NOT NULL,
    period INT NOT NULL CHECK (period BETWEEN 1 AND 5),
    status ENUM('Present', 'Absent', 'Late') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (faculty_id) REFERENCES faculty(id) ON DELETE CASCADE,
    UNIQUE KEY unique_attendance (student_id, date, period),
    INDEX idx_date (date),
    INDEX idx_student_date (student_id, date),
    INDEX idx_period (period)
) ENGINE=InnoDB;

-- Insert Faculty Data
INSERT INTO faculty (name, subject) VALUES
('Ratchana B', 'Machine Learning'),
('S. Karthiga', 'Big Data Analytics'),
('DSP', 'Computer Networks'),
('Maniram', 'Statistical Data Analysis'),
('Maniram', 'Statistical Data Analysis Lab');

-- Insert Students Data (23 students from your list)
INSERT INTO students (reg_no, name, email, phone, board, marks, cgpa, join_date) VALUES
('C3S48851', 'Abzana V', 'abzanavarhath@gmail.com', '9566977038', 'State Board', 506, 8.06, CURRENT_DATE),
('C3S48852', 'Aishwarya Suruthi A', 'suruthia1807@gmail.com', '9345563182', 'CBSE', 300, 7.43, CURRENT_DATE),
('C3S48853', 'Harini J', 'harini240310@gmail.com', '6380535252', 'State Board', 416, 7.99, CURRENT_DATE),
('C3S48854', 'Harini P', 'harini6975@gmail.com', '9787525459', 'State Board', 387, 7.67, CURRENT_DATE),
('C3S48855', 'Harini S', 'sureshharini545@gmail.com', '9843874239', 'State Board', 450, 7.50, CURRENT_DATE),
('C3S48856', 'R Iswarya Harini', 'iswaryaharini581@gmail.com', '9361346023', 'State Board', 456, 7.88, CURRENT_DATE),
('C3S48857', 'K.Meenakshi', 'meenakshikannan2005@gmail.com', '8667339332', 'CBSE', 290, 7.40, CURRENT_DATE),
('C3S48858', 'Megha S', 'meghasurehkumar02@gmail.com', '7598966344', 'State Board', 527, 8.20, CURRENT_DATE),
('C3S48859', 'Moksha G N', 'moksha4296@gmail.com', '8122693757', 'State Board', 515, 8.50, CURRENT_DATE),
('C3S48860', 'Renugadevi. A', 'renugadevia773@gmail.com', '9080435379', 'State Board', 356, 7.10, CURRENT_DATE),
('C3S48861', 'Sneha I', 'sneha051226@gmail.com', '8668004274', 'State Board', 477, 8.27, CURRENT_DATE),
('C3S48862', 'Subarna N R', 'subarnaramesh362@gmail.com', '8189938147', 'State Board', 556, 8.54, CURRENT_DATE),
('C3S48863', 'R.B.Swati', 'swatirb22@gmail.com', '7904533184', 'CBSE', 369, 8.90, CURRENT_DATE),
('C3S48865', 'R.Ashwin', 'rashwin081105@gmail.com', '8838804174', 'CBSE', 326, 7.02, CURRENT_DATE),
('C3S48866', 'S.Darnal', 'darnal2005@gmail.com', '7538817063', 'State Board', 416, 6.86, CURRENT_DATE),
('C3S48867', 'M.Haripranav', 'haripranav003@gmail.com', '9585667578', 'State Board', 404, 7.75, CURRENT_DATE),
('C3S48868', 'Jitesh Kumar K R', 'ithu252005@gmail.com', '6369991560', 'State Board', 402, 7.79, CURRENT_DATE),
('C3S48869', 'Mohamedh Faizal S', 'mohamedhfaizal47@gmail.com', '9524337764', 'State Board', 494, 8.33, CURRENT_DATE),
('C3S48870', 'M.Muthuganesh', 'muthuganesh.muthuvel@gmail.com', '9345740976', 'State Board', 319, 6.73, CURRENT_DATE),
('C3S48871', 'M.M.Nagasrinivasan', 'nagasrinivasanm.m2005@gmail.com', '9655392000', 'State Board', 399, 6.34, CURRENT_DATE),
('C3S48872', 'T.Santhosh', 'santhoshd102005@gmail.com', '6374892846', 'State Board', 321, NULL, CURRENT_DATE),
('C3S48873', 'K.sivagnanam', 'sivagnanamddy@gmail.com', '8778019156', 'State Board', 420, 6.90, CURRENT_DATE),
('C3S48874', 'M.Sriramchandar', 'sriramchandar6@gmail.com', '9360828808', 'State Board', 375, 6.86, CURRENT_DATE);

-- Create View for Attendance Summary
CREATE VIEW attendance_summary AS
SELECT 
    s.id,
    s.reg_no,
    s.name,
    COUNT(CASE WHEN a.status = 'Present' THEN 1 END) as total_present,
    COUNT(CASE WHEN a.status = 'Absent' THEN 1 END) as total_absent,
    COUNT(CASE WHEN a.status = 'Late' THEN 1 END) as total_late,
    COUNT(a.id) as total_classes,
    ROUND((COUNT(CASE WHEN a.status = 'Present' THEN 1 END) * 100.0 / NULLIF(COUNT(a.id), 0)), 2) as attendance_percentage
FROM students s
LEFT JOIN attendance a ON s.id = a.student_id
GROUP BY s.id, s.reg_no, s.name;

-- Success Message
SELECT 'Database setup completed successfully!' AS message;
SELECT COUNT(*) as total_students FROM students;
SELECT COUNT(*) as total_faculty FROM faculty;
