from mysql.connector import Error
from db_config import get_db_connection
from logger_config import logger

class FacultyManager:
    @staticmethod
    def get_all_faculty():
        """Get all faculty and their subjects"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, name, subject FROM faculty ORDER BY name")
            faculty = cursor.fetchall()
            cursor.close()
            conn.close()
            return faculty
        except Error as e:
            logger.error(f"Error getting faculty: {e}")
            return []

    @staticmethod
    def get_faculty_by_id(faculty_id):
        """Get faculty by ID"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, name, subject FROM faculty WHERE id = %s", (faculty_id,))
            faculty = cursor.fetchone()
            cursor.close()
            conn.close()
            return faculty
        except Error as e:
            logger.error(f"Error getting faculty: {e}")
            return None
