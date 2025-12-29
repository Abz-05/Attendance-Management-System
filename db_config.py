"""
Database Configuration Module
Handles MySQL database connection and pooling
"""

import mysql.connector
from mysql.connector import pooling, Error
import configparser
import os
from logger_config import logger

class DatabaseConfig:
    """Database connection manager with pooling support"""
    
    _connection_pool = None
    
    @classmethod
    def initialize_pool(cls):
        """Initialize connection pool"""
        if cls._connection_pool is None:
            try:
                # Read configuration
                config = configparser.ConfigParser()
                config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
                config.read(config_path)
                
                # Get database configuration
                db_config = {
                    'host': config.get('database', 'host'),
                    'user': config.get('database', 'user'),
                    'password': config.get('database', 'password'),
                    'database': config.get('database', 'database'),
                    'port': config.getint('database', 'port'),
                    'charset': 'utf8mb4',
                    'autocommit': False
                }
                
                # Create connection pool
                cls._connection_pool = pooling.MySQLConnectionPool(
                    pool_name="attendance_pool",
                    pool_size=5,
                    pool_reset_session=True,
                    **db_config
                )
                
                logger.info("Database connection pool initialized successfully")
                
            except Error as e:
                logger.error(f"Error initializing database connection pool: {e}")
                raise
            except Exception as e:
                logger.error(f"Unexpected error during pool initialization: {e}")
                raise
    
    @classmethod
    def get_connection(cls):
        """
        Get a connection from the pool
        
        Returns:
            mysql.connector.connection.MySQLConnection: Database connection
        """
        if cls._connection_pool is None:
            cls.initialize_pool()
        
        try:
            connection = cls._connection_pool.get_connection()
            logger.debug("Database connection obtained from pool")
            return connection
        except Error as e:
            logger.error(f"Error getting database connection: {e}")
            raise
    
    @classmethod
    def test_connection(cls):
        """
        Test database connection
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            conn.close()
            logger.info("Database connection test successful")
            return True
        except Error as e:
            logger.error(f"Database connection test failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during connection test: {e}")
            return False

def get_db_connection():
    """
    Convenience function to get database connection
    
    Returns:
        mysql.connector.connection.MySQLConnection: Database connection
    """
    return DatabaseConfig.get_connection()
