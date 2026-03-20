# 🏢 HR Onboarding Dashboard

A comprehensive web-based HR onboarding system built with Flask, featuring employee management, task tracking, policy acknowledgment, training programs, and HR analytics.

## 🌟 Live Demo

**🚀 [View Live Demo](https://your-hr-dashboard.herokuapp.com)**

**Login Credentials:**
- Username: `admin`
- Password: `admin123`

## 📊 Features

### 🎯 **Core Functionality**
- **Employee Management** - Complete onboarding workflow for new hires
- **Task Tracking** - Assign and monitor onboarding tasks
- **Policy Management** - Digital policy acknowledgment system
- **Training Programs** - Track training completion and progress
- **Notification System** - Automated welcome messages and updates
- **KPI Dashboard** - Performance metrics and analytics

### 📈 **HR Analytics**
- **HR Dataset** - 3,400 historical employee records
- **Department Analytics** - Performance breakdown by department
- **Position Analysis** - Complete job role statistics
- **Attrition Tracking** - Employee retention insights
- **Satisfaction Metrics** - Job satisfaction and performance data

### 👥 **Sample Data Included**
- **16 Active Employees** across 5 departments
- **104 Onboarding Tasks** with realistic completion rates
- **45 Policy Assignments** with acknowledgment tracking
- **45 Training Programs** with progress monitoring
- **15 Notifications** with read/unread status

## 🏗️ **System Architecture**

### **Backend**
- **Flask** - Python web framework
- **SQLite** - Database (production-ready)
- **Gunicorn** - WSGI HTTP Server

### **Frontend**
- **Bootstrap 5** - Responsive UI framework
- **Bootstrap Icons** - Icon library
- **Responsive Design** - Mobile-friendly interface

### **Data Management**
- **CSV Import** - Bulk data import functionality
- **Real-time Updates** - Dynamic dashboard updates
- **Data Validation** - Input validation and error handling

## 📱 **Screenshots**

### Dashboard Overview
![Dashboard](https://via.placeholder.com/800x400?text=HR+Dashboard+Overview)

### Employee Management
![Employees](https://via.placeholder.com/800x400?text=Employee+Management)

### HR Dataset Analytics
![Analytics](https://via.placeholder.com/800x400?text=HR+Analytics)

## 🚀 **Deployment Options**

### **1. Heroku (Recommended)**
```bash
# Quick deploy
git clone <repository>
cd hr_onboarding_flask
./deploy_heroku.bat  # Windows
./deploy_heroku.sh   # Linux/Mac
```

### **2. Railway**
```bash
npm install -g @railway/cli
railway login
railway init
railway up
```

### **3. Render**
1. Connect your GitHub repository
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `gunicorn app:app`

## 🔧 **Local Development**

### **Prerequisites**
- Python 3.11+
- pip package manager

### **Setup**
```bash
# Clone repository
git clone <repository>
cd hr_onboarding_flask

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

### **Access Application**
- Open browser: `http://127.0.0.1:5000`
- Login: `admin` / `admin123`

## 📊 **Data Overview**

### **HR Dataset Statistics**
- **Total Records**: 3,400 employees
- **Departments**: Sales, Marketing, Finance, IT, HR
- **Average Age**: 38.4 years
- **Average Income**: $5,125/month
- **Attrition Rate**: 50.7%

### **Active Employees by Department**
- **Finance**: 3 employees (Analyst, Accountant, Budget Analyst)
- **HR**: 3 employees (Manager, Recruiter, Training Coordinator)
- **IT**: 3 employees (Software Engineer, DevOps Engineer, Data Scientist)
- **Marketing**: 3 employees (Specialist, Content Manager, Digital Marketing Manager)
- **Sales**: 3 employees (Representative, Account Manager, Regional Manager)
- **Front Office**: 1 employee (Receptionist)

### **Task Completion Rates**
- **Total Tasks**: 104
- **Completed**: 30 (28.8%)
- **Pending**: 53 (51.0%)
- **Not Started**: 21 (20.2%)

## 🔐 **Security Features**

- **Session Management** - Secure user sessions
- **Input Validation** - SQL injection prevention
- **Environment Variables** - Secure configuration management
- **Production Settings** - Debug mode disabled in production

## 🛠️ **Technical Specifications**

### **Database Schema**
- **users** - Authentication and authorization
- **employees** - Active employee records
- **hr_data** - Historical HR dataset
- **tasks** - Onboarding task management
- **policies** - Policy acknowledgment tracking
- **training** - Training program management
- **notifications** - System notifications
- **kpi** - Key performance indicators

### **API Endpoints**
- `/dashboard` - Main dashboard
- `/hr_data` - HR dataset analytics
- `/employee/<id>` - Employee details
- `/checklist/<id>` - Task management
- `/policy/<id>` - Policy acknowledgment
- `/training/<id>` - Training programs
- `/notifications` - Notification center
- `/kpi` - KPI dashboard

## 📈 **Performance Metrics**

- **Page Load Time**: < 2 seconds
- **Database Queries**: Optimized with indexing
- **Responsive Design**: Mobile-first approach
- **Browser Support**: Chrome, Firefox, Safari, Edge

## 🤝 **Contributing**

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 **Support**

For support and questions:
- 📧 Email: support@hr-dashboard.com
- 📱 GitHub Issues: [Create Issue](https://github.com/your-repo/issues)
- 📖 Documentation: [Wiki](https://github.com/your-repo/wiki)

## 🎯 **Roadmap**

### **Upcoming Features**
- [ ] Email notifications
- [ ] Advanced reporting
- [ ] Mobile app
- [ ] API integration
- [ ] Multi-language support
- [ ] Advanced analytics
- [ ] Document management
- [ ] Calendar integration

---

**Built with ❤️ for HR professionals worldwide**

🌐 **[Live Demo](https://your-hr-dashboard.herokuapp.com)** | 📚 **[Documentation](https://github.com/your-repo/wiki)** | 🐛 **[Report Bug](https://github.com/your-repo/issues)**