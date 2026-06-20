# 🩺 VitaPulse – AI-Based Smart Healthcare Assistant

VitaPulse is an AI-powered healthcare and wellness platform designed to help users monitor and improve their overall well-being. The system combines health tracking, nutrition monitoring, sleep analysis, mood tracking, expense management, medication management, and AI-powered health assistance into a single platform.

The application is built using Flask, MySQL, HTML/CSS/JavaScript, Google OAuth, and Groq AI.

---

# ✨ Features

## 👤 User Management

* User Registration
* User Login
* Google OAuth Login
* Profile Management
* Session Authentication

## 🍎 Nutrition Tracking

* Calorie Tracking
* Meal Logging
* Nutrition Monitoring

## 🏃 Fitness Tracking

* Workout Tracking
* Activity Monitoring
* Progress Tracking

## 😴 Sleep Tracking

* Sleep Duration Logging
* Sleep Quality Monitoring
* Sleep Reports

## 😊 Mood Tracking

* Daily Mood Logging
* Mood Analytics

## 💊 Medicine Management

* Medicine Tracking
* Reminder Management

## 👨‍👩‍👧 Family Health Management

* Family Member Records
* Shared Health Monitoring

## 📊 Health Analytics

* BMI Calculation
* BMR Calculation
* Health Risk Assessment
* Personalized Recommendations

## 🤖 AI Health Assistant

* Groq AI Integration
* Health Chatbot
* Personalized Guidance

## 📄 Reports

* PDF Report Generation
* Health Summary Reports

## 👨‍💼 Admin Dashboard

* User Management
* System Monitoring
* Analytics Dashboard

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

# 📁 Project Structure

```text
vitapulse/
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

# ✅ Prerequisites

Before running the project, install the following software:

* Python 3.9 or higher
* MySQL 8.0 or higher
* Git

Verify installation:

```bash
python --version
mysql --version
git --version
```

---

# 🚀 Installation

## Step 1: Clone Repository

```bash
git clone https://github.com/your-username/vitapulse.git
cd vitapulse
```

---

## Step 2: Create Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ⚙️ Environment Configuration

Rename:

```text
.env.example → .env
```

Open `.env` and update:

```env
# Flask
FLASK_ENV=development
SECRET_KEY=your-secret-key

# Database
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=vitapulse_db

# Google OAuth
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=http://localhost:5000/auth/google/callback

# Groq AI
GROQ_API_KEY=
```

## Environment Variables

| Variable             | Description                |
| -------------------- | -------------------------- |
| FLASK_ENV            | Flask environment          |
| SECRET_KEY           | Application secret key     |
| DB_HOST              | MySQL host                 |
| DB_PORT              | MySQL port                 |
| DB_USER              | MySQL username             |
| DB_PASSWORD          | MySQL password             |
| DB_NAME              | Database name              |
| GOOGLE_CLIENT_ID     | Google OAuth Client ID     |
| GOOGLE_CLIENT_SECRET | Google OAuth Client Secret |
| GROQ_API_KEY         | Groq AI API Key            |

---

# 🗄️ Database Setup

## Start MySQL

Ensure MySQL service is running.

---

## Login to MySQL

```bash
mysql -u root -p
```

Enter your MySQL password.

---

## Create Database

```sql
CREATE DATABASE vitapulse_db;
SHOW DATABASES;
```

Exit MySQL:

```sql
EXIT;
```

---

## Import Schema

### Windows PowerShell

```powershell
Get-Content .\database\schema.sql | mysql -u root -p vitapulse_db
```

### Windows CMD / Linux / macOS

```bash
mysql -u root -p vitapulse_db < database/schema.sql
```

---

## Import Sample Data (Optional)

```bash
mysql -u root -p vitapulse_db < database/seed.sql
```

---

## Verify Database

Login again:

```bash
mysql -u root -p
```

Select database:

```sql
USE vitapulse_db;
```

View tables:

```sql
SHOW TABLES;
```

---

# 🔑 Google OAuth Setup

1. Open Google Cloud Console.
2. Create a new project.
3. Go to APIs & Services → Credentials.
4. Click Create Credentials.
5. Select OAuth Client ID.
6. Choose Web Application.
7. Add the following Redirect URI:

```text
http://localhost:5000/auth/google/callback
```

8. Click Create.
9. Copy Client ID.
10. Copy Client Secret.
11. Paste both into `.env`.

Example:

```env
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
```

---

# 🤖 Groq API Setup

1. Create a Groq account.
2. Navigate to API Keys.
3. Generate a new API key.
4. Copy the key.
5. Paste into `.env`.

Example:

```env
GROQ_API_KEY=your_api_key_here
```

---

# ▶️ Running the Application

Activate virtual environment first:

```bash
venv\Scripts\activate
```

Run the application:

```bash
python run.py
```

Expected output:

```text
* Running on http://127.0.0.1:5000
```

Open:

```text
http://localhost:5000
```

in your browser.

---

# 🧪 Running Tests

Install pytest if needed:

```bash
python -m pip install pytest
```

Verify installation:

```bash
python -m pytest --version
```

Run all tests:

```bash
python -m pytest -v
```

Run a specific test file:

```bash
python -m pytest tests/test_auth.py -v
```

Example successful output:

```text
=====================
3 passed
=====================
```

---

# 🐞 Troubleshooting

## Database Not Found

Error:

```text
ERROR 1049 (42000):
Unknown database 'vitapulse_db'
```

Solution:

```sql
CREATE DATABASE vitapulse_db;
```

---

## Pytest Not Found

Error:

```text
No module named pytest
```

Solution:

```bash
python -m pip install pytest
```

---

## MySQL Connection Failed

Check:

* MySQL service is running
* Database exists
* Credentials in `.env` are correct

---

## Google OAuth Error

Verify callback URL exactly matches:

```text
http://localhost:5000/auth/google/callback
```

---

## Port Already In Use

Change port in `run.py`:

```python
app.run(port=5001)
```

---

# 🔒 Security Notes

* Never commit `.env` to GitHub.
* Keep API keys private.
* Store secrets only in environment variables.
* Use strong passwords for MySQL and OAuth accounts.

---

# 🚀 Future Enhancements

* Mobile Application
* Wearable Device Integration
* AI Health Prediction
* Voice Assistant Support
* Doctor Consultation Module
* Multi-language Support

---

# 👨‍💻 Development Team

AI39A – AI-Based Smart Healthcare Assistant

VitaPulse Development Team

2026

---

# 📜 License

This project is developed for educational and academic purposes.

© 2026 VitaPulse Team

---

# ❤️ VitaPulse

Track Smarter. Live Healthier. Stay Connected.
