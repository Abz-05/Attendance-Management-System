import mysql.connector
import configparser
import os
import sys

def run_sql_file(filename):
    if not os.path.exists(filename):
        print(f"File {filename} not found")
        return

    config = configparser.ConfigParser()
    config.read('config.ini')
    
    try:
        conn = mysql.connector.connect(
            host=config.get('database', 'host'),
            user=config.get('database', 'user'),
            password=config.get('database', 'password'),
            port=config.getint('database', 'port')
        )
        cursor = conn.cursor()
        
        with open(filename, 'r', encoding='utf-8') as f:
            sql = f.read()
            
        commands = sql.split(';')
        
        for command in commands:
            if command.strip():
                try:
                    cursor.execute(command)
                except Exception as e:
                    print(f"Error executing command: {e}")
                    
        conn.commit()
        cursor.close()
        conn.close()
        print(f"SQL script {filename} executed successfully")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    target_file = sys.argv[1] if len(sys.argv) > 1 else 'data_science_setup.sql'
    run_sql_file(target_file)
