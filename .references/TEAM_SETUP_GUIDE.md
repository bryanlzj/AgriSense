# 🚀 AgriSense - Team Setup Guide

Welcome to the AgriSense project! This guide will help you set up your local development environment after cloning the repository.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Backend Setup](#backend-setup)
4. [Frontend Setup](#frontend-setup)
5. [Running the Application](#running-the-application)
6. [Testing](#testing)
7. [Common Issues & Solutions](#common-issues--solutions)
8. [Next Steps](#next-steps)

---

## 🔧 Prerequisites

Before you begin, ensure you have the following installed on your machine:

### **Required Software:**

- **Git** (version 2.30+)
  - Download: https://git-scm.com/downloads
  - Verify: `git --version`

- **Python** (version 3.10 or 3.11)
  - Download: https://www.python.org/downloads/
  - Verify: `python --version` or `python3 --version`
  - ⚠️ **Important:** During installation, check "Add Python to PATH"

- **Code Editor** (Recommended: VS Code)
  - Download: https://code.visualstudio.com/

### **For Flutter Developer (Member 3) Only:**

- **Flutter SDK** (version 3.10+)
  - Download: https://docs.flutter.dev/get-started/install
  - Verify: `flutter --version`
  
- **Android Studio** (for Android development)
  - Download: https://developer.android.com/studio
  
- **Xcode** (for iOS development - macOS only)
  - Download from Mac App Store

### **Optional but Recommended:**

- **Postman** or **Insomnia** - For API testing
- **DB Browser for SQLite** - For viewing the database

---

## 📥 Initial Setup

### **1. Clone the Repository**

```bash
# Clone the repository
git clone <repository-url>

# Navigate to the project directory
cd AgriSense
```

### **2. Create Your Feature Branch**

```bash
# Create and switch to your feature branch
git checkout -b feature/your-name-feature-description

# Example:
# git checkout -b feature/bryan-ml-integration
# git checkout -b feature/sarah-flutter-auth
```

⚠️ **Important:** Never work directly on the `main` or `develop` branch!

### **3. Read the Documentation**

Before coding, familiarize yourself with:

- **`.references/TEAM_COLLABORATION_GUIDE.md`** - Team workflow and Git strategy
- **`.references/prd/agrisense-prd.md`** - Product requirements
- **`.references/tasks/agrisense-tasks.md`** - Task list and progress
- **`backend/API_DOCUMENTATION.md`** - Complete API reference

---

## 🐍 Backend Setup

### **Step 1: Navigate to Backend Directory**

```bash
cd backend
```

### **Step 2: Create Virtual Environment**

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

✅ **Success:** You should see `(venv)` at the beginning of your terminal prompt.

### **Step 3: Install Dependencies**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

⏱️ **Time:** ~2-3 minutes

### **Step 4: Set Up Environment Variables**

```bash
# Copy the example environment file
cp .env.example .env

# Windows (PowerShell):
# Copy-Item .env.example .env
```

**Edit `.env` file:**

```env
# Database
DATABASE_URL=sqlite:///./agrisense.db

# JWT Secret (generate a secure random string)
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=43200

# OpenWeatherMap API (get free key from https://openweathermap.org/api)
OPENWEATHER_API_KEY=your-api-key-here
```

🔑 **Get OpenWeatherMap API Key:**
1. Go to https://openweathermap.org/api
2. Sign up for free account
3. Generate API key (free tier is sufficient)
4. Add to `.env` file

### **Step 5: Initialize Database**

```bash
# Run database migrations
alembic upgrade head

# Seed the database with test data
python seed_database.py
```

✅ **Success:** You should see:
- Migration messages
- "Database seeded successfully!" message
- `agrisense.db` file created

### **Step 6: Verify Backend Setup**

```bash
# Run the backend server
python run.py
```

✅ **Success:** You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:5000
INFO:     Application startup complete.
```

**Test the API:**
1. Open browser: http://localhost:5000/docs
2. You should see Swagger UI with all API endpoints
3. Try the "GET /api/v1/health" endpoint

**Stop the server:** Press `Ctrl+C`

---

## 📱 Flutter Mobile App Setup (Member 3 Only)

> **Note:** The `frontend/` folder contains a React template from Evo Builder. **Ignore it completely** - it's not part of AgriSense.

### **For Member 3 (Flutter Developer):**

You will create a **new Flutter project** from scratch and integrate with the backend APIs.

**Steps:**

1. **Create Flutter Project:**
```bash
# Create new Flutter project (outside of AgriSense repo)
flutter create agrisense_mobile

# Or create inside a mobile/ folder in the repo
cd AgriSense
mkdir mobile
cd mobile
flutter create agrisense_mobile
```

2. **Backend API Integration:**
- **Backend API Base URL:** `http://localhost:5000` (local development)
- **API Documentation:** See `backend/API_DOCUMENTATION.md`
- **All endpoints:** Available at http://localhost:5000/docs (Swagger UI)

3. **Key Dependencies to Add:**
```yaml
dependencies:
  http: ^1.1.0              # For API calls
  provider: ^6.1.0          # State management
  shared_preferences: ^2.2.0 # Token storage
  image_picker: ^1.0.0      # Camera/gallery access
```

4. **Authentication Flow:**
- Store JWT token in SharedPreferences after login
- Include token in Authorization header for all API calls
- Handle token expiration (30 days)

---

## 🏃 Running the Application

### **Backend Server:**

```bash
# From backend directory with venv activated
cd backend
python run.py
```

**Access:**
- API: http://localhost:5000
- Swagger Docs: http://localhost:5000/docs
- ReDoc: http://localhost:5000/redoc

### **Flutter Mobile App (Member 3):**

```bash
# From your Flutter project directory
cd mobile/agrisense_mobile  # or wherever you created it
flutter run
```

**Note:** Make sure backend is running before testing the mobile app!

---

## 🧪 Testing

### **Run Backend Tests:**

```bash
# From backend directory with venv activated
cd backend

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_auth.py

# Run with coverage report
pytest --cov=backend --cov-report=html
```

✅ **Expected:** 55+ tests should pass

**View coverage report:**
- Open `backend/htmlcov/index.html` in browser

### **Test Individual Endpoints:**

**Option 1: Using Swagger UI**
1. Go to http://localhost:5000/docs
2. Click on any endpoint
3. Click "Try it out"
4. Fill in parameters
5. Click "Execute"

**Option 2: Using curl**

```bash
# Register a user
curl -X POST "http://localhost:5000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123","full_name":"Test User"}'

# Login
curl -X POST "http://localhost:5000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=password123"
```

**Option 3: Using Postman/Insomnia**
- Import the API endpoints from Swagger
- Test each endpoint manually

---

## ❌ Common Issues & Solutions

### **Issue 1: "python: command not found"**

**Solution:**
```bash
# Try python3 instead
python3 --version

# Or add Python to PATH (Windows)
# Reinstall Python and check "Add Python to PATH"
```

### **Issue 2: "venv\Scripts\Activate.ps1 cannot be loaded"**

**Solution (Windows PowerShell):**
```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try activating again
.\venv\Scripts\Activate.ps1
```

### **Issue 3: "ModuleNotFoundError: No module named 'X'"**

**Solution:**
```bash
# Ensure venv is activated (you should see (venv) in prompt)
# Reinstall dependencies
pip install -r requirements.txt
```

### **Issue 4: "Address already in use" (Port 5000)**

**Solution:**

**Windows:**
```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

**macOS/Linux:**
```bash
# Find and kill process
lsof -ti:5000 | xargs kill -9
```

### **Issue 5: Database errors after pulling new code**

**Solution:**
```bash
# Delete the database
rm agrisense.db  # or delete manually

# Re-run migrations and seed
alembic upgrade head
python seed_database.py
```

### **Issue 6: "alembic: command not found"**

**Solution:**
```bash
# Ensure venv is activated
# Reinstall alembic
pip install alembic
```

### **Issue 7: Tests failing with import errors**

**Solution:**
```bash
# From backend directory
cd backend

# Ensure you're in the backend directory when running tests
pytest
```

---

## 🎯 Next Steps

### **For All Team Members:**

1. ✅ Complete this setup guide
2. ✅ Verify backend runs successfully
3. ✅ Read `.references/TEAM_COLLABORATION_GUIDE.md`
4. ✅ Review your assigned tasks in `.references/tasks/agrisense-tasks.md`
5. ✅ Join team communication channels (Slack/Discord)
6. ✅ Attend first team meeting

### **For Member 2 (Backend Developer):**

**Your Focus:** ML Integration & Backend Enhancements

**Start Here:**
1. Review `backend/routers/pest.py` - Current mock ML implementation
2. Review `backend/services/alert_service.py` - Alert generation logic
3. Coordinate with Members 4 & 5 on ML model API contract
4. Read `backend/API_DOCUMENTATION.md` - Understand all endpoints

**Key Files:**
```
backend/
├── routers/pest.py          # Pest detection endpoints (mock ML)
├── services/alert_service.py # Alert generation logic
├── utils/image_validator.py  # Image validation
└── utils/file_storage.py     # File upload utilities
```

**First Tasks:**
- Understand current pest detection flow
- Plan ML model integration approach
- Discuss API contract with ML team

### **For Member 3 (Flutter Developer):**

**Your Focus:** Mobile App Development

**Start Here:**
1. Review `backend/API_DOCUMENTATION.md` - All available APIs
2. Test APIs using Swagger UI (http://localhost:5000/docs)
3. Plan Flutter app architecture
4. Set up Flutter project

**API Endpoints You'll Use:**
```
Authentication:
- POST /api/v1/auth/register
- POST /api/v1/auth/login
- GET /api/v1/auth/me

Sensor Data:
- GET /api/v1/sensor/
- POST /api/v1/sensor/
- GET /api/v1/sensor/stats/summary

Pest Detection:
- POST /api/v1/pest/detect (with image upload)
- GET /api/v1/pest/
- GET /api/v1/pest/stats/summary

Weather:
- GET /api/v1/weather/summary
- GET /api/v1/weather/forecast

Alerts:
- GET /api/v1/alert/
- PUT /api/v1/alert/{id}
- GET /api/v1/alert/stats/summary
```

**First Tasks:**
- Create Flutter project structure
- Implement authentication screens
- Set up HTTP client for API calls
- Implement token storage

### **For Members 4 & 5 (ML Engineers):**

**Your Focus:** Pest Detection Model

**Start Here:**
1. Review `backend/routers/pest.py` - See expected input/output format
2. Research pest detection datasets
3. Plan model architecture
4. Set up training environment

**Expected Model API Contract:**

**Input:**
- Image file (JPEG/PNG)
- Min size: 224x224 pixels
- Max size: 5MB

**Output:**
```json
{
  "pest_type": "Fall Armyworm",
  "confidence": 0.87,
  "severity": "high",
  "recommendations": [
    "Apply appropriate pesticide",
    "Monitor surrounding crops"
  ]
}
```

**First Tasks:**
- Dataset collection and labeling
- Baseline model experiments
- Document findings
- Coordinate with Member 2 on integration

---

## 📚 Additional Resources

### **Documentation:**
- **Product Requirements:** `.references/prd/agrisense-prd.md`
- **Task List:** `.references/tasks/agrisense-tasks.md`
- **API Documentation:** `backend/API_DOCUMENTATION.md`
- **Team Workflow:** `.references/TEAM_COLLABORATION_GUIDE.md`

### **External Resources:**
- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **Flutter Docs:** https://flutter.dev/docs
- **SQLAlchemy Docs:** https://docs.sqlalchemy.org/
- **Alembic Docs:** https://alembic.sqlalchemy.org/

### **Useful Commands:**

```bash
# Git workflow
git status                    # Check current status
git add .                     # Stage all changes
git commit -m "message"       # Commit changes
git push origin branch-name   # Push to remote
git pull origin develop       # Pull latest changes

# Backend
cd backend
source venv/bin/activate      # Activate venv (macOS/Linux)
.\venv\Scripts\Activate.ps1   # Activate venv (Windows)
python run.py                 # Start server
pytest                        # Run tests
alembic upgrade head          # Run migrations

# Database
python seed_database.py       # Seed test data
alembic revision --autogenerate -m "message"  # Create migration

# Flutter (Member 3 only)
flutter doctor               # Check Flutter installation
flutter create project_name  # Create new Flutter project
flutter run                  # Run on connected device/emulator
flutter build apk            # Build Android APK
```

---

## 🆘 Getting Help

### **If You're Stuck:**

1. **Check this guide** - Most common issues are covered
2. **Check documentation** - `.references/` folder has detailed info
3. **Ask in team chat** - Your teammates might have faced the same issue
4. **Check error messages** - Read them carefully, they often tell you what's wrong
5. **Google the error** - Include "FastAPI" or "Python" in your search
6. **Ask team lead** - Don't stay stuck for more than 30 minutes

### **Team Communication:**

- **Daily Standups:** [Time TBD] - Share progress and blockers
- **Weekly Sync:** [Time TBD] - Review progress and plan next week
- **Chat Channel:** [Platform TBD] - Quick questions and updates
- **Code Reviews:** GitHub Pull Requests - Review each other's code

---

## ✅ Setup Checklist

Use this checklist to verify your setup is complete:

### **Environment Setup:**
- [ ] Git installed and configured
- [ ] Python 3.10+ installed
- [ ] Flutter SDK installed (Member 3 only)
- [ ] VS Code or preferred editor installed
- [ ] Repository cloned successfully

### **Backend Setup:**
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created and configured
- [ ] OpenWeatherMap API key obtained and added
- [ ] Database migrations run (`alembic upgrade head`)
- [ ] Database seeded (`python seed_database.py`)
- [ ] Backend server runs successfully (`python run.py`)
- [ ] Swagger UI accessible (http://localhost:5000/docs)
- [ ] Tests pass (`pytest`)

### **Documentation Review:**
- [ ] Read `TEAM_COLLABORATION_GUIDE.md`
- [ ] Read `agrisense-prd.md` (Product Requirements)
- [ ] Read `agrisense-tasks.md` (Task List)
- [ ] Read `API_DOCUMENTATION.md` (if working with APIs)
- [ ] Reviewed assigned tasks

### **Git Workflow:**
- [ ] Created feature branch
- [ ] Understand branching strategy
- [ ] Know how to create Pull Requests

### **Team Communication:**
- [ ] Joined team communication channel
- [ ] Know daily standup time
- [ ] Know weekly sync meeting time
- [ ] Have team lead contact info

---

## 🎉 You're Ready!

Congratulations! Your development environment is now set up and you're ready to start contributing to AgriSense.

**Remember:**
- 💬 Communicate with your team
- 📝 Follow the Git workflow
- 🧪 Test your code before pushing
- 📖 Read documentation when unsure
- 🆘 Ask for help when stuck

**Happy coding! 🚀**

---

**Last Updated:** January 2025  
**Project Status:** Backend 97.7% complete (60/88 tasks)  
**Current Phase:** Phase 1 - Backend Development (almost complete)
