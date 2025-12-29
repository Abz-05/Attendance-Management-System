"""
Attendance Management Module
Handles all attendance-related operations
"""

from datetime import date, datetime
from mysql.connector import Error
from db_config import get_db_connection
from logger_config import logger

class AttendanceManager:
    """Manages attendance records and operations"""
    
    VALID_STATUSES = ['Present', 'Absent', 'Late']
    
    PERIOD_TIMINGS = {
        1: ("09:00", "09:50"),
        2: ("09:50", "10:40"),
        # Break 10:40 - 11:00
        3: ("11:00", "11:50"),
        4: ("11:50", "12:40"),
        # Break 12:40 - 13:30
        5: ("13:30", "15:10")
    }
    
    @staticmethod
    def validate_status(status):
        """
        Validate attendance status
        
        Args:
            status (str): Status to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        return status in AttendanceManager.VALID_STATUSES
    
    @staticmethod
    def mark_attendance(student_id, faculty_id, subject, attendance_date=None, period=1, status='Present'):
        """
        Mark attendance for a student
        
        Args:
            student_id (int): Student ID
            faculty_id (int): Faculty ID
            subject (str): Subject name
            attendance_date (str/date, optional): Date (defaults to today)
            period (int): Period number (1-5)
            status (str): Attendance status (Present/Absent/Late)
            
        Returns:
            tuple: (success: bool, message: str)
        """
        # Validate status
        if not AttendanceManager.validate_status(status):
            logger.warning(f"Invalid attendance status: {status}")
            return (False, f"Invalid status. Must be one of: {', '.join(AttendanceManager.VALID_STATUSES)}")
        
        # Validate period
        if period not in range(1, 6):
            return (False, "Invalid period. Must be between 1 and 5")
            
        # Set date to today if not provided
        if attendance_date is None:
            attendance_date = date.today()
        elif isinstance(attendance_date, str):
            try:
                attendance_date = datetime.strptime(attendance_date, '%Y-%m-%d').date()
            except ValueError:
                logger.warning(f"Invalid date format: {attendance_date}")
                return (False, "Invalid date format. Use YYYY-MM-DD")
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Check if student exists
            cursor.execute("SELECT id, name FROM students WHERE id = %s", (student_id,))
            student = cursor.fetchone()
            
            if not student:
                logger.warning(f"Attempted to mark attendance for non-existent student ID: {student_id}")
                cursor.close()
                conn.close()
                return (False, f"Student with ID {student_id} not found")
            
            student_name = student[1]
            
            # Check if attendance already marked for this period on this date
            cursor.execute("SELECT id FROM attendance WHERE student_id = %s AND date = %s AND period = %s", 
                          (student_id, attendance_date, period))
            existing = cursor.fetchone()
            
            if existing:
                # Update existing record
                query = "UPDATE attendance SET faculty_id = %s, subject = %s, status = %s WHERE id = %s"
                cursor.execute(query, (faculty_id, subject, status, existing[0]))
                message = f"Attendance updated for {student_name} (Period {period})"
            else:
                # Insert new attendance record
                query = "INSERT INTO attendance (student_id, faculty_id, subject, date, period, status) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(query, (student_id, faculty_id, subject, attendance_date, period, status))
                message = f"Attendance marked for {student_name} (Period {period})"
            
            conn.commit()
            logger.info(f"{message}: {status}")
            
            cursor.close()
            conn.close()
            
            return (True, message)
            
        except Error as e:
            logger.error(f"Database error while marking attendance: {e}")
            return (False, f"Database error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error while marking attendance: {e}")
            return (False, f"Unexpected error: {e}")
    
    @staticmethod
    def mark_bulk_attendance(attendance_list):
        """
        Mark attendance for multiple students
        
        Args:
            attendance_list (list): List of tuples [(student_id, date, status), ...]
            
        Returns:
            tuple: (success_count: int, failed_count: int, messages: list)
        """
        success_count = 0
        failed_count = 0
        messages = []
        
        for attendance in attendance_list:
            if len(attendance) < 2:
                failed_count += 1
                messages.append(f"Invalid attendance data format: {attendance}")
                continue
            
            student_id = attendance[0]
            attendance_date = attendance[1] if len(attendance) > 1 else None
            status = attendance[2] if len(attendance) > 2 else 'Present'
            
            success, message = AttendanceManager.mark_attendance(student_id, attendance_date, status)
            
            if success:
                success_count += 1
            else:
                failed_count += 1
            
            messages.append(message)
        
        logger.info(f"Bulk attendance marking completed: {success_count} successful, {failed_count} failed")
        return (success_count, failed_count, messages)
    
    @staticmethod
    def get_attendance_by_date(attendance_date=None, period=None):
        """
        Get all attendance records for a specific date and period
        
        Args:
            attendance_date (str/date, optional): Date (defaults to today)
            period (int, optional): Period number
            
        Returns:
            list: List of attendance records
        """
        if attendance_date is None:
            attendance_date = date.today()
        elif isinstance(attendance_date, str):
            try:
                attendance_date = datetime.strptime(attendance_date, '%Y-%m-%d').date()
            except ValueError:
                logger.warning(f"Invalid date format: {attendance_date}")
                return []
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT a.id, a.student_id, s.name, a.subject, f.name as faculty_name, a.date, a.period, a.status, a.created_at
                FROM attendance a
                JOIN students s ON a.student_id = s.id
                JOIN faculty f ON a.faculty_id = f.id
                WHERE a.date = %s
            """
            params = [attendance_date]
            
            if period:
                query += " AND a.period = %s"
                params.append(period)
                
            query += " ORDER BY s.name, a.period"
            
            cursor.execute(query, tuple(params))
            records = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return records
            
        except Error as e:
            logger.error(f"Database error while retrieving attendance: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error while retrieving attendance: {e}")
            return []
    
    @staticmethod
    def get_student_attendance(student_id):
        """
        Get attendance history for a specific student
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT a.id, a.date, a.period, a.subject, f.name as faculty_name, a.status, a.created_at
                FROM attendance a
                JOIN faculty f ON a.faculty_id = f.id
                WHERE a.student_id = %s
                ORDER BY a.date DESC, a.period DESC
            """
            cursor.execute(query, (student_id,))
            records = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return records
            
        except Error as e:
            logger.error(f"Database error while retrieving student attendance: {e}")
            return []
    
    @staticmethod
    def get_attendance_summary(student_id):
        """
        Get attendance summary/statistics for a student
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Total classes conduct across all periods recorded for this student
            cursor.execute("SELECT COUNT(*) FROM attendance WHERE student_id = %s", (student_id,))
            total = cursor.fetchone()[0]
            
            # Get status counts
            cursor.execute("""
                SELECT status, COUNT(*) as count 
                FROM attendance 
                WHERE student_id = %s 
                GROUP BY status
            """, (student_id,))
            
            status_counts = {row[0]: row[1] for row in cursor.fetchall()}
            
            cursor.close()
            conn.close()
            
            present_count = status_counts.get('Present', 0)
            absent_count = status_counts.get('Absent', 0)
            late_count = status_counts.get('Late', 0)
            
            percentage = (present_count / total * 100) if total > 0 else 0
            
            summary = {
                'total': total,
                'present': present_count,
                'absent': absent_count,
                'late': late_count,
                'attendance_percentage': round(percentage, 2)
            }
            
            return summary
            
        except Error as e:
            logger.error(f"Database error while generating attendance summary: {e}")
            return {'total': 0, 'present': 0, 'absent': 0, 'late': 0, 'attendance_percentage': 0}

    @staticmethod
    def get_daily_analysis(report_date=None):
        """
        Get daily attendance analysis for all periods
        """
        if report_date is None:
            report_date = date.today()
        elif isinstance(report_date, str):
            report_date = datetime.strptime(report_date, '%Y-%m-%d').date()
            
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Get period-wise summary
            query = """
                SELECT period, 
                       COUNT(CASE WHEN status = 'Present' THEN 1 END) as present,
                       COUNT(CASE WHEN status = 'Absent' THEN 1 END) as absent,
                       COUNT(CASE WHEN status = 'Late' THEN 1 END) as late
                FROM attendance 
                WHERE date = %s
                GROUP BY period
                ORDER BY period
            """
            cursor.execute(query, (report_date,))
            period_summary = cursor.fetchall()
            
            # Get student-wise summary for the day
            query = """
                SELECT s.name, s.reg_no,
                       COUNT(CASE WHEN a.status = 'Present' THEN 1 END) as present,
                       COUNT(CASE WHEN a.status = 'Absent' THEN 1 END) as absent,
                       COUNT(CASE WHEN a.status = 'Late' THEN 1 END) as late,
                       GROUP_CONCAT(CONCAT(a.period, ':', a.status) ORDER BY a.period) as period_details
                FROM students s
                LEFT JOIN attendance a ON s.id = a.student_id AND a.date = %s
                GROUP BY s.id, s.name, s.reg_no
                ORDER BY s.name
            """
            cursor.execute(query, (report_date,))
            student_daily = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return {
                'date': str(report_date),
                'period_summary': period_summary,
                'student_daily': student_daily
            }
        except Exception as e:
            logger.error(f"Error in get_daily_analysis: {e}")
            return None
