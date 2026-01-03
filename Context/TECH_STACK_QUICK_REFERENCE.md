# AgriSense Tech Stack - Quick Reference Card

**Version**: 2.1  
**Last Updated**: 2025-01-03  
**Print this and keep it handy!** 📌

---

## 🏗️ Architecture (One Glance)

```
Flutter Mobile App (Dart)
        ↓ REST API (HTTPS)
FastAPI Backend (Python 3.10+)
        ↓
PostgreSQL Database (or SQLite for dev)
        ↓
Your Own Server (Docker)
```

---

## 📱 Mobile App Stack

| Component | Technology | Version |
|-----------|------------|---------|
| **Framework** | Flutter | Latest stable |
| **Language** | Dart | 3.x |
| **HTTP Client** | Dio | ^5.0.0 |
| **State Management** | Provider | ^6.0.0 |
| **Image Picker** | image_picker | ^1.0.0 |
| **Secure Storage** | flutter_secure_storage | ^9.0.0 |
| **UI Components** | Material Design | Built-in |

**Key Commands:**
```bash
flutter create agrisense_mobile
flutter pub get
flutter run
flutter build apk
```

---

## 🔙 Backend Stack

| Component | Technology | Version |
|-----------|------------|---------|
| **Framework** | FastAPI | 0.109.0 |
| **Language** | Python | 3.10+ |
| **Server** | Uvicorn | 0.27.0 |
| **ORM** | SQLAlchemy | 2.0.25 |
| **Validation** | Pydantic | 2.5.0 |
| **Auth** | python-jose | 3.3.0 |
| **Password Hash** | passlib[bcrypt] | 1.7.4 |

**Key Commands:**
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
alembic upgrade head
pytest
```

**API Docs:** `http://localhost:8000/docs` (Swagger UI)

---

## 🗄️ Database Stack

| Environment | Database | Why |
|-------------|----------|-----|
| **Development** | SQLite | Zero setup, fast iteration |
| **Production** | PostgreSQL 15 | Production-grade, ACID |

**Connection Strings:**
```python
# Development
DATABASE_URL = "sqlite:///./agrisense.db"

# Production
DATABASE_URL = "postgresql://user:pass@host:5432/agrisense_db"
```

**Key Commands:**
```bash
# SQLite
sqlite3 agrisense.db

# PostgreSQL
psql -U agrisense_user -d agrisense_db
docker exec -it agrisense-db psql
```

---

## ☁️ Deployment Stack

| Environment | Platform | Cost | Setup Time |
|-------------|----------|------|------------|
| **Primary** | Your Own Server | $0 | 20 min |
| **Backup** | Render.com | Free tier | 15 min |
| **Backup 2** | Railway.app | $5/month free | 10 min |

**Your Server Setup:**
```bash
# 1. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 2. Clone & Deploy
git clone https://github.com/you/agrisense.git
cd agrisense
docker-compose up -d

# 3. Check Status
docker-compose ps
```

**Access:**
- Backend: `http://your-server-ip:8000`
- Swagger: `http://your-server-ip:8000/docs`

---

## 🔐 Security Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Passwords** | bcrypt | Hash passwords |
| **Auth** | JWT | Stateless tokens |
| **HTTPS** | Let's Encrypt | Free SSL |
| **Validation** | Pydantic | Input validation |
| **Rate Limit** | slowapi | Prevent abuse |

**JWT Token Example:**
```python
from jose import jwt

token = jwt.encode(
    {"sub": user_id, "exp": expiry},
    SECRET_KEY,
    algorithm="HS256"
)
```

---

## 🤖 ML Integration Stack

| Phase | Strategy | Technology |
|-------|----------|------------|
| **Week 1-6** | Mock Service | Python random predictions |
| **Week 7-10** | Real Model | ML Team's TensorFlow/PyTorch |
| **Backup** | Pre-trained | Roboflow API / Hugging Face |

**Mock Service:**
```python
def mock_detect_pest():
    return {
        "pest_name": "Stem Borer",
        "confidence": 0.87,
        "risk_level": "high"
    }
```

---

## 🌤️ Weather Stack

| Service | OpenWeatherMap API |
|---------|-------------------|
| **Tier** | Free (1000 calls/day) |
| **Endpoint** | `api.openweathermap.org/data/2.5/onecall` |
| **Data** | 7-day forecast |

**API Call:**
```python
import requests

url = f"https://api.openweathermap.org/data/2.5/onecall"
params = {
    "lat": 3.1390,
    "lon": 101.6869,
    "appid": API_KEY,
    "units": "metric"
}
response = requests.get(url, params=params)
```

---

## 📡 Communication Pattern

**What You're Using:** REST API + Polling

```dart
// Flutter: Poll every 30 seconds
Timer.periodic(Duration(seconds: 30), (timer) {
  fetchSensorData();
});

// Pull to refresh
RefreshIndicator(
  onRefresh: fetchSensorData,
  child: Dashboard(),
);
```

**What You're NOT Using:**
- ❌ WebSockets
- ❌ Server-Sent Events (SSE)
- ❌ Webhooks
- ❌ GraphQL

---

## 🛠️ Development Tools

