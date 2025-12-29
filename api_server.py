"""
Attendance Management System - Backend API
Handles all attendance operations, analytics, and data retrieval
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from db_config_new import DatabaseConfig
from datetime import datetime, date
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Configure logging
logging.basicConfig(
    filename='attendance_api.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Period timings configuration
PERIOD_TIMINGS = {
    1: {"start": "09:00", "end": "09:50", "name": "Period 1"},
    2: {"start": "09:50", "end": "10:40", "name": "Period 2"},
    3: {"start": "11:00", "end": "11:50", "name": "Period 3"},
    4: {"start": "11:50", "end": "12:40", "name": "Period 4"},
    5: {"start": "13:30", "end": "15:10", "name": "Period 5"}
}

@app.route('/api/health', methods=['GET'])
def health_check():
    """API health check endpoint"""
    return jsonify({
        'status': 'success',
        'message': 'Attendance Management System API is running',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/students', methods=['GET'])
def get_students():
    """Get all students"""
    try:
        query = "SELECT * FROM students ORDER BY name"
        students = DatabaseConfig.execute_query(query, fetch=True)
        
        if students is not None:
            # Convert date objects to strings
            for student in students:
                if isinstance(student.get('join_date'), date):
                    student['join_date'] = student['join_date'].isoformat()
            
            return jsonify({
                'status': 'success',
                'data': students,
                'count': len(students)
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to fetch students'
            }), 500
    except Exception as e:
        logging.error(f"Error fetching students: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/faculty', methods=['GET'])
def get_faculty():
    """Get all faculty members"""
    try:
        query = "SELECT * FROM faculty ORDER BY name"
        faculty = DatabaseConfig.execute_query(query, fetch=True)
        
        if faculty is not None:
            return jsonify({
                'status': 'success',
                'data': faculty,
                'count': len(faculty)
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to fetch faculty'
            }), 500
    except Exception as e:
        logging.error(f"Error fetching faculty: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/attendance/mark', methods=['POST'])
def mark_attendance():
    """Mark attendance for students"""
    try:
        data = request.json
        faculty_id = data.get('faculty_id')
        subject = data.get('subject')
        attendance_date = data.get('date')
        period = data.get('period')
        attendance_records = data.get('attendance')  # List of {student_id, status}
        
        # Validate required fields
        if not all([faculty_id, subject, attendance_date, period, attendance_records]):
            return jsonify({
                'status': 'error',
                'message': 'Missing required fields'
            }), 400
        
        # Insert attendance records
        success_count = 0
        error_count = 0
        
        for record in attendance_records:
            student_id = record.get('student_id')
            status = record.get('status')
            
            # Check if attendance already exists
            check_query = """
                SELECT id FROM attendance 
                WHERE student_id = %s AND date = %s AND period = %s
            """
            existing = DatabaseConfig.execute_query(
                check_query, 
                (student_id, attendance_date, period), 
                fetch=True
            )
            
            if existing:
                # Update existing record
                update_query = """
                    UPDATE attendance 
                    SET status = %s, faculty_id = %s, subject = %s
                    WHERE student_id = %s AND date = %s AND period = %s
                """
                result = DatabaseConfig.execute_query(
                    update_query,
                    (status, faculty_id, subject, student_id, attendance_date, period)
                )
            else:
                # Insert new record
                insert_query = """
                    INSERT INTO attendance (student_id, faculty_id, subject, date, period, status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                result = DatabaseConfig.execute_query(
                    insert_query,
                    (student_id, faculty_id, subject, attendance_date, period, status)
                )
            
            if result is not None:
                success_count += 1
            else:
                error_count += 1
        
        return jsonify({
            'status': 'success',
            'message': f'Attendance marked successfully for {success_count} students',
            'success_count': success_count,
            'error_count': error_count
        })
        
    except Exception as e:
        logging.error(f"Error marking attendance: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/attendance/daily', methods=['GET'])
def get_daily_attendance():
    """Get daily attendance summary"""
    try:
        attendance_date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
        
        query = """
            SELECT 
                s.id,
                s.reg_no,
                s.name,
                a.period,
                a.status,
                a.subject,
                f.name as faculty_name
            FROM students s
            LEFT JOIN attendance a ON s.id = a.student_id AND a.date = %s
            LEFT JOIN faculty f ON a.faculty_id = f.id
            ORDER BY s.name, a.period
        """
        
        results = DatabaseConfig.execute_query(query, (attendance_date,), fetch=True)
        
        if results is not None:
            # Organize data by student
            students_data = {}
            for row in results:
                student_id = row['id']
                if student_id not in students_data:
                    students_data[student_id] = {
                        'id': row['id'],
                        'reg_no': row['reg_no'],
                        'name': row['name'],
                        'periods': {}
                    }
                
                if row['period']:
                    students_data[student_id]['periods'][row['period']] = {
                        'status': row['status'],
                        'subject': row['subject'],
                        'faculty': row['faculty_name']
                    }
            
            return jsonify({
                'status': 'success',
                'date': attendance_date,
                'data': list(students_data.values())
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to fetch daily attendance'
            }), 500
            
    except Exception as e:
        logging.error(f"Error fetching daily attendance: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/attendance/analytics', methods=['GET'])
def get_attendance_analytics():
    """Get overall attendance analytics"""
    try:
        query = """
            SELECT 
                s.id,
                s.reg_no,
                s.name,
                COUNT(CASE WHEN a.status = 'Present' THEN 1 END) as total_present,
                COUNT(CASE WHEN a.status = 'Absent' THEN 1 END) as total_absent,
                COUNT(CASE WHEN a.status = 'Late' THEN 1 END) as total_late,
                COUNT(a.id) as total_classes,
                ROUND((COUNT(CASE WHEN a.status = 'Present' THEN 1 END) * 100.0 / 
                       NULLIF(COUNT(a.id), 0)), 2) as attendance_percentage
            FROM students s
            LEFT JOIN attendance a ON s.id = a.student_id
            GROUP BY s.id, s.reg_no, s.name
            ORDER BY s.name
        """
        
        results = DatabaseConfig.execute_query(query, fetch=True)
        
        if results is not None:
            return jsonify({
                'status': 'success',
                'data': results,
                'count': len(results)
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to fetch analytics'
            }), 500
            
    except Exception as e:
        logging.error(f"Error fetching analytics: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/student/add', methods=['POST'])
def add_student():
    """Add a new student"""
    try:
        data = request.json
        
        query = """
            INSERT INTO students (reg_no, name, email, phone, board, marks, cgpa)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        result = DatabaseConfig.execute_query(
            query,
            (
                data.get('reg_no'),
                data.get('name'),
                data.get('email'),
                data.get('phone'),
                data.get('board'),
                data.get('marks'),
                data.get('cgpa')
            )
        )
        
        if result is not None:
            return jsonify({
                'status': 'success',
                'message': 'Student added successfully'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to add student'
            }), 500
            
    except Exception as e:
        logging.error(f"Error adding student: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/periods', methods=['GET'])
def get_periods():
    """Get period timings"""
    return jsonify({
        'status': 'success',
        'data': PERIOD_TIMINGS
    })

if __name__ == '__main__':
    print("🚀 Starting Attendance Management System API...")
    print("📍 API will be available at: http://localhost:5000")
    print("📊 Endpoints:")
    print("   - GET  /api/health")
    print("   - GET  /api/students")
    print("   - GET  /api/faculty")
    print("   - POST /api/attendance/mark")
    print("   - GET  /api/attendance/daily")
    print("   - GET  /api/attendance/analytics")
    print("   - POST /api/student/add")
    print("   - GET  /api/periods")
    print("\n✨ Press Ctrl+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
