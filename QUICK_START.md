# 🚀 Quick Start Guide - Attendance Management System

## ⚡ Start the System (3 Steps)

### 1️⃣ Start XAMPP Services

```
Open XAMPP Control Panel
✅ Start Apache
✅ Start MySQL
```

### 2️⃣ Start API Server

```powershell
cd "C:\Xammp\htdocs\Attendance management System"
python api_server.py
```

**Keep this terminal open!**

### 3️⃣ Open Application

```
file:///C:/Xammp/htdocs/Attendance%20management%20System/index.html
```

---

## 📱 Application Pages

| Page                   | URL                    | Purpose                     |
| ---------------------- | ---------------------- | --------------------------- |
| 🏠 **Home**            | `index.html`           | Main dashboard & navigation |
| 📝 **Mark Attendance** | `mark_attendance.html` | Mark period-wise attendance |
| 📊 **Analytics**       | `analytics.html`       | View charts & statistics    |
| 📅 **Daily Reports**   | `daily_report.html`    | Period-wise daily reports   |

---

## 🎯 Quick Actions

### Mark Attendance

1. Select Faculty → Subject auto-fills
2. Select Period (1-5)
3. Select Date
4. Click status for each student (Present/Absent/Late)
5. Submit

**Quick Buttons:**

- ✅ Mark All Present
- ❌ Mark All Absent
- 🔄 Clear All

### View Analytics

- Switch between Bar/Line/Pie charts
- View overall attendance percentages
- See detailed student-wise reports

### Daily Reports

- Select any date
- View period-wise attendance
- See summary statistics

---

## 🔧 Troubleshooting

| Issue                   | Solution                                       |
| ----------------------- | ---------------------------------------------- |
| ❌ Can't fetch students | Check if API server is running on port 5000    |
| ❌ Database error       | Ensure MySQL is running in XAMPP               |
| ❌ Charts not showing   | Check internet connection (Chart.js CDN)       |
| ❌ Port 5000 in use     | Kill process or change port in `api_server.py` |

---

## 📊 System Info

- **Students**: 23 (C3S48851 to C3S48874)
- **Faculty**: 4 (Ratchana B, S. Karthiga, DSP, Maniram)
- **Subjects**: 5 (ML, BDA, CN, SDA, SDA Lab)
- **Periods**: 5 per day
- **Database**: MySQL (attendance_system)
- **API**: Flask (Port 5000)

---

## 🕐 Period Timings

| Period    | Time          |
| --------- | ------------- |
| 1         | 09:00 - 09:50 |
| 2         | 09:50 - 10:40 |
| **Break** | 10:40 - 11:00 |
| 3         | 11:00 - 11:50 |
| 4         | 11:50 - 12:40 |
| **Lunch** | 12:40 - 13:30 |
| 5         | 13:30 - 15:10 |

---

## 🎨 Features

✅ Modern, responsive UI  
✅ Real-time data updates  
✅ Interactive charts (Bar, Line, Pie)  
✅ Period-wise tracking  
✅ Quick bulk actions  
✅ Date filtering  
✅ Detailed analytics  
✅ Beautiful design with gradients & animations

---

## 📞 API Endpoints

```
GET  /api/health          - Health check
GET  /api/students        - Get all students
GET  /api/faculty         - Get all faculty
POST /api/attendance/mark - Mark attendance
GET  /api/attendance/daily - Daily report
GET  /api/attendance/analytics - Analytics data
POST /api/student/add     - Add new student
GET  /api/periods         - Period timings
```

---

**Ready to use! 🎉**

For detailed documentation, see `SETUP_GUIDE.md`
