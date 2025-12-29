USE ds_attendance_system;

-- Add new columns to students table if they don't exist
ALTER TABLE students ADD COLUMN IF NOT EXISTS reg_no VARCHAR(20) UNIQUE;
ALTER TABLE students ADD COLUMN IF NOT EXISTS phone VARCHAR(15);
ALTER TABLE students ADD COLUMN IF NOT EXISTS cgpa DECIMAL(3,2);

-- Clear existing students to insert the updated list with all details
-- (Safe because we are in development and user wants THIS specific list)
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE students;
SET FOREIGN_KEY_CHECKS = 1;

-- Insert the 23 students provided by the user
INSERT INTO students (reg_no, name, email, phone, cgpa, join_date) VALUES
('C3S48851', 'Abzana V', 'abzanavarhath@gmail.com', '9566977038', 8.06, CURDATE()),
('C3S48852', 'Aishwarya Suruthi A', 'suruthia1807@gmail.com', '9345563182', 7.43, CURDATE()),
('C3S48853', 'Harini J', 'harini240310@gmail.com', '6380535252', 7.99, CURDATE()),
('C3S48854', 'Harini P', 'harini6975@gmail.com', '9787525459', 7.67, CURDATE()),
('C3S48855', 'Harini S', 'sureshharini545@gmail.com', '9843874239', 7.50, CURDATE()),
('C3S48856', 'R Iswarya Harini', 'iswaryaharini581@gmail.com', '9361346023', 7.88, CURDATE()),
('C3S48857', 'K.Meenakshi', 'meenakshikannan2005@gmail.com', '8667339332', 7.40, CURDATE()),
('C3S48858', 'Megha S', 'meghasurehkumar02@gmail.com', '7598966344', 8.20, CURDATE()),
('C3S48859', 'Moksha G N', 'moksha4296@gmail.com', '8122693757', 8.50, CURDATE()),
('C3S48860', 'Renugadevi. A', 'renugadevia773@gmail.com', '9080435379', 7.10, CURDATE()),
('C3S48861', 'Sneha I', 'sneha051226@gmail.com', '8668004274', 8.27, CURDATE()),
('C3S48862', 'Subarna N R', 'subarnaramesh362@gmail.com', '8189938147', 8.54, CURDATE()),
('C3S48863', 'R.B.Swati', 'swatirb22@gmail.com', '7904533184', 8.90, CURDATE()),
('C3S48865', 'R.Ashwin', 'rashwin081105@gmail.com', '8838804174', 7.02, CURDATE()),
('C3S48866', 'S.Darnal', 'darnal2005@gmail.com', '7538817063', 6.86, CURDATE()),
('C3S48867', 'M.Haripranav', 'haripranav003@gmail.com', '9585667578', 7.75, CURDATE()),
('C3S48868', 'Jitesh Kumar K R', 'ithu252005@gmail.com', '6369991560', 7.79, CURDATE()),
('C3S48869', 'Mohamedh Faizal S', 'mohamedhfaizal47@gmail.com', '9524337764', 8.33, CURDATE()),
('C3S48870', 'M.Muthuganesh', 'muthuganesh.muthuvel@gmail.com', '9345740976', 6.73, CURDATE()),
('C3S48871', 'M.M.Nagasrinivasan', 'nagasrinivasanm.m2005@gmail.com', '9655392000', 6.34, CURDATE()),
('C3S48872', 'T.Santhosh', 'santhoshd102005@gmail.com', '6374892846', NULL, CURDATE()),
('C3S48873', 'K.sivagnanam', 'sivagnanamddy@gmail.com', '8778019156', 6.90, CURDATE()),
('C3S48874', 'M.Sriramchandar', 'sriramchandar6@gmail.com', '9360828808', 6.86, CURDATE());
