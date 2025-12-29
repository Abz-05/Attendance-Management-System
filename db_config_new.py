"""
Database Configuration for Attendance Management System
"""
import mysql.connector
from mysql.connector import Error
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename='attendance_system.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class DatabaseConfig:
    """Database configuration and connection management"""
    
    # Database credentials
    DB_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': '',  # Default XAMPP MySQL password is empty
        'database': 'attendance_system',
        'charset': 'utf8mb4',
        'collation': 'utf8mb4_unicode_ci'
    }
    
    @staticmethod
    def get_connection():
        """
        Create and return a database connection
        Returns:
            connection object or None if connection fails
        """
        try:
            connection = mysql.connector.connect(**DatabaseConfig.DB_CONFIG)
            if connection.is_connected():
                logging.info("Database connection established successfully")
                return connection
        except Error as e:
            logging.error(f"Error connecting to MySQL database: {e}")
            print(f"❌ Database connection error: {e}")
            return None
    
    @staticmethod
    def execute_query(query, params=None, fetch=False):
        """
        Execute a SQL query
        Args:
            query: SQL query string
            params: Query parameters (tuple)
            fetch: Whether to fetch results
        Returns:
            Results if fetch=True, else None
        """
        connection = None
        cursor = None
        try:
            connection = DatabaseConfig.get_connection()
            if not connection:
                return None
            
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if fetch:
                results = cursor.fetchall()
                logging.info(f"Query executed successfully, fetched {len(results)} rows")
                return results
            else:
                connection.commit()
                logging.info(f"Query executed successfully, {cursor.rowcount} rows affected")
                return cursor.rowcount
                
        except Error as e:
            logging.error(f"Error executing query: {e}")
            print(f"❌ Query execution error: {e}")
            if connection:
                connection.rollback()
            return None
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()
    
    @staticmethod
    def test_connection():
        """Test database connection"""
        connection = DatabaseConfig.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT DATABASE()")
                db_name = cursor.fetchone()[0]
                print(f"✅ Connected to database: {db_name}")
                cursor.close()
                connection.close()
                return True
            except Error as e:
                print(f"❌ Connection test failed: {e}")
                return False
        return False

if __name__ == "__main__":
    print("Testing database connection...")
    DatabaseConfig.test_connection()
