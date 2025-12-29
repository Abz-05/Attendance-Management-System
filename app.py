"""
Flask Web Application for Attendance Management System
Integrates existing Python modules with beautiful web interface
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
from datetime import date, datetime
from student_manager import StudentManager
from attendance_manager import AttendanceManager
from faculty_manager import FacultyManager
from db_config import DatabaseConfig
from logger_config import logger

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'attendance-system-secret-key-2025'

# Test database connection on startup
try:
    if DatabaseConfig.test_connection():
        logger.info("Flask app started - Database connection successful")
    else:
        logger.error("Flask app started - Database connection failed")
except Exception as e:
    logger.error(f"Error testing database connection: {e}")

# ==================== WEB PAGES ====================

@app.route('/')
def index():
    """Dashboard / Home page"""
    try:
        # Get quick stats
        students = StudentManager.get_all_students()
        today_attendance = AttendanceManager.get_attendance_by_date(date.today())
        
        stats = {
            'total_students': len(students),
            'today_attendance': len(today_attendance),
            'today_date': date.today().strftime('%B %d, %Y')
        }
        
        return render_template('index.html', stats=stats)
    except Exception as e:
        logger.error(f"Error loading dashboard: {e}")
        return render_template('index.html', stats={'total_students': 0, 'today_attendance': 0, 'today_date': date.today().strftime('%B %d, %Y')})

@app.route('/students')
def students_page():
    """Student management page"""
    return render_template('students.html')

@app.route('/attendance')
def attendance_page():
    """Attendance marking page"""
    return render_template('attendance.html')

@app.route('/reports')
def reports_page():
    """Reports and analytics page"""
    return render_template('reports.html')

# ==================== API ENDPOINTS ====================

# Student APIs
@app.route('/api/students/add', methods=['POST'])
def add_student():
    """Add a new student"""
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        reg_no = data.get('reg_no')
        phone = data.get('phone')
        cgpa = data.get('cgpa')
        join_date = data.get('join_date')
        
        if join_date:
            join_date = datetime.strptime(join_date, '%Y-%m-%d').date()
        
        success, message, student_id = StudentManager.add_student(
            name=name, 
            email=email, 
            reg_no=reg_no, 
            phone=phone, 
            cgpa=cgpa, 
            join_date=join_date
        )
        
        return jsonify({
            'success': success,
            'message': message,
            'student_id': student_id
        })
    except Exception as e:
        logger.error(f"Error in add_student API: {e}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

@app.route('/api/students/list', methods=['GET'])
def list_students():
    """Get all students"""
    try:
        students = StudentManager.get_all_students()
        
        # Convert date objects to strings for JSON serialization
        for student in students:
            if 'join_date' in student and student['join_date']:
                student['join_date'] = str(student['join_date'])
            if 'created_at' in student and student['created_at']:
                student['created_at'] = str(student['created_at'])
        
        return jsonify({
            'success': True,
            'students': students
        })
    except Exception as e:
        logger.error(f"Error in list_students API: {e}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}',
            'students': []
        }), 500

@app.route('/api/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    """Get a specific student"""
    try:
        student = StudentManager.get_student_by_id(student_id)
        
        if student:
            # Convert dates to strings
            if 'join_date' in student and student['join_date']:
                student['join_date'] = str(student['join_date'])
            if 'created_at' in student and student['created_at']:
                student['created_at'] = str(student['created_at'])
            
            return jsonify({
                'success': True,
                'student': student
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Student not found'
            }), 404
    except Exception as e:
        logger.error(f"Error in get_student API: {e}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

# Attendance APIs
@app.route('/api/attendance/mark', methods=['POST'])
def mark_attendance():
    """Mark attendance for a student"""
    try:
        data = request.get_json()
        student_id = int(data.get('student_id'))
        faculty_id = int(data.get('faculty_id'))
        subject = data.get('subject')
        attendance_date = data.get('date')
        period = int(data.get('period', 1))
        status = data.get('status', 'Present')
        
        success, message = AttendanceManager.mark_attendance(
            student_id=student_id,
            faculty_id=faculty_id,
            subject=subject,
            attendance_date=attendance_date,
            period=period,
            status=status
        )
        
        return jsonify({
            'success': success,
            'message': message
        })
    except Exception as e:
        logger.error(f"Error in mark_attendance API: {e}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

@app.route('/api/attendance/mark_bulk', methods=['POST'])
def mark_bulk_attendance():
    """Mark attendance for multiple students at once"""
    try:
        data = request.get_json()
        faculty_id = int(data.get('faculty_id'))
        subject = data.get('subject')
        attendance_date = data.get('date')
        period = int(data.get('period', 1))
        records = data.get('records', []) # List of {student_id, status}
        
        success_count = 0
        errors = []
        
        for record in records:
            success, message = AttendanceManager.mark_attendance(
                student_id=int(record['student_id']),
                faculty_id=faculty_id,
                subject=subject,
                attendance_date=attendance_date,
                period=period,
                status=record['status']
            )
            if success:
                success_count += 1
            else:
                errors.append(f"Student {record['student_id']}: {message}")
                
        return jsonify({
            'success': True,
            'message': f'Successfully marked {success_count} records',
            'errors': errors
        })
    except Exception as e:
        logger.error(f"Error in mark_bulk_attendance API: {e}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

@app.route('/api/attendance/today', methods=['GET'])
def today_attendance():
    """Get today's attendance records"""
    try:
        records = AttendanceManager.get_attendance_by_date(date.today())
        
        # Convert dates to strings
        for record in records:
            if 'date' in record and record['date']:
                record['date'] = str(record['date'])
            if 'created_at' in record and record['created_at']:
                record['created_at'] = str(record['created_at'])
        
        return jsonify({
            'success': True,
            'date': str(date.today()),
            'records': records
        })
    except Exception as e:
        logger.error(f"Error in today_attendance API: {e}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}',
            'records': []
        }), 500

