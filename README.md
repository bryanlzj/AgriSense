# 🌾 AgriSense

**IoT-Driven Agricultural Monitoring System for Malaysian Farmers**

AgriSense is a mobile application that helps farmers monitor their crops through AI-powered pest detection, environmental monitoring, and weather forecasting. Built as a simulation-based system for educational purposes.

---

## 📱 Project Overview

AgriSense provides farmers with:
- 🐛 **AI Pest Detection** - Upload crop images to identify pest infestations
- 🌡️ **Environmental Monitoring** - Track temperature, humidity, and soil moisture
- ⛅ **Weather Forecasting** - 7-day weather predictions
- 🔔 **Smart Alerts** - Notifications for pest risks and weather warnings
- 📊 **Historical Data** - View trends and past detections

**Note:** This is a simulation-based system using synthetic sensor data - no physical IoT hardware required.

---

## 🛠️ Technology Stack

### **Backend**
- **Framework:** FastAPI (Python 3.10+)
- **Database:** PostgreSQL (production) / SQLite (development)
- **Authentication:** JWT (JSON Web Tokens)
- **ORM:** SQLAlchemy
- **Migrations:** Alembic
- **API Docs:** Swagger UI (auto-generated)

### **Mobile App**
- **Framework:** Flutter (Dart)
- **State Management:** Provider / Riverpod
- **HTTP Client:** Dio
- **Storage:** SharedPreferences (JWT tokens)
- **Platforms:** Android & iOS

### **External Services**
- **Weather API:** OpenWeatherMap
- **ML Service:** Mock service → Real model → Roboflow (backup)

### **Deployment**
- **Backend:** Self-hosted server with Docker
- **Database:** PostgreSQL on server
- **Mobile:** APK distribution

---

## 📁 Project Structure

```
agrisense/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py         # FastAPI application entry
│   │   ├── models/         # SQLAlchemy models
│   │   ├── routes/         # API endpoints
│   │   ├── services/       # Business logic
│   │   ├── schemas/        # Pydantic schemas
│   │   └── utils/          # Helper functions
│   ├── alembic/            # Database migrations
│   ├── tests/              # Backend tests
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment variables template
│
├── mobile/                 # Flutter mobile app
│   ├── lib/
│   │   ├── main.dart       # App entry point
│   │   ├── screens/        # UI screens
│   │   ├── widgets/        # Reusable widgets
│   │   ├── services/       # API services
│   │   ├── models/         # Data models
│   │   └── utils/          # Helper functions
│   ├── assets/             # Images, fonts, etc.
│   ├── test/               # Mobile tests
│   └── pubspec.yaml        # Flutter dependencies
│
├── docs/                   # Documentation
│   ├── api/                # API documentation
│   ├── architecture/       # System design docs
│   └── user-guide/         # User manuals
│
├── .references/            # Project references
│   ├── prd/                # Product Requirements Document
│   └── tasks/              # Task list and tracking
│
└── Context/                # Project context and handover docs

```

---

## 🚀 Getting Started

### **Prerequisites**
- Python 3.10+
- Flutter SDK 3.0+
- PostgreSQL 14+ (or SQLite for development)
- Git

### **Backend Setup**

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run database migrations:**
   ```bash
   alembic upgrade head
   ```

6. **Start development server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

7. **Access API documentation:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### **Mobile Setup**

1. **Navigate to mobile directory:**
   ```bash
   cd mobile
   ```

2. **Install dependencies:**
   ```bash
   flutter pub get
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with backend API URL
   ```

4. **Run on emulator/device:**
   ```bash
   flutter run
   ```

5. **Build APK (Android):**
   ```bash
   flutter build apk --release
   ```

---

## 📚 API Documentation

Once the backend is running, access the interactive API documentation:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### **Key Endpoints:**

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login and get JWT token |
| GET | `/api/sensors/current` | Get current sensor readings |
| GET | `/api/sensors/history` | Get historical sensor data |
| POST | `/api/detections/upload` | Upload image for pest detection |
| GET | `/api/detections/history` | Get detection history |
| GET | `/api/weather/forecast` | Get 7-day weather forecast |
| GET | `/api/alerts` | Get user alerts |
| PUT | `/api/alerts/{id}/read` | Mark alert as read |

---

## 🧪 Testing

### **Backend Tests**
```bash
cd backend
pytest tests/ -v --cov=app
```

### **Mobile Tests**
```bash
cd mobile
flutter test
```

---

## 🐳 Docker Deployment

### **Backend with Docker:**

1. **Build image:**
   ```bash
   cd backend
   docker build -t agrisense-backend .
   ```

2. **Run container:**
   ```bash
   docker run -d -p 8000:8000 \
     -e DATABASE_URL=postgresql://user:pass@host/db \
     -e JWT_SECRET=your-secret-key \
     agrisense-backend
   ```

### **Docker Compose (Full Stack):**
```bash
docker-compose up -d
```

---

## 🔐 Environment Variables

### **Backend (.env)**
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/agrisense
# or for SQLite: sqlite:///./agrisense.db

# JWT Authentication
JWT_SECRET_KEY=your-super-secret-key-change-this
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=1440

# OpenWeatherMap API
OPENWEATHER_API_KEY=your-api-key-here

# ML Service
ML_SERVICE_URL=http://localhost:5001
ML_SERVICE_ENABLED=false

# File Upload
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE_MB=10
```

### **Mobile (.env)**
```env
API_BASE_URL=http://localhost:8000
API_TIMEOUT_SECONDS=30
```

---

## 📖 Documentation

- **PRD:** `.references/prd/agrisense-prd.md` - Complete product requirements
- **Task List:** `.references/tasks/agrisense-tasks.md` - Development tasks
- **Handover:** `Context/agrisense_handover_v2.md` - Project context and decisions
- **API Docs:** Available at `/docs` when backend is running

---

## 🎯 Development Roadmap

### **Phase 0: Setup** ✅ (Current)
- [x] Project structure
- [ ] Backend scaffolding
- [ ] Database setup
- [ ] Mobile app initialization

### **Phase 1: Backend Development** (Weeks 1-8)
- [ ] Authentication system
- [ ] Sensor data API
- [ ] Pest detection API
- [ ] Weather integration
- [ ] Alert system

### **Phase 2: Mobile Development** (Weeks 9-12)
- [ ] Authentication screens
- [ ] Dashboard UI
- [ ] Pest detection flow
- [ ] Alerts & notifications

### **Phase 3: Integration** (Weeks 13-14)
- [ ] ML model integration
- [ ] End-to-end testing
- [ ] Deployment
- [ ] Demo preparation

---

## 🤝 Contributing

This is a capstone project for educational purposes. For questions or suggestions:

1. Review the PRD and task list in `.references/`
2. Follow the coding standards in `.instructions/`
3. Ensure all tests pass before committing
4. Update documentation for new features

---

## 📄 License

This project is developed for educational purposes as part of a Bachelor of Software Engineering capstone project.

---

## 👥 Team

**Integration Lead** - Backend, Mobile, ML Integration

**ML Team** - Pest detection model training

**Project Type** - Final Year Capstone Project (Bachelor of Software Engineering)

---

## 🙏 Acknowledgments

- OpenWeatherMap for weather data API
- Roboflow for ML model hosting (backup)
- Flutter and FastAPI communities
- Malaysian farmers for inspiration

---

## 📞 Support

For issues or questions:
- Check the documentation in `/docs`
- Review the handover document in `/Context`
- Refer to API documentation at `/docs` endpoint

---

**Built with ❤️ for Malaysian farmers** 🇲🇾🌾
