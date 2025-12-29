"""
Main Application - Attendance Management System
Interactive menu-driven system for managing students and attendance
"""

import sys
from datetime import date, datetime
from student_manager import StudentManager
from attendance_manager import AttendanceManager
from db_config import DatabaseConfig
from logger_config import logger

def print_header():
    """Print application header"""
    print("\n" + "="*60)
    print(" " * 15 + "ATTENDANCE MANAGEMENT SYSTEM")
    print("="*60 + "\n")

def print_menu():
    """Print main menu"""
    print("\n" + "-"*60)
    print("MAIN MENU")
    print("-"*60)
    print("1. Add New Student")
    print("2. Add Multiple Students")
    print("3. View All Students")
    print("4. Mark Daily Attendance")
    print("5. Mark Bulk Attendance")
    print("6. View Today's Attendance")
    print("7. View Attendance by Date")
    print("8. View Student Attendance History")
    print("9. View Student Attendance Summary")
    print("0. Exit")
    print("-"*60)

def add_new_student():
    """Add a single new student"""
    print("\n--- Add New Student ---")
    try:
        name = input("Enter student name: ").strip()
        email = input("Enter student email: ").strip()
        
        use_custom_date = input("Use custom join date? (y/n, default: today): ").strip().lower()
        
        join_date = None
        if use_custom_date == 'y':
            date_str = input("Enter join date (YYYY-MM-DD): ").strip()
            try:
                join_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                print("Invalid date format. Using today's date.")
                join_date = None
        
        success, message, student_id = StudentManager.add_student(name, email, join_date)
        
        if success:
            print(f"\n✓ SUCCESS: {message}")
        else:
            print(f"\n✗ ERROR: {message}")
            
    except KeyboardInterrupt:
        print("\n\nOperation cancelled.")
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        logger.error(f"Error in add_new_student: {e}")

def add_multiple_students():
    """Add multiple students"""
    print("\n--- Add Multiple Students ---")
    try:
        count = int(input("How many students to add? "))
        students_list = []
        
        for i in range(count):
            print(f"\nStudent {i+1}:")
            name = input("  Name: ").strip()
            email = input("  Email: ").strip()
            students_list.append((name, email))
        
        print("\nProcessing...")
        success_count, failed_count, messages = StudentManager.add_students_bulk(students_list)
        
        print(f"\n{'='*60}")
        print(f"BULK IMPORT RESULTS:")
        print(f"  Successful: {success_count}")
        print(f"  Failed: {failed_count}")
        print(f"{'='*60}")
        
        if input("\nShow detailed messages? (y/n): ").strip().lower() == 'y':
            for msg in messages:
                print(f"  - {msg}")
                
    except ValueError:
        print("\n✗ ERROR: Invalid number entered.")
    except KeyboardInterrupt:
        print("\n\nOperation cancelled.")
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        logger.error(f"Error in add_multiple_students: {e}")

def view_all_students():
    """Display all students"""
    print("\n--- All Students ---")
    students = StudentManager.get_all_students()
    
    if not students:
        print("No students found in the database.")
        return
    
    print(f"\nTotal Students: {len(students)}\n")
    print(f"{'ID':<5} {'Name':<25} {'Email':<30} {'Join Date':<12}")
    print("-"*75)
    
    for student in students:
        print(f"{student['id']:<5} {student['name']:<25} {student['email']:<30} {student['join_date']}")

def mark_daily_attendance():
    """Mark attendance for students"""
    print("\n--- Mark Daily Attendance ---")
    try:
        student_id = int(input("Enter student ID: "))
        
        use_custom_date = input("Use custom date? (y/n, default: today): ").strip().lower()
        attendance_date = None
        
        if use_custom_date == 'y':
            date_str = input("Enter date (YYYY-MM-DD): ").strip()
            attendance_date = date_str
        
        print("\nAttendance Status:")
        print("1. Present")
        print("2. Absent")
        print("3. Leave")
        
        status_choice = input("Select status (1-3, default: Present): ").strip()
        status_map = {'1': 'Present', '2': 'Absent', '3': 'Leave'}
        status = status_map.get(status_choice, 'Present')
        
        success, message = AttendanceManager.mark_attendance(student_id, attendance_date, status)
        
        if success:
            print(f"\n✓ SUCCESS: {message}")
        else:
            print(f"\n✗ ERROR: {message}")
            
    except ValueError:
        print("\n✗ ERROR: Invalid student ID.")
    except KeyboardInterrupt:
        print("\n\nOperation cancelled.")
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        logger.error(f"Error in mark_daily_attendance: {e}")

