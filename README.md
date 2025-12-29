# 🎓 Attendance Management System

A comprehensive, modern web-based attendance management system built with **Python Flask**, **MySQL**, **HTML/CSS/JavaScript**, and **Chart.js** for beautiful data visualizations.

![System Status](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)
![MySQL](https://img.shields.io/badge/mysql-8.0+-orange.svg)

## ✨ Features

### 📝 Attendance Management

- **Period-wise Tracking**: Mark attendance for 5 periods per day
- **Quick Actions**: Mark all present/absent with one click
- **Real-time Updates**: Instant feedback and validation
- **Date Selection**: Mark attendance for any date
- **Faculty & Subject Selection**: Organized by faculty and subject

### 📊 Analytics Dashboard

- **Interactive Charts**: Switch between Bar, Line, and Pie charts
- **Real-time Statistics**: Total students, average attendance, classes, and late arrivals
- **Student-wise Reports**: Detailed attendance percentage for each student
- **Visual Insights**: Color-coded attendance status
- **Auto-refresh**: Updates every 30 seconds

### 📅 Daily Reports

- **Period-wise View**: See all 5 periods for any date
- **Summary Statistics**: Quick overview of daily attendance
- **Subject Information**: View which subject was taught in each period
- **Faculty Details**: See which faculty conducted each class

### 🎨 Modern UI/UX

- **Vibrant Design**: Beautiful gradients and glassmorphism effects
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Smooth Animations**: Hover effects and transitions
- **Professional Typography**: Inter font family
- **Intuitive Navigation**: Easy-to-use interface

## 🚀 Quick Start

### Prerequisites

- XAMPP (Apache + MySQL)
- Python 3.8 or higher
- Modern web browser

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/Abz-05/Attendance-Management-System.git
cd Attendance-Management-System
```

2. **Install Python dependencies**

```bash
pip install -r requirements.txt
```

3. **Set up the database**

```bash
# Start MySQL in XAMPP
# Then import the database
mysql -u root < attendance_system_setup.sql
```

4. **Start the API server**

```bash
python api_server.py
```

5. **Open the application**

```
Open index.html in your browser
```

## 📁 Project Structure

```
Attendance-Management-System/
├── 📄 index.html                    # Main landing page
├── 📄 mark_attendance.html          # Attendance marking interface
├── 📄 analytics.html                # Analytics dashboard with charts
├── 📄 daily_report.html             # Daily attendance reports
├── 🐍 api_server.py                 # Flask API backend
├── 🐍 db_config_new.py              # Database configuration
├── 🗄️ attendance_system_setup.sql   # Database schema & data
├── 📋 requirements.txt              # Python dependencies
├── 📖 SETUP_GUIDE.md                # Detailed setup instructions
├── 📖 QUICK_START.md                # Quick reference guide
└── 📖 README.md                     # This file
```

## 🎯 System Configuration

### Students

- **Total**: 23 students
- **Registration Numbers**: C3S48851 to C3S48874
- **Details**: Name, Email, Phone, Board, Marks, CGPA

### Faculty & Subjects

| Faculty     | Subject                       |
| ----------- | ----------------------------- |
| Ratchana B  | Machine Learning              |
| S. Karthiga | Big Data Analytics            |
| DSP         | Computer Networks             |
| Maniram     | Statistical Data Analysis     |
| Maniram     | Statistical Data Analysis Lab |

### Period Timings

| Period    | Time          | Duration |
| --------- | ------------- | -------- |
| Period 1  | 09:00 - 09:50 | 50 mins  |
| Period 2  | 09:50 - 10:40 | 50 mins  |
| **Break** | 10:40 - 11:00 | 20 mins  |
| Period 3  | 11:00 - 11:50 | 50 mins  |
| Period 4  | 11:50 - 12:40 | 50 mins  |
| **Lunch** | 12:40 - 13:30 | 50 mins  |
| Period 5  | 13:30 - 15:10 | 100 mins |

## 🔌 API Endpoints

| Method | Endpoint                    | Description        |
| ------ | --------------------------- | ------------------ |
| GET    | `/api/health`               | Health check       |
| GET    | `/api/students`             | Get all students   |
| GET    | `/api/faculty`              | Get all faculty    |
| POST   | `/api/attendance/mark`      | Mark attendance    |
| GET    | `/api/attendance/daily`     | Get daily report   |
| GET    | `/api/attendance/analytics` | Get analytics data |
| POST   | `/api/student/add`          | Add new student    |
| GET    | `/api/periods`              | Get period timings |

## 💾 Database Schema

### Students Table

```sql
- id (Primary Key)
- reg_no (Unique)
- name
- email (Unique)
- phone
- board
- marks
- cgpa
- join_date
- created_at
```

### Faculty Table

```sql
- id (Primary Key)
- name
- subject
- created_at
```

### Attendance Table

```sql
- id (Primary Key)
- student_id (Foreign Key)
- faculty_id (Foreign Key)
- subject
- date
- period (1-5)
- status (Present/Absent/Late)
- created_at
```

## 🛠️ Technologies Used

### Backend

- **Python 3.8+**: Core programming language
- **Flask 3.0.0**: Web framework for API
- **MySQL 8.0+**: Database management
- **mysql-connector-python**: Database connectivity

### Frontend

- **HTML5**: Structure
- **CSS3**: Styling with gradients and animations
- **JavaScript (ES6+)**: Interactivity and API calls
- **Chart.js 4.4.0**: Data visualization
- **Inter Font**: Modern typography

### Tools

- **XAMPP**: Local development environment
- **Git**: Version control
- **GitHub**: Repository hosting

## 📊 Screenshots

### Landing Page

Beautiful, modern landing page with system statistics and quick navigation.

### Mark Attendance

Intuitive interface for marking attendance with quick actions and real-time validation.

### Analytics Dashboard

Interactive charts with multiple visualization options (Bar, Line, Pie).

### Daily Reports

Comprehensive period-wise attendance view with summary statistics.

## 🔒 Security Features

- Input validation on all forms
- SQL injection prevention with parameterized queries
- Error handling and logging
- CORS configuration for API security

## 🐛 Troubleshooting

### Common Issues

**Issue**: Can't fetch students  
**Solution**: Ensure API server is running on port 5000

**Issue**: Database connection error  
**Solution**: Check if MySQL is running in XAMPP

**Issue**: Charts not displaying  
**Solution**: Check internet connection (Chart.js loads from CDN)

**Issue**: Port 5000 already in use  
**Solution**: Kill the process or change port in `api_server.py`

For more troubleshooting help, see [SETUP_GUIDE.md](SETUP_GUIDE.md)

## 📝 Usage

### Marking Attendance

1. Open `mark_attendance.html`
2. Select faculty (subject auto-fills)
3. Select period (1-5) and date
4. Mark Present/Absent/Late for each student
5. Use quick actions for bulk operations
6. Submit attendance

### Viewing Analytics

1. Open `analytics.html`
2. View overall statistics
3. Switch between chart types (Bar/Line/Pie)
4. Review detailed student-wise report
5. Check attendance percentages

### Daily Reports

1. Open `daily_report.html`
2. Select a date
3. Click "Load Report"
4. View period-wise attendance
5. Check summary statistics

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

**Abzana V**

- GitHub: [@Abz-05](https://github.com/Abz-05)
- Email: abzanavarhath@gmail.com

## 🙏 Acknowledgments

- Chart.js for beautiful visualizations
- Flask community for excellent documentation
- Inter font family for modern typography
- All contributors and testers

## 📞 Support

For issues, questions, or suggestions:

1. Check the [SETUP_GUIDE.md](SETUP_GUIDE.md)
2. Review [QUICK_START.md](QUICK_START.md)
3. Open an issue on GitHub
4. Contact via email

---

**Made with ❤️ for efficient attendance management**

⭐ Star this repo if you find it helpful!
