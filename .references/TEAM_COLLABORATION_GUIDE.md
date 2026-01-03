# AgriSense Team Collaboration Guide

**Project:** AgriSense - Smart Agriculture Mobile Application  
**Team Size:** 5 Members  
**Duration:** 14 Weeks  
**Last Updated:** January 4, 2026

---

## 📋 Table of Contents

1. [Team Structure](#team-structure)
2. [Project Architecture](#project-architecture)
3. [Role Breakdown](#role-breakdown)
4. [Git Workflow](#git-workflow)
5. [Communication & Coordination](#communication--coordination)
6. [API Contract](#api-contract)
7. [ML Integration](#ml-integration)
8. [Timeline & Milestones](#timeline--milestones)
9. [Tools for Collaboration](#tools-for-collaboration)
10. [First Team Meeting Agenda](#first-team-meeting-agenda)
11. [Best Practices](#best-practices)

---

## 👥 Team Structure

### Team Composition

```
┌─────────────────────────────────────────────────────────┐
│  AgriSense Development Team (5 Members)                 │
└─────────────────────────────────────────────────────────┘

👤 Member 1: Backend Lead + DevOps
👤 Member 2: Backend Developer + API Integration
👤 Member 3: Flutter/Mobile Developer
👤 Member 4: ML Engineer - Model Development
👤 Member 5: ML Engineer - Model Training & Optimization
```

### Team Responsibilities Matrix

| Member | Primary Role | Secondary Role | Key Deliverables |
|--------|-------------|----------------|------------------|
| **Member 1** | Backend Lead | DevOps & Deployment | Auth system, Alerts, Weather API, Server setup |
| **Member 2** | Backend Developer | ML Integration | Sensor API, Pest API, ML model integration |
| **Member 3** | Flutter Developer | UI/UX Design | Mobile app (all screens), API integration |
| **Member 4** | ML Engineer | Data Collection | Model architecture, Experiments, Dataset |
| **Member 5** | ML Engineer | Model Deployment | Training pipeline, Model optimization, API |

---

## 🏗️ Project Architecture

### Directory Structure

```
AgriSense/
│
├── 📱 FRONTEND (Member 3)
│   └── mobile/
│       ├── lib/
│       │   ├── screens/
│       │   │   ├── auth/
│       │   │   ├── dashboard/
│       │   │   ├── sensors/
│       │   │   ├── pests/
│       │   │   └── alerts/
│       │   ├── services/
│       │   │   ├── auth_service.dart
│       │   │   ├── sensor_service.dart
│       │   │   ├── pest_service.dart
│       │   │   └── alert_service.dart
│       │   ├── widgets/
│       │   └── models/
│       ├── assets/
│       └── pubspec.yaml
│
├── 🔧 BACKEND (Members 1 & 2)
│   └── backend/
│       ├── main.py
│       ├── database.py
│       ├── config.py
│       ├── routers/
│       │   ├── auth.py          ← Member 1
│       │   ├── sensors.py       ← Member 2
│       │   ├── pests.py         ← Member 2
│       │   ├── alerts.py        ← Member 1
│       │   └── weather.py       ← Member 1
│       ├── models/
│       │   ├── user.py
│       │   ├── sensor_reading.py
│       │   ├── pest_detection.py
│       │   └── alert.py
│       ├── schemas/
│       │   ├── auth.py          ← Member 1
│       │   ├── sensor.py        ← Member 2
│       │   ├── pest.py          ← Member 2
│       │   └── alert.py         ← Member 1
│       ├── utils/
│       │   ├── jwt.py           ← Member 1
│       │   ├── password.py
│       │   ├── ml_integration.py ← Member 2
│       │   └── weather_api.py   ← Member 1
│       └── tests/
│
└── 🤖 MACHINE LEARNING (Members 4 & 5)
    └── ml/
        ├── notebooks/           ← Member 4 (Experiments)
        │   ├── 01_data_exploration.ipynb
        │   ├── 02_model_experiments.ipynb
        │   └── 03_results_analysis.ipynb
        ├── datasets/            ← Both
        │   ├── raw/
        │   ├── processed/
        │   └── labels.csv
        ├── models/              ← Member 4
        │   ├── baseline_model.py
        │   ├── cnn_model.py
        │   └── transfer_learning.py
        ├── training/            ← Member 5
        │   ├── train.py
        │   ├── evaluate.py
        │   └── config.yaml
        └── api/                 ← Both (integrate with backend)
            ├── inference.py
            ├── model_loader.py
            └── preprocessing.py
```

---

## 📋 Role Breakdown

### 👤 Member 1: Backend Lead + DevOps

**Primary Responsibilities:**
- ✅ Backend architecture and setup (COMPLETE)
- ✅ Database design and migrations (COMPLETE)
- ✅ Authentication system (JWT, login, register)
- ✅ Alert system API
- ✅ Weather integration (OpenWeatherMap)
- ✅ Deployment and server management
- ✅ API documentation
- ✅ Code reviews for backend

**Tasks Breakdown:**

#### Week 3-4: Authentication System (Task 1.1)
```
├── 1.1.1: Install JWT dependencies
│   - Add python-jose[cryptography]
│   - Update requirements.txt
│
├── 1.1.2: Create JWT utilities
│   - Create utils/jwt.py
│   - Implement create_access_token()
│   - Implement verify_token()
│
├── 1.1.3: Create auth dependencies
│   - Implement get_current_user()
│   - Implement get_current_active_user()
│
├── 1.1.4: Create Pydantic schemas
│   - Create schemas/auth.py
│   - UserCreate, UserLogin, UserResponse, Token
│
└── 1.1.5: Create auth router
    - Create routers/auth.py
    - POST /api/v1/auth/register
    - POST /api/v1/auth/login
    - GET /api/v1/auth/me
```

#### Week 6-7: Alert System API (Task 1.4)
```
├── 1.4.1: Create alert schemas
│   - Create schemas/alert.py
│   - AlertResponse, AlertCreate
│
├── 1.4.2: Create alert router
│   - Create routers/alerts.py
│
├── 1.4.3: Implement get alerts endpoint
│   - GET /api/v1/alerts
│   - Filter by read status, type, severity
│   - Pagination support
│
├── 1.4.4: Implement mark as read endpoint
│   - PUT /api/v1/alerts/{id}/read
│
└── 1.4.5: Implement alert generation logic
    - Create utils/alert_generator.py
    - Weather-based alerts
    - Sensor anomaly alerts
```

#### Week 7-8: Weather Integration (Task 1.5)
```
├── 1.5.1: Sign up for OpenWeatherMap API
│   - Get API key
│   - Add to .env file
│
├── 1.5.2: Create weather service
│   - Create utils/weather_api.py
│   - Implement fetch_forecast()
│   - Implement fetch_current_weather()
│
├── 1.5.3: Create weather router
│   - Create routers/weather.py
│
├── 1.5.4: Implement forecast endpoint
│   - GET /api/v1/weather/forecast
│   - 7-day forecast
│
└── 1.5.5: Implement weather-based alerts
    - Heavy rain detection
    - Extreme heat detection
    - Storm warnings
```

**Files You Own:**
```
backend/
├── main.py
├── routers/
│   ├── auth.py
│   ├── alerts.py
│   └── weather.py
├── schemas/
│   ├── auth.py
│   └── alert.py
├── utils/
│   ├── jwt.py
│   ├── alert_generator.py
│   └── weather_api.py
└── tests/
    ├── test_auth.py
    └── test_alerts.py
```

---

### 👤 Member 2: Backend Developer + API Integration

**Primary Responsibilities:**
- ✅ Sensor data API endpoints
- ✅ Pest detection API endpoints
- ✅ Integration with ML model
- ✅ Data validation and processing
- ✅ Testing API endpoints
- ✅ Working with Member 3 (Flutter dev) on API contracts
- ✅ Working with Members 4 & 5 (ML team) on model integration

**Tasks Breakdown:**

#### Week 4-5: Sensor Data API (Task 1.2)
```
├── 1.2.1: Create sensor schemas
│   - Create schemas/sensor.py
│   - SensorReadingCreate, SensorReadingResponse
│
├── 1.2.2: Create sensor router
│   - Create routers/sensors.py
│
├── 1.2.3: Implement submit reading endpoint
│   - POST /api/v1/sensors/readings
│   - Validate sensor data
│   - Store in database
│
├── 1.2.4: Implement get readings endpoint
│   - GET /api/v1/sensors/readings
│   - Filter by date range
│   - Pagination support
│
├── 1.2.5: Implement get latest reading endpoint
│   - GET /api/v1/sensors/readings/latest
│
└── 1.2.6: Implement anomaly detection
    - Check for unusual values
    - Generate alerts if needed
```

#### Week 5-6: Pest Detection API (Task 1.3)
```
├── 1.3.1: Create pest detection schemas
│   - Create schemas/pest.py
│   - PestDetectionResponse, PestDetectionCreate
│
├── 1.3.2: Create pest detection router
│   - Create routers/pests.py
│
├── 1.3.3: Implement image upload endpoint
│   - POST /api/v1/pests/detect
│   - Handle image upload
│   - Validate image format
│
├── 1.3.4: Integrate with ML model
│   - Create utils/ml_integration.py
│   - Mock response first
│   - Real ML integration later (with Members 4 & 5)
│
├── 1.3.5: Implement get detections endpoint
│   - GET /api/v1/pests/detections
│   - Filter by date, severity
│
└── 1.3.6: Implement detection history endpoint
    - GET /api/v1/pests/detections/{id}
    - Get single detection details
```

**Files You Own:**
```
backend/
├── routers/
│   ├── sensors.py
│   └── pests.py
├── schemas/
│   ├── sensor.py
│   └── pest.py
├── utils/
│   ├── image_processing.py
│   └── ml_integration.py
└── tests/
    ├── test_sensors.py
    └── test_pests.py
```

---

### 👤 Member 3: Flutter/Mobile Developer

**Primary Responsibilities:**
- ✅ Mobile app UI/UX design
- ✅ All Flutter screens and widgets
- ✅ API integration (calling backend endpoints)
- ✅ State management (Provider/Riverpod/Bloc)
- ✅ Local storage (SharedPreferences)
- ✅ Camera integration for pest detection
- ✅ Push notifications (optional)

**Tasks Breakdown:**

#### Week 9-10: Flutter Project Setup (Task 2.1)
```
├── 2.1.1: Create Flutter project
│   - flutter create agrisense_mobile
│   - Set up folder structure
│
├── 2.1.2: Set up folder structure
│   - lib/screens/
│   - lib/services/
│   - lib/widgets/
│   - lib/models/
│
├── 2.1.3: Install dependencies
│   - http (API calls)
│   - provider (state management)
│   - shared_preferences (local storage)
│   - image_picker (camera)
│
└── 2.1.4: Set up state management
    - Choose Provider/Riverpod/Bloc
    - Set up app-wide state
```

#### Week 10-11: Authentication Screens (Task 2.2)
```
├── 2.2.1: Login screen
│   - UI design
│   - Form validation
│   - Error handling
│
├── 2.2.2: Register screen
│   - UI design
│   - Form validation
│   - Password confirmation
│
├── 2.2.3: Auth service (API calls)
│   - Create services/auth_service.dart
│   - login() method
│   - register() method
│
└── 2.2.4: Token storage
    - Store JWT token in SharedPreferences
    - Auto-login on app start
    - Logout functionality
```

#### Week 11-12: Dashboard & Sensor Screens (Task 2.3)
```
├── 2.3.1: Dashboard screen
│   - Overview cards
│   - Latest sensor readings
│   - Quick actions
│
├── 2.3.2: Sensor readings list
│   - List view with pagination
│   - Filter by date
│   - Pull to refresh
│
├── 2.3.3: Add sensor reading screen
│   - Input form for manual entry
│   - Validation
│   - Submit to API
│
└── 2.3.4: Sensor service (API calls)
    - Create services/sensor_service.dart
    - getReadings() method
    - submitReading() method
```

#### Week 12-13: Pest Detection Screens (Task 2.4)
```
├── 2.4.1: Camera integration
│   - Use image_picker package
│   - Take photo or select from gallery
│
├── 2.4.2: Image upload screen
│   - Show selected image
│   - Upload to backend
│   - Loading indicator
│
├── 2.4.3: Detection results screen
│   - Display pest name
│   - Show confidence score
│   - Display recommendations
│
└── 2.4.4: Pest service (API calls)
    - Create services/pest_service.dart
    - detectPest() method
    - getDetections() method
```

#### Week 13-14: Alerts & Weather Screens (Task 2.5)
```
├── 2.5.1: Alerts list screen
│   - List of alerts
│   - Filter by read/unread
│   - Mark as read
│
├── 2.5.2: Weather forecast screen
│   - 7-day forecast
│   - Current weather
│   - Weather icons
│
├── 2.5.3: Push notifications (optional)
│   - Firebase Cloud Messaging
│   - Local notifications
│
└── 2.5.4: Alert/Weather services
    - Create services/alert_service.dart
    - Create services/weather_service.dart
```

**Files You Own:**
```
mobile/
├── lib/
│   ├── main.dart
│   ├── screens/
│   │   ├── auth/
│   │   │   ├── login_screen.dart
│   │   │   └── register_screen.dart
│   │   ├── dashboard/
│   │   │   └── dashboard_screen.dart
│   │   ├── sensors/
│   │   │   ├── sensor_list_screen.dart
│   │   │   └── add_reading_screen.dart
│   │   ├── pests/
│   │   │   ├── camera_screen.dart
│   │   │   ├── upload_screen.dart
│   │   │   └── detection_result_screen.dart
│   │   ├── alerts/
│   │   │   └── alerts_screen.dart
│   │   └── weather/
│   │       └── weather_screen.dart
│   ├── services/
│   │   ├── auth_service.dart
│   │   ├── sensor_service.dart
│   │   ├── pest_service.dart
│   │   ├── alert_service.dart
│   │   └── weather_service.dart
│   ├── models/
│   │   ├── user.dart
│   │   ├── sensor_reading.dart
│   │   ├── pest_detection.dart
│   │   └── alert.dart
│   └── widgets/
│       ├── custom_button.dart
│       ├── sensor_card.dart
│       └── alert_card.dart
├── assets/
│   └── images/
└── pubspec.yaml
```

---

### 👤 Member 4: ML Engineer - Model Development

**Primary Responsibilities:**
- ✅ Research pest detection models
- ✅ Data collection and labeling
- ✅ Model architecture design
- ✅ Experiment with different approaches
- ✅ Jupyter notebooks for exploration
- ✅ Document findings and results

**Tasks Breakdown:**

#### Week 9-10: Dataset Preparation (Task 3.1)
```
├── 3.1.1: Collect pest images
│   - Research existing datasets
│   - Collect images from online sources
│   - Take photos if possible
│   - Target: 500-1000 images per pest type
│
├── 3.1.2: Label images
│   - Use LabelImg or similar tool
│   - Create labels.csv
│   - Categories: Fall Armyworm, Aphids, Whitefly, etc.
│
├── 3.1.3: Data exploration
│   - Create 01_data_exploration.ipynb
│   - Analyze image sizes, formats
│   - Check class distribution
│
└── 3.1.4: Document dataset
    - Create DATASET.md
    - Document sources
    - Document labeling process
```

#### Week 10-11: Model Development (Task 3.2)
```
├── 3.2.1: Research models
│   - Review papers on pest detection
│   - Compare CNN architectures
│   - Consider transfer learning
│
├── 3.2.2: Implement baseline model
│   - Create models/baseline_model.py
│   - Simple CNN architecture
│   - Train on small dataset
│
├── 3.2.3: Experiment with architectures
│   - Create 02_model_experiments.ipynb
│   - Try different architectures:
│     - ResNet50
│     - MobileNetV2
│     - EfficientNet
│   - Compare results
│
└── 3.2.4: Document findings
    - Create MODEL_EXPERIMENTS.md
    - Document each experiment
    - Compare accuracy, speed, size
```

#### Week 11-12: Model Refinement (Task 3.3)
```
├── 3.3.1: Data augmentation
│   - Implement augmentation pipeline
│   - Rotation, flip, zoom, brightness
│
├── 3.3.2: Feature engineering
│   - Experiment with preprocessing
│   - Try different input sizes
│
├── 3.3.3: Model evaluation
│   - Create 03_results_analysis.ipynb
│   - Confusion matrix
│   - Precision, recall, F1-score
│
└── 3.3.4: Select best model
    - Compare all experiments
    - Choose final architecture
    - Document decision
```

**Files You Own:**
```
ml/
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_model_experiments.ipynb
│   └── 03_results_analysis.ipynb
├── datasets/
│   ├── raw/
│   ├── processed/
│   └── labels.csv
├── models/
│   ├── baseline_model.py
│   ├── cnn_model.py
│   └── transfer_learning.py
└── docs/
    ├── DATASET.md
    └── MODEL_EXPERIMENTS.md
```

---

### 👤 Member 5: ML Engineer - Model Training & Optimization

**Primary Responsibilities:**
- ✅ Training pipeline setup
- ✅ Model training and fine-tuning
- ✅ Model evaluation and metrics
- ✅ Model optimization (speed, accuracy)
- ✅ Model deployment preparation
- ✅ Create inference API

**Tasks Breakdown:**

#### Week 10-11: Training Pipeline (Task 3.4)
```
├── 3.4.1: Set up training environment
│   - Install TensorFlow/PyTorch
│   - Set up GPU (if available)
│   - Create requirements.txt for ML
│
├── 3.4.2: Create training script
│   - Create training/train.py
│   - Data loading
│   - Training loop
│   - Checkpointing
│
├── 3.4.3: Create evaluation script
│   - Create training/evaluate.py
│   - Calculate metrics
│   - Generate reports
│
└── 3.4.4: Create config file
    - Create training/config.yaml
    - Hyperparameters
    - Paths
    - Training settings
```

#### Week 11-12: Model Training (Task 3.5)
```
├── 3.5.1: Train baseline model
│   - Use Member 4's architecture
│   - Train on full dataset
│   - Monitor metrics
│
├── 3.5.2: Hyperparameter tuning
│   - Learning rate
│   - Batch size
│   - Optimizer
│   - Regularization
│
├── 3.5.3: Train final model
│   - Use best hyperparameters
│   - Train for more epochs
│   - Save best checkpoint
│
└── 3.5.4: Model evaluation
    - Test on validation set
    - Calculate final metrics
    - Generate confusion matrix
```

#### Week 12-13: Model Optimization & Deployment (Task 3.6)
```
├── 3.6.1: Model optimization
│   - Quantization (reduce size)
│   - Pruning (reduce complexity)
│   - Convert to TFLite (for mobile)
│
├── 3.6.2: Create inference API
│   - Create api/inference.py
│   - FastAPI endpoint
│   - Image preprocessing
│   - Model loading
│
├── 3.6.3: Test inference API
│   - Test with sample images
│   - Measure inference time
│   - Optimize if needed
│
└── 3.6.4: Integration with backend
    - Work with Member 2
    - Test end-to-end flow
    - Deploy ML API
```

**Files You Own:**
```
ml/
├── training/
│   ├── train.py
│   ├── evaluate.py
│   ├── config.yaml
│   └── utils.py
├── api/
│   ├── inference.py
│   ├── model_loader.py
│   └── preprocessing.py
├── models/
│   ├── checkpoints/
│   └── final_model.h5
└── docs/
    ├── TRAINING.md
    └── DEPLOYMENT.md
```

---

## 🔄 Git Workflow

### Branch Strategy

```
main (production-ready code)
│
├── develop (integration branch)
│   │
│   ├── feature/auth-system          ← Member 1
│   ├── feature/alert-system         ← Member 1
│   ├── feature/weather-integration  ← Member 1
│   ├── feature/sensor-api           ← Member 2
│   ├── feature/pest-api             ← Member 2
│   ├── feature/ml-integration       ← Member 2
│   ├── feature/flutter-auth         ← Member 3
│   ├── feature/flutter-dashboard    ← Member 3
│   ├── feature/flutter-sensors      ← Member 3
│   ├── feature/ml-model-dev         ← Member 4
│   ├── feature/ml-experiments       ← Member 4
│   ├── feature/ml-training          ← Member 5
│   └── feature/ml-deployment        ← Member 5
```

### Workflow Steps

#### 1. Starting a New Feature

```bash
# 1. Make sure you're on develop and it's up to date
git checkout develop
git pull origin develop

# 2. Create your feature branch
git checkout -b feature/your-feature-name

# Example for Member 1:
git checkout -b feature/auth-system

# Example for Member 2:
git checkout -b feature/sensor-api

# Example for Member 3:
git checkout -b feature/flutter-auth
```

#### 2. Working on Your Feature

```bash
# Make changes to your files
# Test your code

# Stage your changes
git add .

# Commit with a clear message
git commit -m "Add login endpoint with JWT authentication"

# Push to remote
git push origin feature/your-feature-name
```

#### 3. Creating a Pull Request

```bash
# 1. Push your branch to GitHub
git push origin feature/your-feature-name

# 2. Go to GitHub repository
# 3. Click "New Pull Request"
# 4. Select: base: develop ← compare: feature/your-feature-name
# 5. Fill in PR template:
#    - What does this PR do?
#    - How to test?
#    - Screenshots (if UI changes)
# 6. Request review from team members
```

#### 4. Code Review Process

**For PR Author:**
- Respond to comments
- Make requested changes
- Push updates to the same branch

**For Reviewers:**
- Review code within 24 hours
- Leave constructive comments
- Approve if looks good

**Merge Criteria:**
- At least 1 approval
- All tests pass
- No merge conflicts

#### 5. Merging to Develop

```bash
# After approval, merge on GitHub
# Then update your local develop branch

git checkout develop
git pull origin develop

# Delete your feature branch (optional)
git branch -d feature/your-feature-name
```

### Commit Message Guidelines

**Format:**
```
<type>: <subject>

<body (optional)>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples:**

```bash
# Good commit messages
git commit -m "feat: add login endpoint with JWT authentication"
git commit -m "fix: resolve sensor reading validation error"
git commit -m "docs: update API documentation for pest detection"
git commit -m "refactor: simplify alert generation logic"

# Bad commit messages (avoid these)
git commit -m "update"
git commit -m "fix bug"
git commit -m "changes"
```

### Handling Merge Conflicts

```bash
# 1. Update your branch with latest develop
git checkout feature/your-feature
git pull origin develop

# 2. If conflicts occur, Git will tell you which files
# 3. Open conflicted files and resolve manually
# 4. Look for conflict markers:
#    <<<<<<< HEAD
#    Your changes
#    =======
#    Changes from develop
#    >>>>>>> develop

# 5. After resolving, stage and commit
git add .
git commit -m "resolve merge conflicts with develop"
git push origin feature/your-feature
```

---

## 💬 Communication & Coordination

### Daily Standup (15 minutes)

**Time:** 9:00 AM (or agreed time)  
**Format:** Slack/Discord or Video call

**Each member answers:**
1. ✅ What did I complete yesterday?
2. 🔨 What am I working on today?
3. 🚧 Any blockers?

**Example:**

```
Member 1 (Backend Lead):
✅ Yesterday: Completed JWT authentication endpoints
🔨 Today: Starting alert system API
🚧 Blockers: None

Member 2 (Backend Dev):
✅ Yesterday: Implemented sensor data validation
🔨 Today: Working on pest detection image upload
🚧 Blockers: Need to coordinate with Member 3 on API response format

Member 3 (Flutter Dev):
✅ Yesterday: Designed login screen UI
🔨 Today: Implementing login API integration
🚧 Blockers: Waiting for auth endpoints from Member 1

Member 4 (ML - Model Dev):
✅ Yesterday: Collected 300 pest images
🔨 Today: Labeling images and data exploration
🚧 Blockers: None

Member 5 (ML - Training):
✅ Yesterday: Set up training environment
🔨 Today: Creating training pipeline script
🚧 Blockers: Waiting for labeled data from Member 4
```

### Weekly Sync Meeting (1 hour)

**Time:** Friday 3:00 PM (or agreed time)  
**Format:** Video call

**Agenda:**
1. **Demo Time (30 min):** Each member demos completed work
2. **Blockers Discussion (15 min):** Resolve any issues
3. **Next Week Planning (15 min):** Assign tasks for next week

**Meeting Notes Template:**

```markdown
# Weekly Sync - Week X

**Date:** January 10, 2026  
**Attendees:** All 5 members

## Demos
- Member 1: Demonstrated auth endpoints in Swagger UI
- Member 2: Showed sensor data API working with Postman
- Member 3: Showed login screen mockup
- Member 4: Presented dataset exploration notebook
- Member 5: Showed training pipeline setup

## Blockers Resolved
- Member 3 needed API docs → Member 1 shared Swagger link
- Member 5 needed labeled data → Member 4 will finish by Monday

## Next Week Goals
- Member 1: Complete alert system
- Member 2: Finish pest detection API
- Member 3: Complete auth screens
- Member 4: Finish data labeling
- Member 5: Train baseline model

## Action Items
- [ ] Member 1: Update API documentation
- [ ] Member 2: Create API contract doc for Member 3
- [ ] Member 4: Share labeled dataset with Member 5
```

### Communication Channels

#### Slack/Discord Channels

```
#general - General team chat
#backend - Backend discussions (Members 1 & 2)
#frontend - Flutter discussions (Member 3)
#ml - ML discussions (Members 4 & 5)
#integration - Cross-team coordination
#random - Non-work chat
```

#### GitHub Issues

**Use for:**
- Bug reports
- Feature requests
- Task tracking

**Issue Template:**

```markdown
**Title:** [BUG] Login endpoint returns 500 error

**Description:**
When calling POST /api/v1/auth/login with valid credentials, 
the server returns 500 Internal Server Error.

**Steps to Reproduce:**
1. Send POST request to /api/v1/auth/login
2. Include valid username and password
3. Observe 500 error

**Expected Behavior:**
Should return 200 with JWT token

**Actual Behavior:**
Returns 500 error

**Assigned To:** @Member1
**Labels:** bug, backend, high-priority
```

#### Response Time Expectations

| Channel | Response Time |
|---------|---------------|
| **Urgent (Blocker)** | Within 2 hours |
| **Slack/Discord** | Within 4 hours |
| **GitHub PR Review** | Within 24 hours |
| **GitHub Issues** | Within 48 hours |
| **Email** | Within 2 days |

---

## 📄 API Contract

### Why API Contracts Matter

API contracts ensure that:
- Frontend knows what to expect from backend
- Backend knows what frontend needs
- Both teams can work in parallel
- Changes are communicated clearly

### API Contract Document

**Location:** `docs/API_CONTRACT.md`

**Template:**

```markdown
# AgriSense API Contract

## Base URL
- Development: `http://localhost:8000`
- Production: `https://api.agrisense.com`

## Authentication
All protected endpoints require JWT token in header:
```
Authorization: Bearer <token>
```

---

## 1. Authentication Endpoints

### 1.1 Register User

**Endpoint:** `POST /api/v1/auth/register`

**Request Body:**
```json
{
  "username": "farmer1",
  "password": "password123"
}
```

**Success Response (201):**
```json
{
  "id": 1,
  "username": "farmer1",
  "is_active": true,
  "created_at": "2026-01-04T10:30:00Z"
}
```

**Error Response (400):**
```json
{
  "detail": "Username already exists"
}
```

---

### 1.2 Login User

**Endpoint:** `POST /api/v1/auth/login`

**Request Body:**
```json
{
  "username": "farmer1",
  "password": "password123"
}
```

**Success Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "farmer1"
  }
}
```

**Error Response (401):**
```json
{
  "detail": "Incorrect username or password"
}
```

---

### 1.3 Get Current User

**Endpoint:** `GET /api/v1/auth/me`

**Headers:**
```
Authorization: Bearer <token>
```

**Success Response (200):**
```json
{
  "id": 1,
  "username": "farmer1",
  "is_active": true,
  "created_at": "2026-01-04T10:30:00Z"
}
```

**Error Response (401):**
```json
{
  "detail": "Not authenticated"
}
```

---

## 2. Sensor Readings Endpoints

### 2.1 Submit Sensor Reading

**Endpoint:** `POST /api/v1/sensors/readings`

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "temperature": 28.5,
  "humidity": 65.2,
  "soil_moisture": 52.3,
  "light_intensity": 45000
}
```

**Success Response (201):**
```json
{
  "id": 1,
  "user_id": 1,
  "temperature": 28.5,
  "humidity": 65.2,
  "soil_moisture": 52.3,
  "light_intensity": 45000,
  "timestamp": "2026-01-04T10:30:00Z"
}
```

**Error Response (422):**
```json
{
  "detail": [
    {
      "loc": ["body", "temperature"],
      "msg": "ensure this value is greater than or equal to -50",
      "type": "value_error.number.not_ge"
    }
  ]
}
```

---

### 2.2 Get Sensor Readings

**Endpoint:** `GET /api/v1/sensors/readings`

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `limit` (optional): Number of readings (default: 100)
- `offset` (optional): Pagination offset (default: 0)
- `start_date` (optional): Filter from date (ISO format)
- `end_date` (optional): Filter to date (ISO format)

**Example:**
```
GET /api/v1/sensors/readings?limit=10&offset=0
```

**Success Response (200):**
```json
{
  "total": 168,
  "limit": 10,
  "offset": 0,
  "readings": [
    {
      "id": 1,
      "temperature": 28.5,
      "humidity": 65.2,
      "soil_moisture": 52.3,
      "light_intensity": 45000,
      "timestamp": "2026-01-04T10:30:00Z"
    },
    {
      "id": 2,
      "temperature": 29.1,
      "humidity": 63.8,
      "soil_moisture": 51.9,
      "light_intensity": 48000,
      "timestamp": "2026-01-04T11:30:00Z"
    }
  ]
}
```

---

### 2.3 Get Latest Sensor Reading

**Endpoint:** `GET /api/v1/sensors/readings/latest`

**Headers:**
```
Authorization: Bearer <token>
```

**Success Response (200):**
```json
{
  "id": 168,
  "temperature": 27.8,
  "humidity": 68.5,
  "soil_moisture": 54.1,
  "light_intensity": 42000,
  "timestamp": "2026-01-04T14:30:00Z"
}
```

---

## 3. Pest Detection Endpoints

### 3.1 Detect Pest (Upload Image)

**Endpoint:** `POST /api/v1/pests/detect`

**Headers:**
```
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**Request Body (Form Data):**
```
image: <file>
```

**Success Response (200):**
```json
{
  "id": 1,
  "user_id": 1,
  "image_url": "/uploads/pest_123.jpg",
  "pest_type": "Fall Armyworm",
  "confidence_score": 0.87,
  "severity_level": "high",
  "recommendations": "Apply recommended pesticide immediately. Monitor field daily.",
  "detected_at": "2026-01-04T10:30:00Z"
}
```

**Error Response (400):**
```json
{
  "detail": "Invalid image format. Only JPG, JPEG, PNG allowed."
}
```

---

### 3.2 Get Pest Detections

**Endpoint:** `GET /api/v1/pests/detections`

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `limit` (optional): Number of detections (default: 50)
- `offset` (optional): Pagination offset (default: 0)

**Success Response (200):**
```json
{
  "total": 9,
  "limit": 50,
  "offset": 0,
  "detections": [
    {
      "id": 1,
      "pest_type": "Fall Armyworm",
      "confidence_score": 0.87,
      "severity_level": "high",
      "detected_at": "2026-01-04T10:30:00Z"
    },
    {
      "id": 2,
      "pest_type": "Aphids",
      "confidence_score": 0.85,
      "severity_level": "medium",
      "detected_at": "2026-01-03T15:20:00Z"
    }
  ]
}
```

---

## 4. Alerts Endpoints

### 4.1 Get Alerts

**Endpoint:** `GET /api/v1/alerts`

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `is_read` (optional): Filter by read status (true/false)
- `alert_type` (optional): Filter by type (weather, pest, environmental)
- `severity` (optional): Filter by severity (low, medium, high, critical)

**Example:**
```
GET /api/v1/alerts?is_read=false&severity=high
```

**Success Response (200):**
```json
{
  "total": 12,
  "unread_count": 8,
  "alerts": [
    {
      "id": 1,
      "alert_type": "weather",
      "severity": "high",
      "title": "Heavy Rain Warning",
      "message": "Heavy rain (65mm) expected tomorrow. Take precautions.",
      "recommendations": "Cover crops, prepare drainage, secure equipment",
      "is_read": false,
      "created_at": "2026-01-04T08:00:00Z"
    },
    {
      "id": 2,
      "alert_type": "pest",
      "severity": "critical",
      "title": "Fall Armyworm Detected",
      "message": "Fall Armyworm detected with 87% confidence.",
      "recommendations": "Apply recommended pesticide immediately.",
      "is_read": false,
      "created_at": "2026-01-04T10:30:00Z"
    }
  ]
}
```

---

### 4.2 Mark Alert as Read

**Endpoint:** `PUT /api/v1/alerts/{alert_id}/read`

**Headers:**
```
Authorization: Bearer <token>
```

**Success Response (200):**
```json
{
  "id": 1,
  "is_read": true,
  "read_at": "2026-01-04T15:00:00Z"
}
```

---

## 5. Weather Endpoints

### 5.1 Get Weather Forecast

**Endpoint:** `GET /api/v1/weather/forecast`

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `days` (optional): Number of days (default: 7, max: 7)

**Success Response (200):**
```json
{
  "location": "Nairobi, Kenya",
  "current": {
    "temperature": 24.5,
    "humidity": 65,
    "description": "Partly cloudy",
    "icon": "02d"
  },
  "forecast": [
    {
      "date": "2026-01-05",
      "temp_min": 18.0,
      "temp_max": 26.5,
      "humidity": 60,
      "precipitation": 0,
      "description": "Sunny",
      "icon": "01d"
    },
    {
      "date": "2026-01-06",
      "temp_min": 19.0,
      "temp_max": 27.0,
      "humidity": 70,
      "precipitation": 15,
      "description": "Light rain",
      "icon": "10d"
    }
  ]
}
```

---

## Error Responses

### Standard Error Format

All errors follow this format:

```json
{
  "detail": "Error message here"
}
```

### HTTP Status Codes

| Code | Meaning | When Used |
|------|---------|-----------|
| 200 | OK | Successful GET, PUT |
| 201 | Created | Successful POST |
| 400 | Bad Request | Invalid input data |
| 401 | Unauthorized | Missing or invalid token |
| 403 | Forbidden | Valid token but no permission |
| 404 | Not Found | Resource doesn't exist |
| 422 | Unprocessable Entity | Validation error |
| 500 | Internal Server Error | Server error |

---

## Testing the API

### Using Swagger UI

1. Start backend server: `uvicorn main:app --reload`
2. Open browser: `http://localhost:8000/docs`
3. Click on endpoint
4. Click "Try it out"
5. Fill in parameters
6. Click "Execute"

### Using Postman

1. Import collection from `docs/AgriSense.postman_collection.json`
2. Set environment variable `base_url` to `http://localhost:8000`
3. Login to get token
4. Use token in subsequent requests

### Using cURL

```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"farmer1","password":"password123"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"farmer1","password":"password123"}'

# Get sensor readings (with token)
curl -X GET http://localhost:8000/api/v1/sensors/readings \
  -H "Authorization: Bearer <your-token>"
```
```

### Creating the API Contract

**Who Creates:**
- Members 1 & 2 (Backend) draft the initial contract
- Member 3 (Flutter) reviews and suggests changes
- All agree before implementation

**When to Update:**
- Before implementing new endpoints
- When changing request/response format
- When adding new fields

**How to Update:**
1. Create GitHub issue proposing change
2. Discuss in team meeting
3. Update API_CONTRACT.md
4. Notify all team members

---

## 🤖 ML Integration

### Integration Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Flutter App (Member 3)                                 │
│  - User takes photo of pest                             │
│  - Uploads to backend                                   │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ HTTP POST /api/v1/pests/detect
                     │ (multipart/form-data with image)
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│  FastAPI Backend (Member 2)                             │
│  ┌────────────────────────────────────────────────────┐ │
│  │  routers/pests.py                                  │ │
│  │  - Receives image upload                           │ │
│  │  - Validates image format                          │ │
│  │  - Saves image to disk                             │ │
│  └──────────────────┬─────────────────────────────────┘ │
│                     │                                    │
│  ┌────────────────────────────────────────────────────┐ │
│  │  utils/ml_integration.py                           │ │
│  │  - Calls ML API                                    │ │
│  │  - Handles errors                                  │ │
│  │  - Returns prediction                              │ │
│  └──────────────────┬─────────────────────────────────┘ │
└────────────────────┬┴────────────────────────────────────┘
                     │
                     │ HTTP POST http://ml-server:5001/predict
                     │ (multipart/form-data with image)
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│  ML API Server (Members 4 & 5)                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │  api/inference.py                                  │ │
│  │  - Receives image                                  │ │
│  │  - Preprocesses image                              │ │
│  │  - Loads ML model                                  │ │
│  │  - Runs inference                                  │ │
│  │  - Returns prediction                              │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### Phase 1: Mock ML Integration (Week 5-6)

**Member 2 creates mock response:**

```python
# backend/utils/ml_integration.py

def detect_pest_mock(image_path: str) -> dict:
    """
    Mock ML detection for testing
    Returns fake prediction
    """
    import random
    
    pests = [
        ("Fall Armyworm", 0.87, "high"),
        ("Aphids", 0.85, "medium"),
        ("Whitefly", 0.78, "low")
    ]
    
    pest_type, confidence, severity = random.choice(pests)
    
    return {
        "pest_type": pest_type,
        "confidence_score": confidence,
        "severity_level": severity,
        "recommendations": f"Apply recommended treatment for {pest_type}."
    }

# Usage in routers/pests.py
@router.post("/detect")
async def detect_pest(
    image: UploadFile,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Save image
    image_path = save_uploaded_image(image)
    
    # Get prediction (mock for now)
    prediction = detect_pest_mock(image_path)
    
    # Save to database
    detection = PestDetection(
        user_id=current_user.id,
        image_url=image_path,
        **prediction
    )
    db.add(detection)
    db.commit()
    
    return detection
```

### Phase 2: Real ML Integration (Week 11-12)

**Members 4 & 5 create ML API:**

```python
# ml/api/inference.py

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
import numpy as np
from PIL import Image
import io

app = FastAPI(title="AgriSense ML API")

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model at startup
model = None

@app.on_event("startup")
async def load_model():
    global model
    model = tf.keras.models.load_model('models/pest_detection_model.h5')
    print("Model loaded successfully")

# Preprocessing function
def preprocess_image(image_bytes: bytes) -> np.ndarray:
    """
    Preprocess image for model input
    """
    # Open image
    image = Image.open(io.BytesIO(image_bytes))
    
    # Resize to model input size (e.g., 224x224)
    image = image.resize((224, 224))
    
    # Convert to array
    img_array = np.array(image)
    
    # Normalize
    img_array = img_array / 255.0
    
    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array

# Pest classes
PEST_CLASSES = [
    "Fall Armyworm",
    "Aphids",
    "Whitefly",
    "Healthy (No Pest)"
]

# Severity mapping
def get_severity(confidence: float) -> str:
    if confidence >= 0.85:
        return "high"
    elif confidence >= 0.70:
        return "medium"
    else:
        return "low"

# Recommendations mapping
RECOMMENDATIONS = {
    "Fall Armyworm": "Apply recommended pesticide immediately. Monitor field daily. Consider biological control methods.",
    "Aphids": "Use insecticidal soap or neem oil. Introduce natural predators like ladybugs.",
    "Whitefly": "Use yellow sticky traps. Apply insecticidal soap. Remove heavily infested leaves.",
    "Healthy (No Pest)": "Continue regular monitoring. Maintain good agricultural practices."
}

@app.post("/predict")
async def predict(image: UploadFile = File(...)):
    """
    Predict pest type from uploaded image
    """
    try:
        # Read image bytes
        image_bytes = await image.read()
        
        # Preprocess
        img_array = preprocess_image(image_bytes)
        
        # Run inference
        predictions = model.predict(img_array)
        
        # Get top prediction
        predicted_class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_idx])
        pest_type = PEST_CLASSES[predicted_class_idx]
        
        # Get severity
        severity = get_severity(confidence)
        
        # Get recommendations
        recommendations = RECOMMENDATIONS.get(pest_type, "Consult agricultural expert.")
        
        return {
            "pest_type": pest_type,
            "confidence_score": round(confidence, 2),
            "severity_level": severity,
            "recommendations": recommendations,
            "all_predictions": {
                PEST_CLASSES[i]: round(float(predictions[0][i]), 2)
                for i in range(len(PEST_CLASSES))
            }
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "pest_type": "Unknown",
            "confidence_score": 0.0,
            "severity_level": "unknown",
            "recommendations": "Error processing image. Please try again."
        }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)
```

**Member 2 updates backend integration:**

```python
# backend/utils/ml_integration.py

import requests
from fastapi import UploadFile
import os

ML_API_URL = os.getenv("ML_API_URL", "http://localhost:5001")

def detect_pest_real(image_path: str) -> dict:
    """
    Call real ML API for pest detection
    """
    try:
        # Read image file
        with open(image_path, 'rb') as f:
            files = {'image': f}
            
            # Call ML API
            response = requests.post(
                f"{ML_API_URL}/predict",
                files=files,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"ML API returned {response.status_code}")
                
    except Exception as e:
        # Fallback to mock if ML API fails
        print(f"ML API error: {e}. Using mock response.")
        return detect_pest_mock(image_path)

# Update routers/pests.py to use detect_pest_real instead of detect_pest_mock
```

### Testing ML Integration

**Step 1: Start ML API (Members 4 & 5)**
```bash
cd ml
python api/inference.py
# ML API running on http://localhost:5001
```

**Step 2: Start Backend API (Member 2)**
```bash
cd backend
uvicorn main:app --reload --port 8000
# Backend API running on http://localhost:8000
```

**Step 3: Test with cURL**
```bash
# Test ML API directly
curl -X POST http://localhost:5001/predict \
  -F "image=@test_pest.jpg"

# Test through backend
curl -X POST http://localhost:8000/api/v1/pests/detect \
  -H "Authorization: Bearer <token>" \
  -F "image=@test_pest.jpg"
```

**Step 4: Test with Flutter (Member 3)**
```dart
// services/pest_service.dart
Future<PestDetection> detectPest(File imageFile) async {
  final request = http.MultipartRequest(
    'POST',
    Uri.parse('$baseUrl/api/v1/pests/detect'),
  );
  
  request.headers['Authorization'] = 'Bearer $token';
  request.files.add(await http.MultipartFile.fromPath('image', imageFile.path));
  
  final response = await request.send();
  final responseData = await response.stream.bytesToString();
  
  return PestDetection.fromJson(json.decode(responseData));
}
```

### ML Team Deliverables

**Members 4 & 5 must provide:**

1. **Trained Model File**
   - `ml/models/pest_detection_model.h5` (TensorFlow)
   - Or `ml/models/pest_detection_model.pth` (PyTorch)

2. **Model Documentation**
   - `ml/docs/MODEL.md`
   - Architecture details
   - Input/output format
   - Performance metrics
   - Training details

3. **Inference API**
   - `ml/api/inference.py`
   - FastAPI server
   - `/predict` endpoint
   - `/health` endpoint

4. **Requirements File**
   - `ml/requirements.txt`
   - All ML dependencies

5. **Deployment Instructions**
   - `ml/docs/DEPLOYMENT.md`
   - How to run ML API
   - Environment setup
   - Troubleshooting

---

## 📅 Timeline & Milestones

### 14-Week Project Timeline

```
┌─────────────────────────────────────────────────────────┐
│  PHASE 0: Setup & Planning (Week 1-2) - COMPLETE ✅     │
└─────────────────────────────────────────────────────────┘

Week 1-2: Project Setup
├── Member 1: Backend setup ✅
├── Member 2: Learn FastAPI, clone repo
├── Member 3: Learn Flutter basics
├── Members 4 & 5: Research ML models
└── All: Team meeting, role assignment

Deliverables:
✅ Backend structure complete
✅ Database models created
✅ Git repository set up
✅ Team roles assigned

---

┌─────────────────────────────────────────────────────────┐
│  PHASE 1: Backend Development (Week 3-8)                │
└─────────────────────────────────────────────────────────┘

Week 3-4: Authentication System
├── Member 1: JWT auth, register, login
├── Member 2: Learn backend codebase
├── Member 3: UI mockups for mobile app
└── Members 4 & 5: Data collection starts

Deliverables:
- [ ] Auth endpoints working
- [ ] JWT token generation
- [ ] User registration/login
- [ ] API documentation updated

---

Week 4-5: Sensor Data API
├── Member 1: Alert system planning
├── Member 2: Sensor endpoints, validation
├── Member 3: Flutter project setup
└── Members 4 & 5: Data labeling

Deliverables:
- [ ] Sensor CRUD endpoints
- [ ] Data validation working
- [ ] Anomaly detection logic
- [ ] API tested with Postman

---

Week 5-6: Pest Detection API (Mock)
├── Member 1: Alert system implementation
├── Member 2: Pest endpoints, image upload, mock ML
├── Member 3: Auth screens in Flutter
└── Members 4 & 5: Model experiments

Deliverables:
- [ ] Image upload working
- [ ] Mock ML responses
- [ ] Pest detection endpoints
- [ ] Alert system API complete

---

Week 6-7: Weather Integration
├── Member 1: Weather API integration
├── Member 2: Testing, bug fixes
├── Member 3: Dashboard screen
└── Members 4 & 5: Model training

Deliverables:
- [ ] Weather forecast endpoint
- [ ] Weather-based alerts
- [ ] All backend endpoints complete
- [ ] API documentation finalized

---

Week 7-8: Backend Refinement
├── Member 1: Deployment setup
├── Member 2: Performance optimization
├── Member 3: Sensor screens
└── Members 4 & 5: Model optimization

Deliverables:
- [ ] Backend deployed to server
- [ ] All endpoints tested
- [ ] Performance optimized
- [ ] Documentation complete

---

┌─────────────────────────────────────────────────────────┐
│  PHASE 2: Frontend Development (Week 9-12)              │
└─────────────────────────────────────────────────────────┘

Week 9-10: Flutter Core Features
├── Member 1: Backend support
├── Member 2: ML integration preparation
├── Member 3: Auth + Dashboard + Sensors
└── Members 4 & 5: ML API development

Deliverables:
- [ ] Login/Register screens
- [ ] Dashboard screen
- [ ] Sensor list/add screens
- [ ] API integration working

---

Week 10-11: Pest Detection & Alerts
├── Member 1: Backend monitoring
├── Member 2: Real ML integration
├── Member 3: Pest detection + Alerts screens
└── Members 4 & 5: ML API testing

Deliverables:
- [ ] Camera integration
- [ ] Image upload working
- [ ] Alerts screen
- [ ] ML API integrated

---

Week 11-12: Weather & Polish
├── Member 1: Bug fixes
├── Member 2: API optimization
├── Member 3: Weather screen + UI polish
└── Members 4 & 5: ML deployment

Deliverables:
- [ ] Weather forecast screen
- [ ] All screens complete
- [ ] UI polished
- [ ] ML model deployed

---

┌─────────────────────────────────────────────────────────┐
│  PHASE 3: Integration & Testing (Week 13-14)            │
└─────────────────────────────────────────────────────────┘

Week 13: Integration Testing
├── All members: End-to-end testing
├── All members: Bug fixes
├── All members: Performance testing
└── All members: User acceptance testing

Deliverables:
- [ ] All features working together
- [ ] Bugs fixed
- [ ] Performance acceptable
- [ ] User feedback incorporated

---

Week 14: Final Polish & Presentation
├── All members: Final bug fixes
├── All members: Documentation
├── All members: Presentation preparation
└── All members: Demo video

Deliverables:
- [ ] Final version deployed
- [ ] Documentation complete
- [ ] Presentation ready
- [ ] Demo video created
- [ ] Project submitted
```

### Milestone Checklist

#### Milestone 1: Backend Complete (End of Week 8)
- [ ] All API endpoints implemented
- [ ] Authentication working
- [ ] Database populated with test data
- [ ] API documentation complete
- [ ] Swagger UI accessible
- [ ] Backend deployed to server

#### Milestone 2: Frontend Complete (End of Week 12)
- [ ] All screens implemented
- [ ] API integration working
- [ ] Camera functionality working
- [ ] Data displays correctly
- [ ] Error handling implemented
- [ ] App runs on Android/iOS

#### Milestone 3: ML Integrated (End of Week 12)
- [ ] Model trained and optimized
- [ ] ML API deployed
- [ ] Backend integrated with ML API
- [ ] Flutter app shows real predictions
- [ ] Accuracy acceptable (>80%)

#### Milestone 4: Project Complete (End of Week 14)
- [ ] All features working
- [ ] No critical bugs
- [ ] Documentation complete
- [ ] Presentation ready
- [ ] Demo video created
- [ ] Project submitted

---

## 🛠️ Tools for Collaboration

### 1. Version Control

**GitHub Repository**

```
Repository: github.com/your-team/agrisense
Branches:
├── main (production)
├── develop (integration)
└── feature/* (individual features)
```

**GitHub Features to Use:**
- **Issues:** Track bugs and tasks
- **Projects:** Kanban board for task management
- **Pull Requests:** Code review
- **Wiki:** Project documentation
- **Actions:** CI/CD (optional)

---

### 2. Communication

**Slack/Discord**

```
Channels:
├── #general - General team chat
├── #backend - Backend discussions
├── #frontend - Flutter discussions
├── #ml - ML discussions
├── #integration - Cross-team coordination
├── #bugs - Bug reports
└── #random - Non-work chat
```

**Best Practices:**
- Use threads for long discussions
- Tag people with @mention
- Use code blocks for code snippets
- Share screenshots/videos for UI issues

---

### 3. Documentation

**Confluence/Notion**

```
Pages:
├── Project Overview
├── Team Roles
├── API Documentation
├── Meeting Notes
├── Decision Log
└── FAQ
```

**Google Docs**
- Meeting agendas
- Weekly reports
- Shared notes

---

### 4. API Testing

**Postman**

```
Collections:
├── Authentication
│   ├── Register
│   ├── Login
│   └── Get Current User
├── Sensors
│   ├── Submit Reading
│   ├── Get Readings
│   └── Get Latest
├── Pests
│   ├── Detect Pest
│   └── Get Detections
├── Alerts
│   ├── Get Alerts
│   └── Mark as Read
└── Weather
    └── Get Forecast
```

**Share Postman Collection:**
1. Export collection
2. Save to `docs/AgriSense.postman_collection.json`
3. Commit to Git
4. Team members import

---

### 5. Project Management

**GitHub Projects (Kanban Board)**

```
Columns:
├── Backlog (All tasks)
├── To Do (This week)
├── In Progress (Currently working)
├── In Review (PR created)
├── Done (Merged)
└── Blocked (Waiting on something)
```

**Card Template:**
```
Title: [Backend] Implement login endpoint
Assignee: @Member1
Labels: backend, authentication, high-priority
Estimate: 4 hours
Description:
- Create POST /api/v1/auth/login endpoint
- Validate username and password
- Generate JWT token
- Return token and user info
```

---

### 6. Code Quality

**Linting & Formatting**

**Backend (Python):**
```bash
# Install tools
pip install black flake8 mypy

# Format code
black .

# Check style
flake8 .

# Type checking
mypy .
```

**Frontend (Flutter):**
```bash
# Format code
flutter format .

# Analyze code
flutter analyze
```

**Pre-commit Hooks:**
```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
# Runs checks before each commit
```

---

### 7. Testing

**Backend Testing:**
```bash
# Run tests
pytest

# With coverage
pytest --cov=backend --cov-report=html
```

**Frontend Testing:**
```bash
# Run tests
flutter test

# Integration tests
flutter drive --target=test_driver/app.dart
```

---

## 📋 First Team Meeting Agenda

### Meeting Details

**Date:** [To be scheduled]  
**Time:** 1 hour  
**Location:** Video call (Zoom/Google Meet)  
**Attendees:** All 5 team members

---

### Agenda

#### 1. Introductions (10 minutes)

**Each member shares:**
- Name and background
- Experience with relevant technologies
- Strengths and interests
- Availability (hours per week)

**Example:**
```
"Hi, I'm [Name]. I have experience with Python and FastAPI from 
a previous project. I'm interested in backend development and 
can commit 15 hours per week. I'm strongest in API design but 
want to learn more about deployment."
```

---

#### 2. Project Overview (15 minutes)

**Member 1 presents:**
- AgriSense goals and features
- Current progress (Phase 0 complete)
- Dual core features (Weather + Pest Detection)
- Technology stack
- 14-week timeline

**Show:**
- Backend running (Swagger UI)
- Database with test data
- Project structure

---

#### 3. Role Assignment & Responsibilities (15 minutes)

**Discuss and confirm:**
- Member 1: Backend Lead + DevOps
- Member 2: Backend Developer + ML Integration
- Member 3: Flutter Developer
- Member 4: ML Engineer - Model Development
- Member 5: ML Engineer - Training & Deployment

**Questions to address:**
- Is everyone comfortable with their role?
- Any concerns or preferences?
- Any skills gaps that need support?

---

#### 4. Setup Tasks (15 minutes)

**Immediate action items:**

**Member 1 (You):**
- [ ] Share GitHub repository access
- [ ] Share Slack/Discord invite
- [ ] Share API documentation link
- [ ] Share this collaboration guide

**Member 2:**
- [ ] Clone repository
- [ ] Set up backend locally
- [ ] Run database migration
- [ ] Test API endpoints in Swagger

**Member 3:**
- [ ] Review API contract document
- [ ] Set up Flutter development environment
- [ ] Create Flutter project structure
- [ ] Design initial UI mockups

**Members 4 & 5:**
- [ ] Research pest detection datasets
- [ ] Discuss ML approach (CNN, transfer learning, etc.)
- [ ] Set up ML development environment
- [ ] Create ML project structure

---

#### 5. Communication Setup (10 minutes)

**Set up tools:**
- [ ] Create Slack/Discord workspace
- [ ] Create channels (#backend, #frontend, #ml, etc.)
- [ ] Set up GitHub Projects board
- [ ] Schedule daily standup time
- [ ] Schedule weekly sync time

**Agree on:**
- Response time expectations
- Meeting times (consider time zones)
- Preferred communication methods

---

#### 6. Next Steps & First Sprint (10 minutes)

**Week 3 Goals:**

**Member 1:**
- [ ] Start authentication system (Task 1.1)
- [ ] Install JWT dependencies
- [ ] Create JWT utilities

**Member 2:**
- [ ] Study backend codebase
- [ ] Understand database models
- [ ] Review FastAPI documentation
- [ ] Prepare for sensor API (Task 1.2)

**Member 3:**
- [ ] Create UI mockups for all screens
- [ ] Set up Flutter project
- [ ] Install dependencies
- [ ] Create folder structure

**Members 4 & 5:**
- [ ] Collect pest images (target: 200 images)
- [ ] Research model architectures
- [ ] Set up Jupyter notebooks
- [ ] Create dataset structure

---

#### 7. Questions & Discussion (5 minutes)

**Open floor for:**
- Any questions about the project
- Concerns or blockers
- Suggestions for improvement
- Schedule next meeting

---

### Meeting Notes Template

```markdown
# AgriSense Team Meeting - Week X

**Date:** January 10, 2026  
**Time:** 3:00 PM - 4:00 PM  
**Attendees:** Member 1, Member 2, Member 3, Member 4, Member 5

## Agenda Items

### 1. Introductions
- Member 1: Backend Lead, 5 years Python experience
- Member 2: Backend Dev, 2 years FastAPI experience
- Member 3: Flutter Dev, 3 years mobile development
- Member 4: ML Engineer, 2 years deep learning
- Member 5: ML Engineer, 3 years model deployment

### 2. Project Overview
- Member 1 demonstrated current backend setup
- Showed Swagger UI with health check endpoint
- Explained dual core features

### 3. Role Assignment
- All members confirmed their roles
- No concerns raised
- Member 3 requested API documentation - Member 1 will provide

### 4. Setup Tasks
- All members received GitHub access
- Slack workspace created
- GitHub Projects board set up

### 5. Communication
- Daily standup: 9:00 AM on Slack
- Weekly sync: Friday 3:00 PM on Zoom
- Response time: Within 4 hours for Slack messages

### 6. Next Steps
- Week 3 goals assigned to all members
- Next meeting: Friday, January 17, 3:00 PM

## Action Items
- [ ] Member 1: Share API documentation link
- [ ] Member 2: Set up backend locally by Monday
- [ ] Member 3: Share UI mockups by Wednesday
- [ ] Members 4 & 5: Share dataset plan by Tuesday

## Decisions Made
- Using Slack for daily communication
- Using GitHub Projects for task tracking
- Weekly demos every Friday

## Next Meeting
- Date: Friday, January 17, 2026
- Time: 3:00 PM
- Agenda: Demo Week 3 progress, discuss Week 4 tasks
```

---

## ✅ Best Practices

### 1. Code Quality

**Write Clean Code:**
```python
# Good: Clear, descriptive names
def get_sensor_readings_for_user(user_id: int, limit: int = 100):
    """Get sensor readings for a specific user"""
    return db.query(SensorReading)\
        .filter(SensorReading.user_id == user_id)\
        .limit(limit)\
        .all()

# Bad: Unclear, abbreviated names
def get_sr(u, l=100):
    return db.query(SR).filter(SR.u == u).limit(l).all()
```

**Add Comments:**
```python
# Good: Explain WHY, not WHAT
# Check if soil moisture is below threshold to prevent crop damage
if reading.soil_moisture < 40:
    generate_alert(user, "Low soil moisture")

# Bad: Obvious comment
# Check if soil moisture is less than 40
if reading.soil_moisture < 40:
    generate_alert(user, "Low soil moisture")
```

**Use Type Hints:**
```python
# Good: Type hints help catch errors
def calculate_average_temperature(
    readings: list[SensorReading]
) -> float:
    return sum(r.temperature for r in readings) / len(readings)

# Bad: No type information
def calculate_average_temperature(readings):
    return sum(r.temperature for r in readings) / len(readings)
```

---

### 2. Git Best Practices

**Commit Often:**
```bash
# Good: Small, focused commits
git commit -m "Add temperature validation"
git commit -m "Add humidity validation"
git commit -m "Add soil moisture validation"

# Bad: One huge commit
git commit -m "Add all validations"
```

**Write Good Commit Messages:**
```bash
# Good: Clear and descriptive
git commit -m "feat: add JWT token expiration check"
git commit -m "fix: resolve sensor reading timestamp issue"
git commit -m "docs: update API documentation for alerts"

# Bad: Vague and unhelpful
git commit -m "update"
git commit -m "fix bug"
git commit -m "changes"
```

**Pull Before Push:**
```bash
# Always pull latest changes before pushing
git pull origin develop
git push origin feature/your-feature
```

---

### 3. Code Review

**For PR Author:**
- Write clear PR description
- Add screenshots for UI changes
- Respond to comments promptly
- Don't take feedback personally

**For Reviewers:**
- Review within 24 hours
- Be constructive and specific
- Suggest improvements, don't just criticize
- Approve if code meets standards

**PR Template:**
```markdown
## What does this PR do?
Implements JWT authentication for login endpoint

## How to test?
1. Start backend server
2. Go to /docs
3. Try POST /api/v1/auth/login
4. Verify token is returned

## Screenshots
(if applicable)

## Checklist
- [x] Code follows style guidelines
- [x] Tests added/updated
- [x] Documentation updated
- [x] No breaking changes
```

---

### 4. Testing

**Write Tests:**
```python
# backend/tests/test_auth.py

def test_register_user(client):
    """Test user registration"""
    response = client.post(
        "/api/v1/auth/register",
        json={"username": "testuser", "password": "testpass123"}
    )
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"

def test_login_user(client):
    """Test user login"""
    # First register
    client.post(
        "/api/v1/auth/register",
        json={"username": "testuser", "password": "testpass123"}
    )
    
    # Then login
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "testuser", "password": "testpass123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
```

**Test Before Pushing:**
```bash
# Run tests before creating PR
pytest
flutter test

# Fix any failing tests
# Then push
```

---

### 5. Documentation

**Document Your Code:**
```python
def generate_weather_alert(
    user: User,
    forecast: dict,
    db: Session
) -> Alert:
    """
    Generate weather-based alert for user
    
    Args:
        user: User to send alert to
        forecast: Weather forecast data from OpenWeatherMap
        db: Database session
    
    Returns:
        Created Alert object
    
    Example:
        >>> forecast = {"precipitation": 65, "date": "2026-01-05"}
        >>> alert = generate_weather_alert(user, forecast, db)
        >>> alert.title
        'Heavy Rain Warning'
    """
    # Implementation...
```

**Update Documentation:**
- Update API_CONTRACT.md when changing endpoints
- Update README.md when adding features
- Update comments when changing logic

---

### 6. Communication

**Be Responsive:**
- Check Slack at least twice daily
- Respond to mentions within 4 hours
- Update team if you'll be unavailable

**Be Clear:**
```
# Good: Specific and actionable
"The sensor API is returning 500 error when temperature is null. 
I think we need to add validation in routers/sensors.py line 45. 
Can you take a look?"

# Bad: Vague and unhelpful
"Something is broken with sensors"
```

**Ask for Help:**
```
# Good: Show what you've tried
"I'm stuck on the ML integration. I've tried calling the API 
with requests.post() but getting connection refused error. 
I've checked that the ML server is running on port 5001. 
Any ideas?"

# Bad: No context
"ML integration not working, help!"
```

---

### 7. Time Management

**Set Realistic Goals:**
- Don't overcommit
- Break large tasks into smaller ones
- Communicate if you're behind schedule

**Track Your Time:**
```
Monday:
- 2 hours: Implemented login endpoint
- 1 hour: Wrote tests
- 1 hour: Code review for Member 2

Tuesday:
- 3 hours: Implemented alert system
- 1 hour: Updated documentation
```

**Avoid Burnout:**
- Take breaks
- Don't work late nights consistently
- Ask for help when overwhelmed

---

## 🎯 Success Criteria

### Project Success Metrics

**Technical:**
- [ ] All API endpoints working
- [ ] Mobile app runs on Android/iOS
- [ ] ML model accuracy >80%
- [ ] No critical bugs
- [ ] Code coverage >70%

**Team:**
- [ ] All members contributed
- [ ] Good communication maintained
- [ ] Deadlines met
- [ ] Code reviews completed
- [ ] Documentation complete

**Learning:**
- [ ] Each member learned new skills
- [ ] Best practices followed
- [ ] Knowledge shared within team
- [ ] Challenges overcome together

---

## 📞 Contact Information

### Team Members

| Member | Role | Email | GitHub | Availability |
|--------|------|-------|--------|--------------|
| Member 1 | Backend Lead | member1@email.com | @member1 | Mon-Fri 9AM-5PM |
| Member 2 | Backend Dev | member2@email.com | @member2 | Mon-Fri 10AM-6PM |
| Member 3 | Flutter Dev | member3@email.com | @member3 | Mon-Fri 9AM-5PM |
| Member 4 | ML Engineer | member4@email.com | @member4 | Mon-Fri 2PM-10PM |
| Member 5 | ML Engineer | member5@email.com | @member5 | Mon-Fri 1PM-9PM |

---

## 📚 Additional Resources

### Learning Resources

**Backend (FastAPI):**
- Official Docs: https://fastapi.tiangolo.com/
- Tutorial: https://fastapi.tiangolo.com/tutorial/
- SQLAlchemy: https://docs.sqlalchemy.org/

**Frontend (Flutter):**
- Official Docs: https://flutter.dev/docs
- Cookbook: https://flutter.dev/docs/cookbook
- Packages: https://pub.dev/

**Machine Learning:**
- TensorFlow: https://www.tensorflow.org/tutorials
- PyTorch: https://pytorch.org/tutorials/
- Pest Detection Papers: (to be added by ML team)

**Git & GitHub:**
- Git Handbook: https://guides.github.com/introduction/git-handbook/
- GitHub Flow: https://guides.github.com/introduction/flow/

---

## 🔄 Document Updates

This document will be updated as the project progresses.

**Version History:**
- v1.0 (2026-01-04): Initial version created
- v1.1 (TBD): Updated after first team meeting
- v1.2 (TBD): Updated with team decisions

**Last Updated:** January 4, 2026  
**Next Review:** After first team meeting

---

## ✅ Acknowledgments

This collaboration guide was created to ensure smooth teamwork and successful project delivery for the AgriSense capstone project.

**Good luck, team! Let's build something amazing! 🚀🌱**