def mark_bulk_attendance():
    """Mark attendance for multiple students"""
    print("\n--- Mark Bulk Attendance ---")
    try:
        # Show all students first
        students = StudentManager.get_all_students()
        if not students:
            print("No students found in database.")
            return
        
        print("\nAvailable Students:")
        for student in students:
            print(f"  ID {student['id']}: {student['name']}")
        
        use_custom_date = input("\nUse custom date? (y/n, default: today): ").strip().lower()
        attendance_date = None
        
        if use_custom_date == 'y':
            date_str = input("Enter date (YYYY-MM-DD): ").strip()
            attendance_date = date_str
        
        print("\nAttendance Status Options:")
        print("1. Present  2. Absent  3. Leave")
        
        attendance_list = []
        for student in students:
            status_choice = input(f"\nStatus for {student['name']} (ID {student['id']}) [1-3, Enter to skip]: ").strip()
            
            if not status_choice:
                continue
            
            status_map = {'1': 'Present', '2': 'Absent', '3': 'Leave'}
            status = status_map.get(status_choice, 'Present')
            
            attendance_list.append((student['id'], attendance_date, status))
        
        if not attendance_list:
            print("\nNo attendance records to mark.")
            return
        
        print("\nProcessing...")
        success_count, failed_count, messages = AttendanceManager.mark_bulk_attendance(attendance_list)
        
        print(f"\n{'='*60}")
        print(f"BULK ATTENDANCE RESULTS:")
        print(f"  Successful: {success_count}")
        print(f"  Failed: {failed_count}")
        print(f"{'='*60}")
        
        if input("\nShow detailed messages? (y/n): ").strip().lower() == 'y':
            for msg in messages:
                print(f"  - {msg}")
                
    except KeyboardInterrupt:
        print("\n\nOperation cancelled.")
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        logger.error(f"Error in mark_bulk_attendance: {e}")

def view_todays_attendance():
    """View today's attendance records"""
    print("\n--- Today's Attendance ---")
    records = AttendanceManager.get_attendance_by_date()
    
    if not records:
        print(f"No attendance records found for {date.today()}")
        return
    
    print(f"\nDate: {date.today()}")
    print(f"Total Records: {len(records)}\n")
    print(f"{'ID':<5} {'Student Name':<25} {'Email':<30} {'Status':<10}")
    print("-"*75)
    
    for record in records:
        print(f"{record['student_id']:<5} {record['name']:<25} {record['email']:<30} {record['status']:<10}")

def view_attendance_by_date():
    """View attendance for a specific date"""
    print("\n--- View Attendance by Date ---")
    try:
        date_str = input("Enter date (YYYY-MM-DD): ").strip()
        records = AttendanceManager.get_attendance_by_date(date_str)
        
        if not records:
            print(f"\nNo attendance records found for {date_str}")
            return
        
        print(f"\nDate: {date_str}")
        print(f"Total Records: {len(records)}\n")
        print(f"{'ID':<5} {'Student Name':<25} {'Email':<30} {'Status':<10}")
        print("-"*75)
        
        for record in records:
            print(f"{record['student_id']:<5} {record['name']:<25} {record['email']:<30} {record['status']:<10}")
            
    except KeyboardInterrupt:
        print("\n\nOperation cancelled.")
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        logger.error(f"Error in view_attendance_by_date: {e}")

