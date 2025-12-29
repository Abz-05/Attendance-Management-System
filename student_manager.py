"""
Student Management Module
Handles all student-related operations including auto-addition
"""

from datetime import date
from mysql.connector import Error
import re
from db_config import get_db_connection
from logger_config import logger

class StudentManager:
    """Manages student records and operations"""
    
    @staticmethod
    def validate_email(email):
        """
        Validate email format
        
        Args:
            email (str): Email to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def add_student(name, email, reg_no=None, phone=None, cgpa=None, join_date=None):
        """
        Add a new student to the database with all details
        
        Args:
            name (str): Student name
            email (str): Student email
            reg_no (str, optional): Registration number
            phone (str, optional): Phone number
            cgpa (float, optional): CGPA
            join_date (str/date, optional): Join date (defaults to today)
            
        Returns:
            tuple: (success: bool, message: str, student_id: int or None)
        """
        # Validate inputs
        if not name or not name.strip():
            logger.warning("Attempted to add student with empty name")
            return (False, "Student name cannot be empty", None)
        
        if not email or not email.strip():
            logger.warning("Attempted to add student with empty email")
            return (False, "Student email cannot be empty", None)
        
        email = email.strip().lower()
        
        if not StudentManager.validate_email(email):
            logger.warning(f"Invalid email format: {email}")
            return (False, f"Invalid email format: {email}", None)
        
        # Set join date to today if not provided
        if join_date is None:
            join_date = date.today()
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Check if student already exists
            cursor.execute("SELECT id, name FROM students WHERE email = %s", (email,))
            existing = cursor.fetchone()
            
            if existing:
                logger.info(f"Student with email {email} already exists (ID: {existing[0]})")
                cursor.close()
                conn.close()
                return (False, f"Student '{existing[1]}' with email {email} already exists", None)
            
            # Insert new student
            query = "INSERT INTO students (name, email, reg_no, phone, cgpa, join_date) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (name.strip(), email, reg_no, phone, cgpa, join_date))
            conn.commit()
            
            student_id = cursor.lastrowid
            logger.info(f"Successfully added student: {name} (ID: {student_id}, Email: {email})")
            
            cursor.close()
            conn.close()
            
            return (True, f"Student '{name}' added successfully with ID: {student_id}", student_id)
            
        except Error as e:
            logger.error(f"Database error while adding student: {e}")
            return (False, f"Database error: {e}", None)
        except Exception as e:
            logger.error(f"Unexpected error while adding student: {e}")
            return (False, f"Unexpected error: {e}", None)
    
    @staticmethod
    def add_students_bulk(students_list):
        """
        Add multiple students at once
        
        Args:
            students_list (list): List of tuples [(name, email), (name, email), ...]
            
        Returns:
            tuple: (success_count: int, failed_count: int, messages: list)
        """
        success_count = 0
        failed_count = 0
        messages = []
        
        for student in students_list:
            if len(student) != 2:
                failed_count += 1
                messages.append(f"Invalid student data format: {student}")
                continue
            
            name, email = student
            success, message, student_id = StudentManager.add_student(name, email)
            
            if success:
                success_count += 1
            else:
                failed_count += 1
            
            messages.append(message)
        
        logger.info(f"Bulk student import completed: {success_count} successful, {failed_count} failed")
        return (success_count, failed_count, messages)
    
    @staticmethod
    def get_all_students():
        """
        Get all students from database
        
        Returns:
            list: List of student records as dictionaries
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("SELECT id, name, email, reg_no, phone, cgpa, join_date, created_at FROM students ORDER BY name")
            students = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            logger.info(f"Retrieved {len(students)} students from database")
            return students
            
        except Error as e:
            logger.error(f"Database error while retrieving students: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error while retrieving students: {e}")
            return []
    
    @staticmethod
    def get_student_by_id(student_id):
        """
        Get student by ID
        
        Args:
            student_id (int): Student ID
            
        Returns:
            dict or None: Student record or None if not found
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("SELECT id, name, email, reg_no, phone, cgpa, join_date, created_at FROM students WHERE id = %s", 
                          (student_id,))
            student = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if student:
                logger.debug(f"Found student with ID {student_id}")
            else:
                logger.debug(f"No student found with ID {student_id}")
            
            return student
            
        except Error as e:
            logger.error(f"Database error while retrieving student: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error while retrieving student: {e}")
            return None
    
    @staticmethod
    def get_student_by_email(email):
        """
        Get student by email
        
        Args:
            email (str): Student email
            
        Returns:
            dict or None: Student record or None if not found
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("SELECT id, name, email, join_date, created_at FROM students WHERE email = %s", 
                          (email.lower().strip(),))
            student = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if student:
                logger.debug(f"Found student with email {email}")
            else:
                logger.debug(f"No student found with email {email}")
            
            return student
            
        except Error as e:
            logger.error(f"Database error while retrieving student: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error while retrieving student: {e}")
            return None