| Tool | Required? | Purpose |
|------|-----------|---------|
| Python 3.10+ | ✅ Yes | Backend |
| Flutter SDK | ✅ Yes | Mobile |
| Docker Desktop | ✅ Yes | Deployment |
| PostgreSQL | ✅ Yes | Database |
| VS Code | ⭐ Recommended | Editor |
| GitHub Copilot | ⭐ Recommended | AI assist |
| DBeaver | ⚠️ Optional | DB GUI |

---

## 📦 Installation Cheat Sheet

**Backend:**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn sqlalchemy pydantic python-jose passlib[bcrypt] python-multipart requests pillow slowapi alembic

# Or use requirements.txt
pip install -r requirements.txt
```

**Mobile:**
```bash
# Create Flutter project
flutter create agrisense_mobile
cd agrisense_mobile

# Add dependencies to pubspec.yaml, then:
flutter pub get
```

**Database:**
```bash
# SQLite (nothing to install!)
# Just use: sqlite3 agrisense.db

# PostgreSQL with Docker
docker run --name agrisense-db \
  -e POSTGRES_PASSWORD=dev123 \
  -p 5432:5432 \
  -d postgres:15
```

---

## 🚀 Quick Start (Day 1)

**Backend (10 minutes):**
```bash
mkdir -p backend/app
cd backend
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn
echo 'from fastapi import FastAPI\napp = FastAPI()\n@app.get("/")\ndef root():\n    return {"message": "AgriSense API"}' > app/main.py
uvicorn app.main:app --reload
# Visit: http://localhost:8000/docs
```

**Mobile (10 minutes):**
```bash
flutter create agrisense_mobile
cd agrisense_mobile
flutter run
# See "Hello World" on device
```

**Test Connection (5 minutes):**
```dart
// In Flutter, call your API
final response = await http.get('http://localhost:8000/');
print(response.body);  // Should see: {"message": "AgriSense API"}
```

---

## 🔄 Common Commands

**Backend:**
```bash
# Run development server
uvicorn app.main:app --reload

# Run tests
pytest

# Create database migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Check API docs
open http://localhost:8000/docs
```

**Mobile:**
```bash
# Run on device
flutter run

# Hot reload (in running app)
# Press 'r' in terminal

# Build APK
flutter build apk --release

# Run tests
flutter test

# Clean build
flutter clean && flutter pub get
```

**Docker:**
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop all services
docker-compose down

# Rebuild after code changes
docker-compose up -d --build
```

---

## 🐛 Debugging Checklist

**Backend not starting?**
- [ ] Virtual environment activated?
- [ ] Dependencies installed? (`pip list`)
- [ ] Port 8000 available? (`lsof -i :8000`)
- [ ] Database running? (`docker ps`)

**Mobile can't connect to API?**
- [ ] Backend running? (check `http://localhost:8000/docs`)
- [ ] Correct API URL? (localhost vs IP address)
- [ ] CORS enabled in backend?
- [ ] Using HTTP (not HTTPS) for local dev?

**Database errors?**
- [ ] Database created? (`CREATE DATABASE agrisense_db`)
- [ ] Migrations applied? (`alembic upgrade head`)
- [ ] Connection string correct?
- [ ] PostgreSQL running? (`docker ps`)

---

## 📊 Tech Stack Rating Summary

| Component | Rating | Status |
|-----------|--------|--------|
| Flutter | ⭐⭐⭐⭐⭐ | Perfect choice |
| FastAPI | ⭐⭐⭐⭐⭐ | Excellent (Flask backup) |
| PostgreSQL | ⭐⭐⭐⭐ | Good (SQLite for dev) |
| Your Server | ⭐⭐⭐⭐⭐ | Better than Azure |
| JWT Auth | ⭐⭐⭐⭐⭐ | Industry standard |
| OpenWeatherMap | ⭐⭐⭐⭐⭐ | Reliable & free |
| Python Data Gen | ⭐⭐⭐⭐⭐ | Simple & effective |

**Overall: 4.9/5** - Excellent tech stack! 🎉

---

## 💡 Pro Tips

1. **Start with SQLite** - Don't waste time setting up PostgreSQL on Day 1
2. **Use Swagger UI** - Test all APIs at `/docs` before writing mobile code
3. **Commit often** - Small commits = easy to debug
4. **Deploy early** - Week 6, even if incomplete
5. **Mock ML first** - Don't wait for ML team
6. **Use AI assistants** - GitHub Copilot, ChatGPT, Claude
7. **Keep it simple** - REST + polling works great

---

## 📞 Quick Help

**Stuck on code?**
1. Read error message carefully
2. Google exact error
3. Ask AI: "Why am I getting [error]?"
4. Check Stack Overflow
5. Read official docs

**Stuck on decisions?**
1. Choose simpler option
2. Timebox research (max 2 hours)
3. Ask supervisor
4. Look at similar projects on GitHub

---

## ✅ Phase 0 Checklist (Week 1-2)

- [ ] Install Python 3.10+
- [ ] Install Flutter SDK
- [ ] Install Docker Desktop
- [ ] Install VS Code
- [ ] Create GitHub repository
- [ ] Run "Hello World" FastAPI
- [ ] Run "Hello World" Flutter
- [ ] Test mobile → backend connection
- [ ] Set up SQLite database
- [ ] Create first API endpoint
- [ ] Call API from Flutter
- [ ] Commit to GitHub

**When all checked:** You're ready for Phase 1! 🚀

---

**Keep this card handy during development!**

For full details, see: `agrisense_handover_v2.md`