def view_student_attendance_history():
    """View attendance history for a student"""
    print("\n--- Student Attendance History ---")
    try:
        student_id = int(input("Enter student ID: "))
        
        # Get student details
        student = StudentManager.get_student_by_id(student_id)
        if not student:
            print(f"\n✗ ERROR: Student with ID {student_id} not found.")
            return
        
        records = AttendanceManager.get_student_attendance(student_id)
        
        if not records:
            print(f"\nNo attendance records found for {student['name']}")
            return
        
        print(f"\nStudent: {student['name']} (ID: {student_id})")
        print(f"Email: {student['email']}")
        print(f"Total Records: {len(records)}\n")
        print(f"{'Date':<12} {'Status':<10} {'Marked At':<20}")
        print("-"*45)
        
        for record in records:
            marked_at = record['created_at'].strftime('%Y-%m-%d %H:%M:%S') if record['created_at'] else 'N/A'
            print(f"{record['date']:<12} {record['status']:<10} {marked_at:<20}")
            
    except ValueError:
        print("\n✗ ERROR: Invalid student ID.")
    except KeyboardInterrupt:
        print("\n\nOperation cancelled.")
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        logger.error(f"Error in view_student_attendance_history: {e}")

def view_attendance_summary():
    """View attendance summary for a student"""
    print("\n--- Student Attendance Summary ---")
    try:
        student_id = int(input("Enter student ID: "))
        
        # Get student details
        student = StudentManager.get_student_by_id(student_id)
        if not student:
            print(f"\n✗ ERROR: Student with ID {student_id} not found.")
            return
        
        summary = AttendanceManager.get_attendance_summary(student_id)
        
        if not summary or summary['total'] == 0:
            print(f"\nNo attendance records found for {student['name']}")
            return
        
        print(f"\n{'='*60}")
        print(f"ATTENDANCE SUMMARY - {student['name']}")
        print(f"{'='*60}")
        print(f"Email: {student['email']}")
        print(f"Join Date: {student['join_date']}")
        print(f"\nAttendance Statistics:")
        print(f"  Total Days: {summary['total']}")
        print(f"  Present: {summary['present']}")
        print(f"  Absent: {summary['absent']}")
        print(f"  Leave: {summary['leave']}")
        print(f"  Attendance Percentage: {summary['attendance_percentage']}%")
        print(f"{'='*60}")
        
    except ValueError:
        print("\n✗ ERROR: Invalid student ID.")
    except KeyboardInterrupt:
        print("\n\nOperation cancelled.")
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        logger.error(f"Error in view_attendance_summary: {e}")

def main():
    """Main application loop"""
    print_header()
    
    # Test database connection
    print("Testing database connection...")
    if not DatabaseConfig.test_connection():
        print("\n✗ ERROR: Could not connect to database!")
        print("Please check your database configuration in config.ini")
        print("Ensure MySQL server is running and credentials are correct.")
        sys.exit(1)
    
    print("✓ Database connection successful!\n")
    logger.info("Application started")
    
    menu_functions = {
        '1': add_new_student,
        '2': add_multiple_students,
        '3': view_all_students,
        '4': mark_daily_attendance,
        '5': mark_bulk_attendance,
        '6': view_todays_attendance,
        '7': view_attendance_by_date,
        '8': view_student_attendance_history,
        '9': view_attendance_summary
    }
    
    while True:
        try:
            print_menu()
            choice = input("\nEnter your choice (0-9): ").strip()
            
            if choice == '0':
                print("\n" + "="*60)
                print("Thank you for using Attendance Management System!")
                print("="*60 + "\n")
                logger.info("Application closed")
                sys.exit(0)
            
            if choice in menu_functions:
                menu_functions[choice]()
            else:
                print("\n✗ Invalid choice. Please select 0-9.")
                
        except KeyboardInterrupt:
            print("\n\n" + "="*60)
            print("Application interrupted. Exiting...")
            print("="*60 + "\n")
            logger.info("Application interrupted by user")
            sys.exit(0)
        except Exception as e:
            print(f"\n✗ Unexpected error: {e}")
            logger.error(f"Unexpected error in main loop: {e}")

if __name__ == "__main__":
    main()
