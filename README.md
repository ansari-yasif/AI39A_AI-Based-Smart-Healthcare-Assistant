# 🩺 VitaPulse – AI-Based Smart Healthcare Assistant

<p align="center">
  <img src="https://img.shields.io/badge/Flask-Python-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/MySQL-Database-orange?style=for-the-badge">
  <img src="https://img.shields.io/badge/Groq-AI-green?style=for-the-badge">
  <img src="https://img.shields.io/badge/Google-OAuth-red?style=for-the-badge">
</p>

## 🌟 Overview

**VitaPulse** is an AI-powered Smart Healthcare Assistant designed to help users maintain a healthier lifestyle through intelligent health tracking and personalized insights.

The platform combines nutrition monitoring, fitness tracking, sleep analysis, mood tracking, expense management, medication reminders, and AI-powered health assistance into a single integrated wellness ecosystem.

Users can interact with an intelligent chatbot powered by Groq AI to receive personalized recommendations and wellness guidance.

---

## ✨ Key Features

### 👤 User Management

* Secure Registration & Login
* Google OAuth Authentication
* Profile Management
* Session-Based Authentication

### 🍎 Nutrition Tracking

* Daily Calorie Tracking
* Meal Logging
* Nutritional Analysis
* Calorie History

### 🏃 Fitness Monitoring

* Workout Tracking
* Activity Management
* Progress Monitoring
* Health Metrics Calculation

### 😴 Sleep Monitoring

* Sleep Duration Tracking
* Sleep Quality Analysis
* Historical Sleep Reports

### 😊 Mood Tracking

* Daily Mood Logging
* Mood Analytics
* Wellness Monitoring

### 💊 Medicine Management

* Medication Tracking
* Reminder Support
* Medical History Storage

### 👨‍👩‍👧 Family Health

* Family Member Management
* Shared Health Records
* Family Wellness Monitoring

### 📊 Health Analytics

* BMI Calculation
* BMR Calculation
* Health Risk Assessment
* Personalized Insights

### 🤖 AI Health Assistant

* Groq AI Integration
* Natural Language Conversations
* Personalized Recommendations
* Health Guidance

### 📄 Reporting System

* PDF Report Generation
* Health Summary Reports
* Progress Analytics

### 👨‍💼 Admin Dashboard

* User Management
* System Monitoring
* Data Analytics
* Administrative Controls

---

# 🏗️ System Architecture

```text
Frontend (HTML/CSS/JS)
         │
         ▼
Flask Routes
         │
         ▼
Controllers (Business Logic)
         │
         ▼
Models (Database Layer)
         │
         ▼
MySQL Database
```

---

# 📁 Project Structure

```text
vitapulse/
│
├── run.py
├── config.py
├── requirements.txt
├── README.md
│
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── auth.py
│   ├── helpers.py
│   ├── constants.py
│   │
│   ├── models/
│   ├── controllers/
│   ├── routes/
│   ├── templates/
│   └── static/
│
├── database/
│   ├── schema.sql
│   └── seed.sql
│
└── tests/
```

---

# 🛠️ Technology Stack

## Backend

* Python 3.9+
* Flask
* PyMySQL

## Frontend

* HTML5
* CSS3
* JavaScript
* Chart.js
* Lucide Icons

## Authentication

* Google OAuth
* Authlib

## Database

* MySQL

## AI Integration

* Groq API

## Additional Libraries

* ReportLab
* python-dotenv
* cryptography

---

# 🚀 Installation Guide

## 1. Clone Repository

```bash
git clone https://github.com/your-username/vitapulse.git
cd vitapulse
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Rename:

```bash
.env.example → .env
```

Update:

```env
# Flask
FLASK_ENV=development
SECRET_KEY=your-secret-key

# Database
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=vitapulse_db

# Google OAuth
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=http://localhost:5000/auth/google/callback

# Groq AI
GROQ_API_KEY=
```

---

# 🗄️ Database Setup

## Login to MySQL

```bash
mysql -u root -p
```

## Create Database

```sql
CREATE DATABASE vitapulse_db;
```

## Import Schema

### Windows PowerShell

```powershell
Get-Content .\database\schema.sql | mysql -u root -p vitapulse_db
```

### CMD / Linux / macOS

```bash
mysql -u root -p vitapulse_db < database/schema.sql
```

## Import Sample Data (Optional)

```bash
mysql -u root -p vitapulse_db < database/seed.sql
```

---

# ▶️ Run Application

```bash
python run.py
```

Server starts at:

```text
http://localhost:5000
```

---

# 🔑 API Configuration

## Google OAuth Setup

1. Open Google Cloud Console
2. Create Project
3. Go to APIs & Services → Credentials
4. Create OAuth Client ID
5. Select Web Application
6. Add Redirect URI:

```text
http://localhost:5000/auth/google/callback
```

7. Copy credentials into `.env`

---

## Groq API Setup

1. Create a Groq account
2. Generate an API Key
3. Add it to `.env`

```env
GROQ_API_KEY=your_api_key_here
```

---

# 📊 Core Modules

| Module         | Description             |
| -------------- | ----------------------- |
| Authentication | Login, Register, OAuth  |
| Dashboard      | User Overview           |
| Calories       | Nutrition Tracking      |
| Meals          | Food Logging            |
| Sleep          | Sleep Monitoring        |
| Mood           | Mood Tracking           |
| Workout        | Exercise Tracking       |
| Expense        | Health Expense Tracking |
| Medicine       | Medication Management   |
| AI Assistant   | Health Chatbot          |
| Reports        | PDF Generation          |
| Admin          | System Administration   |

---

# 🧪 Testing

Run all tests:

```bash
pytest
```

Run a specific test:

```bash
pytest tests/test_auth_controller.py
```

---


# 🔒 Security Features

* Password Hashing
* Environment Variables
* Session Protection
* OAuth Authentication
* Secure Database Access
* Input Validation

---

# 🐞 Troubleshooting

### Database Not Found

```text
ERROR 1049 (42000):
Unknown database 'vitapulse_db'
```

Solution:

```sql
CREATE DATABASE vitapulse_db;
```

---

### MySQL Connection Failed

Verify:

* MySQL service is running
* Credentials in `.env` are correct
* Database exists

---

### OAuth Error

Ensure the callback URL exactly matches:

```text
http://localhost:5000/auth/google/callback
```

---

### Port Already In Use

Change port in:

```python
app.run(port=5001)
```

---

# 🎯 Future Enhancements

* Mobile Application
* Wearable Device Integration
* AI Health Prediction
* Voice Assistant Support
* Doctor Consultation Module
* Health Goal Recommendations
* Multi-language Support

---

# 👨‍💻 Development Team

**AI39A – AI Based Smart Healthcare Assistant**

VitaPulse Development Team

2026

---

# 📜 License

This project is developed for educational and academic purposes.

© 2026 VitaPulse Team

---

# ❤️ Empowering Better Health Through AI

"Track Smarter. Live Healthier. Stay Connected."