@app.route('/api/attendance/date/<date_str>', methods=['GET'])
def attendance_by_date(date_str):
    """Get attendance for a specific date"""
    try:
        records = AttendanceManager.get_attendance_by_date(date_str)
        
        # Convert dates to strings
        for record in records:
            if 'date' in record and record['date']:
                record['date'] = str(record['date'])
            if 'created_at' in record and record['created_at']:
                record['created_at'] = str(record['created_at'])
        
        return jsonify({
            'success': True,
            'date': date_str,
            'records': records
        })
    except Exception as e:
        logger.error(f"Error in attendance_by_date API: {e}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}',
            'records': []
        }), 500

@app.route('/api/attendance/student/<int:student_id>', methods=['GET'])
def student_attendance(student_id):
    """Get attendance history for a student"""
    try:
        records = AttendanceManager.get_student_attendance(student_id)
        
        # Convert dates to strings
        for record in records:
            if 'date' in record and record['date']:
                record['date'] = str(record['date'])
            if 'created_at' in record and record['created_at']:
                record['created_at'] = str(record['created_at'])
        
        return jsonify({
            'success': True,
            'student_id': student_id,
            'records': records
        })
    except Exception as e:
        logger.error(f"Error in student_attendance API: {e}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}',
            'records': []
        }), 500

@app.route('/api/faculty/list', methods=['GET'])
def list_faculty():
    """Get all faculty records"""
    try:
        faculty = FacultyManager.get_all_faculty()
        return jsonify({
            'success': True,
            'faculty': faculty
        })
    except Exception as e:
        logger.error(f"Error in list_faculty API: {e}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}',
            'faculty': []
        }), 500

@app.route('/api/reports/daily/<date_str>', methods=['GET'])
def daily_analysis(date_str):
    """Get daily analysis for all periods"""
    try:
        analysis = AttendanceManager.get_daily_analysis(date_str)
        if analysis:
            return jsonify({
                'success': True,
                'analysis': analysis
            })
        else:
            return jsonify({
                'success': False,
                'message': 'No data found for this date'
            }), 404
    except Exception as e:
        logger.error(f"Error in daily_analysis API: {e}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

@app.route('/api/reports/summary/<int:student_id>', methods=['GET'])
def attendance_summary(student_id):
    """Get attendance summary for a student"""
    try:
        summary = AttendanceManager.get_attendance_summary(student_id)
        student = StudentManager.get_student_by_id(student_id)
        
        if student:
            # Convert dates
            if 'join_date' in student and student['join_date']:
                student['join_date'] = str(student['join_date'])
            if 'created_at' in student and student['created_at']:
                student['created_at'] = str(student['created_at'])
        
        return jsonify({
            'success': True,
            'student': student,
            'summary': summary
        })
    except Exception as e:
        logger.error(f"Error in attendance_summary API: {e}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print(" " * 15 + "ATTENDANCE MANAGEMENT SYSTEM")
    print(" " * 20 + "Web Application")
    print("="*60)
    print("\nStarting Flask server...")
    print("Access the application at: http://localhost:5000")
    print("\nPress CTRL+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
