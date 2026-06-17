# AI39A - AI Based Smart Healthcare Assistant

## 📁 Folder Structure

```
vitapulse/
├── run.py                      ← Entry point
├── config.py                   ← Dev/Prod/Test config
├── requirements.txt
├── README.md
│
├── app/
│   ├── __init__.py             ← Application factory
│   ├── database.py             ← DB utility (DictCursor singleton)
│   ├── auth.py                 ← Decorators + password helpers
│   ├── helpers.py              ← BMR, BMI, date, validation utils
│   ├── constants.py            ← App-wide constants
│   │
│   ├── models/                 ← Database access layer
│   │   ├── base_model.py
│   │   ├── user.py
│   │   ├── calorie.py
│   │   ├── meal.py
│   │   ├── sleep.py
│   │   ├── mood.py
│   │   ├── expense.py
│   │   ├── workout.py
│   │   ├── medicine.py
│   │   ├── family.py
│   │   ├── health_risk.py
│   │   └── report.py
│   │
│   ├── controllers/            ← Business logic layer
│   │   ├── base_controller.py
│   │   ├── auth_controller.py
│   │   ├── dashboard_controller.py
│   │   ├── calorie_controller.py
│   │   ├── meal_controller.py
│   │   ├── sleep_controller.py
│   │   ├── mood_controller.py
│   │   ├── expense_controller.py
│   │   ├── ai_controller.py
│   │   ├── health_controller.py
│   │   └── admin_controller.py
│   │
│   ├── routes/                 ← URL → Controller mapping
│   │   ├── auth_routes.py
│   │   ├── dashboard_routes.py
│   │   ├── calorie_routes.py
│   │   ├── meal_routes.py
│   │   ├── sleep_routes.py
│   │   ├── mood_routes.py
│   │   ├── expense_routes.py
│   │   ├── ai_routes.py
│   │   ├── health_routes.py
│   │   └── admin_routes.py
│   │
│   ├── templates/
│   │   ├── base.html           ← Master layout
│   │   ├── dashboard_layout.html ← Sidebar layout
│   │   ├── index.html          ← Landing page
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── partials/           ← Reusable template fragments
│   │   ├── calorie/
│   │   ├── meals/
│   │   ├── sleep/
│   │   ├── mood/
│   │   ├── expense/
│   │   ├── ai/
│   │   ├── health/
│   │   ├── admin/
│   │   └── errors/             ← 403, 404, 500
│   │
│   └── static/
│       ├── css/                ← style.css, dashboard.css, auth.css…
│       ├── js/                 ← main.js, charts.js, chatbot.js…
│       ├── images/
│       └── uploads/
│
├── database/
│   ├── schema.sql              ← All CREATE TABLE statements
│   └── seed.sql                ← Demo data
│
└── docs/
    ├── architecture.md
    ├── api.md
    └── setup.md
```

---