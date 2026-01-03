# AgriSense Project Context & Handover Document v2.0

## Project Overview
AgriSense is a **simulation-based** IoT agricultural monitoring system for Malaysian farmers. This is a final year student project focused on building a **functional mobile application** with backend services that demonstrates precision agriculture concepts using **simulated/synthetic data only**.

## ⚠️ CRITICAL CLARIFICATIONS

### What This Project IS
- A **mobile-first application** (Flutter) for agricultural monitoring
- A **fully simulated system** - NO physical IoT hardware whatsoever
- A **proof-of-concept** demonstrating data-driven farming decisions
- An **AI-assisted development project** (using AI coding assistants is permitted and encouraged)
- A **learning project** where team has theoretical knowledge but limited practical experience

### What This Project IS NOT
- ❌ A real IoT deployment with physical sensors
- ❌ A research project requiring novel ML algorithms
- ❌ An enterprise-grade production system
- ❌ A hardware engineering project
- ❌ A system that will be used by real farmers (it's a demo/prototype)

---

## 🔧 COMPLETE TECH STACK OVERVIEW

### Architecture Summary

```
┌─────────────────────────────────────────────────────────────┐
│                    MOBILE APP LAYER                          │
│  Flutter (Dart) + Material Design                            │
│  - Camera integration (image_picker)                         │
│  - HTTP client (dio)                                         │
│  - State management (Provider/Riverpod)                      │
│  - Secure storage (flutter_secure_storage)                  │
└─────────────────────────────────────────────────────────────┘
                          ↓ HTTPS/REST API
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND API LAYER                         │
│  FastAPI (Python 3.10+) [Primary]                           │
│  Flask (Python 3.10+) [Backup if FastAPI too complex]       │
│  - Auto-generated Swagger docs (/docs)                      │
│  - Pydantic validation                                       │
│  - JWT authentication (python-jose)                          │
│  - Async file uploads                                        │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                    BUSINESS LOGIC LAYER                      │
│  - Synthetic data generator (Python script)                 │
│  - ML integration service (mock → real → backup)            │
│  - Weather API client (OpenWeatherMap)                      │
│  - Alert generation logic                                    │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                    DATA LAYER                                │
│  PostgreSQL 15 (Production)                                  │
│  SQLite (Development - Recommended for quick start)          │
│  - SQLAlchemy ORM                                            │
│  - Alembic migrations                                        │
│  - PostGIS extension (optional geospatial)                  │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                    ML LAYER (External)                       │
│  Option 1: ML Team's Model (TensorFlow/PyTorch)             │
│  Option 2: Roboflow API (Backup)                             │
│  Option 3: Hugging Face Pre-trained (Backup)                │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                    DEPLOYMENT LAYER                          │
│  Development: Local Docker / Evo Builder                    │
│  Production: Your Own Server (Primary)                      │
│  Backup: Render.com / Railway.app                           │
│  Database: PostgreSQL on server / Render PostgreSQL         │
│  Mobile: APK distribution (no app store)                    │
└─────────────────────────────────────────────────────────────┘
```

### Tech Stack Decisions & Rationale

| Component | Choice | Rating | Rationale |
|-----------|--------|--------|-----------|
| **Mobile Framework** | Flutter | ⭐⭐⭐⭐⭐ | Cross-platform (Android/iOS), single codebase, excellent camera support, perfect for student projects |
| **Backend Framework** | FastAPI (Flask backup) | ⭐⭐⭐⭐⭐ | Auto-generated docs (critical for demos), modern Python, async support for ML, easy AI-assisted development |
| **Database** | PostgreSQL (SQLite dev) | ⭐⭐⭐⭐ | Production-grade, ACID compliance, PostGIS for geospatial. **Start with SQLite for faster development** |
| **Cloud/Hosting** | Your Own Server | ⭐⭐⭐⭐⭐ | Free, full control, real DevOps learning, no vendor lock-in. **Much better than Azure for student projects** |
| **Authentication** | JWT + bcrypt | ⭐⭐⭐⭐⭐ | Industry standard, stateless, mobile-friendly, secure |
| **ML Strategy** | Mock → Real → Backup | ⭐⭐⭐⭐⭐ | Risk mitigation, not blocked by ML team, multiple fallback options |
| **Data Simulation** | Python script | ⭐⭐⭐⭐⭐ | Simple, controllable, no external dependencies, perfect for student project |
| **Weather Data** | OpenWeatherMap API | ⭐⭐⭐⭐⭐ | Free tier sufficient, reliable, Malaysian locations supported |
| **Image Storage** | Server filesystem / Cloudinary | ⭐⭐⭐⭐ | Simple file storage on server, or Cloudinary free tier (25GB) for CDN benefits |

### Key Technology Choices Explained

#### Why FastAPI over Flask?
- ✅ **Auto-generated API documentation** (Swagger UI at `/docs`) - HUGE for demos and testing
- ✅ **Automatic validation** (Pydantic) - catches errors before they reach your code
- ✅ **Async support** - handles ML inference without blocking other requests
- ✅ **Modern Python** - type hints make code clearer and AI assistants work better
- ✅ **Faster development** - less boilerplate code
- ⚠️ **Backup Plan**: Switch to Flask if struggling after Week 3 (simpler, more tutorials)

#### Why Your Own Server over Azure?
- ✅ **$0 cost** vs Azure credits that run out
- ✅ **20 minutes setup** vs 2-3 days learning Azure
- ✅ **Full control** vs limited by cloud policies
- ✅ **Real DevOps skills** vs cloud-specific knowledge
- ✅ **No complexity** - just Docker Compose vs Resource Groups, VNETs, IAM
- ✅ **Better for resume** - self-hosted shows real infrastructure knowledge

#### Why SQLite for Development?
- ✅ **Zero setup** - just a file, no Docker needed
- ✅ **Fast iteration** - no connection pooling, no network latency
- ✅ **Easy debugging** - use DB Browser to inspect data
- ✅ **Perfect for prototyping** - switch to PostgreSQL later (just change URL)
- ⚠️ **Migrate to PostgreSQL** by Week 9 for production features

#### Why Flutter over React Native?
- ✅ **Better performance** - compiles to native ARM/x64
- ✅ **Rich widget library** - Material Design built-in
- ✅ **Excellent camera support** - critical for pest detection
- ✅ **Single codebase** - Android + iOS (though you'll focus on Android)
- ✅ **Hot reload** - see changes instantly
- ✅ **AI assistants know Flutter well** - good code generation

### Development Tools

| Tool | Purpose | Required? |
|------|---------|-----------|
| **Python 3.10+** | Backend development | ✅ Yes |
| **Flutter SDK** | Mobile development | ✅ Yes |
| **Docker Desktop** | Local deployment | ✅ Yes |
| **PostgreSQL** | Database (or SQLite) | ✅ Yes |
| **VS Code** | Code editor | ⭐ Recommended |
| **Postman/Insomnia** | API testing | ⚠️ Optional (Swagger UI sufficient) |
| **DBeaver/pgAdmin** | Database GUI | ⚠️ Optional (helpful for debugging) |
| **GitHub Copilot** | AI code assistant | ⭐ Highly Recommended |

### External Services & APIs

| Service | Purpose | Cost | Required? |
|---------|---------|------|-----------|
| **OpenWeatherMap** | Weather forecast | Free (1000 calls/day) | ✅ Yes |
| **Cloudinary** | Image hosting (optional) | Free (25GB) | ⚠️ Optional |
| **Roboflow** | ML backup plan | Free (1000 predictions/month) | ⚠️ Backup only |
| **Render.com** | Deployment backup | Free tier | ⚠️ Backup only |
| **GitHub** | Version control | Free | ✅ Yes |

### Package Dependencies

**Backend (Python):**
```txt
fastapi==0.109.0          # Web framework
uvicorn==0.27.0           # ASGI server
sqlalchemy==2.0.25        # ORM
alembic==1.13.0           # Database migrations
pydantic==2.5.0           # Data validation
python-jose[cryptography]==3.3.0  # JWT
passlib[bcrypt]==1.7.4    # Password hashing
python-multipart==0.0.6   # File uploads
requests==2.31.0          # HTTP client (for weather API)
pillow==10.1.0            # Image processing
slowapi==0.1.9            # Rate limiting
```

**Mobile (Flutter):**
```yaml
dependencies:
  flutter:
    sdk: flutter
  dio: ^5.0.0                      # HTTP client
  provider: ^6.0.0                 # State management
  flutter_secure_storage: ^9.0.0  # JWT storage
  image_picker: ^1.0.0             # Camera/gallery
  cached_network_image: ^3.0.0    # Image caching
  google_fonts: ^6.0.0             # Typography
  flutter_spinkit: ^5.0.0          # Loading indicators
  fluttertoast: ^8.0.0             # Toast messages
  intl: ^0.18.0                    # Date formatting
```

### Communication Patterns

**What You're Using: Simple REST API + Polling** ✅
```
Mobile App → (every 30 seconds) → GET /api/sensors → Backend → Database
Mobile App → (pull to refresh) → GET /api/sensors → Backend → Database
Mobile App → (user action) → POST /api/pests/detect → Backend → ML Service
```

**What You're NOT Using:**
- ❌ **WebSockets** - Too complex, battery drain, overkill for your use case
- ❌ **Server-Sent Events (SSE)** - Continuous streaming not needed
- ❌ **Webhooks** - Mobile apps can't receive webhooks (no public URL)
- ❌ **GraphQL** - REST is simpler and sufficient

**Why Simple Polling is Perfect:**
- ✅ Works 100% of the time (no connection issues)
- ✅ Battery efficient (only fetches when app is open)
- ✅ Easy to debug (just HTTP requests)
- ✅ Works offline (graceful degradation)
- ✅ What 95% of mobile apps use

### Security Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Password Hashing** | bcrypt (via passlib) | Secure password storage |
| **Authentication** | JWT (python-jose) | Stateless auth tokens |
| **HTTPS/TLS** | Let's Encrypt (free SSL) | Encrypted communication |
| **Input Validation** | Pydantic (FastAPI) | Prevent injection attacks |
| **Rate Limiting** | slowapi | Prevent abuse |
| **CORS** | FastAPI middleware | Control API access |
| **File Validation** | Custom logic | Prevent malicious uploads |

---

## 🎯 REVISED SCOPE - REALISTIC MVP

### Phase 1: Must-Have Core Features (Months 1-3)
**Goal**: One working end-to-end workflow

#### Priority 1 (Critical Path) ⭐⭐⭐
1. **User Authentication**
   - Sign up / Login / Logout
   - Simple JWT-based auth
   - Password reset via email

2. **Pest Detection Workflow** (THE CORE FEATURE)
   - Mobile app: Camera screen to capture pest image
   - Upload image to backend
   - Backend forwards to ML service (or mock)
   - Display detection results (pest name, confidence, recommendations)
   - Store results in database
   
3. **Simple Dashboard**
   - Display current "simulated" sensor readings (temperature, humidity, soil moisture)
   - Show latest pest detection results
   - Show active alerts

4. **Basic Alert System**
   - Generate alerts based on thresholds (e.g., high pest risk detected)
   - Display in-app notifications
   - Store alert history

#### Priority 2 (If Time Permits) ⭐⭐
1. **Weather Forecast Display**
   - Fetch from free weather API (OpenWeatherMap)
   - Display 7-day forecast
   - No ML prediction needed initially

2. **Historical Data View**
   - Simple list/table of past sensor readings
   - Filter by date range

3. **User Profile Management**
   - Edit profile information
   - Add farm sector details

#### Priority 3 (Nice to Have) ⭐
1. **AI Chatbot** (if using OpenRouter free tier)
2. **Data visualization charts** (simple line charts)
3. **Push notifications** (via Firebase)

### Phase 2: Cut Entirely (Move to "Future Work" section)
- ❌ Multiple farm sector management
- ❌ Admin management system
- ❌ Dataset import functionality
- ❌ Complex data visualizations
- ❌ IoT device simulation (use simple synthetic data instead)
- ❌ Training ML models from scratch

---

## 🔧 TECHNICAL DECISIONS (FINALIZED)

### 1. Simulated Sensor Data Source - DECISION MADE ✅

**RECOMMENDATION: Simple Python Synthetic Data Generator**

**Why This Approach:**
- ✅ Full control over data patterns
- ✅ No external dependencies or API costs
- ✅ Easy to modify for testing scenarios
- ✅ Can simulate realistic agricultural conditions
- ✅ ~50 lines of Python code

**Implementation Plan:**

```python
# data_simulator.py
import random
import time
from datetime import datetime
import psycopg2

def generate_sensor_reading():
    """Generate realistic sensor data"""
    
    # Base values for Malaysian tropical climate
    base_temp = 28  # Celsius
    base_humidity = 75  # Percent
    base_soil_moisture = 45  # Percent
    
    # Add realistic variations
    hour = datetime.now().hour
    
    # Temperature: warmer during day (10am-4pm)
    temp_variation = 5 if 10 <= hour <= 16 else -2
    temperature = base_temp + temp_variation + random.uniform(-2, 2)
    
    # Humidity: higher at night
    humidity_variation = -10 if 10 <= hour <= 16 else 5
    humidity = base_humidity + humidity_variation + random.uniform(-5, 5)
    
    # Soil moisture: decreases during day, increases after "rain events"
    rain_event = random.random() < 0.1  # 10% chance of rain
    if rain_event:
        soil_moisture = base_soil_moisture + random.uniform(10, 20)
    else:
        soil_moisture = base_soil_moisture + random.uniform(-5, 5)
    
    # Other sensors
    solar_radiation = random.uniform(200, 800) if 6 <= hour <= 18 else 0
    wind_speed = random.uniform(5, 20)
    
    return {
        'timestamp': datetime.now(),
        'temperature': round(temperature, 2),
        'humidity': round(humidity, 2),
        'soil_moisture': round(soil_moisture, 2),
        'solar_radiation': round(solar_radiation, 2),
        'wind_speed': round(wind_speed, 2),
        'rainfall': 0 if not rain_event else random.uniform(5, 15)
    }

def insert_to_database(data):
    """Insert simulated data into PostgreSQL"""
    conn = psycopg2.connect(
        dbname="agrisense_db",
        user="your_user",
        password="your_password",
        host="localhost"
    )
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO sensor_data 
        (sector_id, timestamp, temperature, humidity, soil_moisture, 
         solar_radiation, wind_speed, rainfall)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        'default-sector-id',  # Use actual sector ID
        data['timestamp'],
        data['temperature'],
        data['humidity'],
        data['soil_moisture'],
        data['solar_radiation'],
        data['wind_speed'],
        data['rainfall']
    ))
    
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    # Run every 5 minutes (cron job or while loop)
    while True:
        reading = generate_sensor_reading()
        insert_to_database(reading)
        print(f"[{reading['timestamp']}] Data inserted: Temp={reading['temperature']}°C, Humidity={reading['humidity']}%")
        time.sleep(300)  # 5 minutes
```

**Deployment:**
- Run as a background process on your server
- Or use cron job: `*/5 * * * * python3 /path/to/data_simulator.py`

**Alternative: Pre-seed Historical Data**
```python
# seed_historical_data.py
from datetime import datetime, timedelta

def seed_last_30_days():
    """Generate 30 days of historical data for charts"""
    start_date = datetime.now() - timedelta(days=30)
    
    for day in range(30):
        for hour in range(24):
            timestamp = start_date + timedelta(days=day, hours=hour)
            data = generate_sensor_reading()
            data['timestamp'] = timestamp
            insert_to_database(data)
    
    print("Seeded 720 historical records (30 days × 24 hours)")
```

### 2. Weather Data Source - DECISION MADE ✅

**RECOMMENDATION: Use Free Weather API (No ML Prediction Initially)**

**Option A: OpenWeatherMap API** (Recommended)
- Free tier: 1000 calls/day
- 7-day forecast included
- Malaysian locations supported
- API docs: https://openweathermap.org/api

```python
# weather_service.py
import requests

def get_weather_forecast(lat, lon):
    """Fetch 7-day forecast from OpenWeatherMap"""
    api_key = "your_free_api_key"
    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly&appid={api_key}&units=metric"
    
    response = requests.get(url)
    data = response.json()
    
    forecast = []
    for day in data['daily'][:7]:
        forecast.append({
            'date': day['dt'],
            'temp_min': day['temp']['min'],
            'temp_max': day['temp']['max'],
            'humidity': day['humidity'],
            'rainfall_prob': day.get('pop', 0) * 100,  # Probability of precipitation
            'description': day['weather'][0]['description']
        })
    
    return forecast
```

**Option B: ML Weather Prediction (Phase 2)**
- Only if ML team delivers working model
- Use as enhancement, not dependency
- Fallback to API if ML fails

### 3. Cloud Hosting - DECISION MADE ✅

**RECOMMENDATION: Use Your Own Server (Primary) + Render.com (Backup)**

**YOU HAVE YOUR OWN SERVER - This is Perfect!**

**Why Your Own Server is BETTER than Azure:**

| Aspect | Your Server | Azure Cloud |
|--------|-------------|-------------|
| **Cost** | $0 (already have it) | Credits run out, then $ |
| **Setup Time** | 20 minutes (Docker) | 2-3 days (learning curve) |
| **Control** | Full root access | Limited by policies |
| **Learning** | Real DevOps skills | Cloud-specific knowledge |
| **Demo Risk** | You control uptime | Free tier limits |
| **Complexity** | Simple (Docker Compose) | Complex (Resource Groups, VNETs) |

**Advantages:**
- ✅ **Free** (no cloud costs or credit card needed)
- ✅ **Full control** (install anything you need)
- ✅ **Real DevOps learning** (valuable for resume)
- ✅ **No vendor lock-in** (not dependent on Azure/AWS)
- ✅ **Better for demo** (no worrying about free tier limits)
- ✅ **Portable skills** (works on any cloud later)
- ✅ **Fast iteration** (no waiting for cloud deployments)

**Server Requirements:**
- Linux server (Ubuntu 22.04 recommended)
- Minimum 2GB RAM, 20GB disk space
- Public IP address
- SSH access
- (Optional) Domain name for professional URL

**Important Note:**
- Your server needs initial setup (Docker, PostgreSQL, etc.)
- This document assumes you'll set it up during Phase 0 (Week 1-2)
- Detailed setup instructions provided in deployment section below

**Complete Docker Setup for Your Server:**
```yaml
# docker-compose.yml - Deploy your entire stack in one command
version: '3.8'

services:
  postgres:
    image: postgres:15
    container_name: agrisense_db
    environment:
      POSTGRES_DB: agrisense_db
      POSTGRES_USER: agrisense_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}  # Set in .env file
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups  # For database backups
    restart: unless-stopped

  backend:
    build: ./backend
    container_name: agrisense_backend
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000
    # For Flask use: gunicorn app:app --bind 0.0.0.0:8000 --workers 4
    environment:
      DATABASE_URL: postgresql://agrisense_user:${DB_PASSWORD}@postgres:5432/agrisense_db
      SECRET_KEY: ${SECRET_KEY}
      OPENWEATHER_API_KEY: ${OPENWEATHER_API_KEY}
      ENVIRONMENT: production
    ports:
      - "8000:8000"
    depends_on:
      - postgres
    volumes:
      - ./backend:/app
      - ./uploads:/app/uploads  # Store uploaded pest images
    restart: unless-stopped

  # Optional: Nginx as reverse proxy for HTTPS
  nginx:
    image: nginx:alpine
    container_name: agrisense_nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl  # SSL certificates
    depends_on:
      - backend
    restart: unless-stopped

volumes:
  postgres_data:
```

**Quick Deployment Steps:**
```bash
# 1. SSH into your server
ssh user@your-server-ip

# 2. Install Docker & Docker Compose (one-time setup)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo apt install docker-compose

# 3. Clone your repository
git clone https://github.com/yourusername/agrisense.git
cd agrisense

# 4. Create environment file
nano .env
# Add:
# DB_PASSWORD=your_secure_password
# SECRET_KEY=your_jwt_secret_key
# OPENWEATHER_API_KEY=your_api_key

# 5. Deploy everything (one command!)
docker-compose up -d

# 6. Check if running
docker-compose ps

# Your API is now live at http://your-server-ip:8000
```

**Setting Up HTTPS (Free SSL with Let's Encrypt):**
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# If you have a domain (e.g., api.agrisense.com)
sudo certbot --nginx -d api.agrisense.com

# If no domain, use free DNS service:
# - DuckDNS.org: agrisense-api.duckdns.org
# - No-IP.com: agrisense.ddns.net

# Certbot auto-renews every 90 days
```

**Accessing Your API from Flutter:**
```dart
// lib/config/api_config.dart

// Option 1: Using IP address (quick start)
const String API_BASE_URL = 'http://123.45.67.89:8000';

// Option 2: Using domain with HTTPS (recommended for demo)
const String API_BASE_URL = 'https://api.agrisense.com';

// Option 3: Using free DNS service
const String API_BASE_URL = 'https://agrisense-api.duckdns.org';
```

**Server Management Commands:**
```bash
# View logs
docker-compose logs -f backend
docker-compose logs -f postgres

# Restart services
docker-compose restart backend

# Update code and redeploy
git pull
docker-compose down
docker-compose up -d --build

# Backup database
docker exec agrisense_db pg_dump -U agrisense_user agrisense_db > backup_$(date +%Y%m%d).sql

# Stop everything
docker-compose down

# Stop and remove all data (fresh start)
docker-compose down -v
```

**Image Storage on Your Server:**
- **Recommended**: Store uploaded pest images in `/uploads` folder (mounted volume)
- File path in database: `/uploads/pest_images/uuid_filename.jpg`
- Serve via backend endpoint: `GET /api/images/{filename}`
- Alternatively: Use Cloudinary free tier (25GB) if you want CDN benefits

**Monitoring & Maintenance:**
```bash
# Check disk space
df -h

# Check memory usage
free -m

# View running containers
docker ps

# Check container resource usage
docker stats

# Set up automatic backups (cron job)
sudo crontab -e
# Add: 0 2 * * * /path/to/backup-script.sh
```

**Why This is Better Than Azure for Your Project:**
1. ✅ No cost concerns or credit limits
2. ✅ Full control over deployment (learn real DevOps)
3. ✅ No vendor lock-in (skills transfer to any cloud)
4. ✅ Can experiment freely without worrying about bills
5. ✅ More impressive on resume (self-hosted = real infrastructure knowledge)
6. ✅ Faster debugging (direct server access, no cloud abstractions)
7. ✅ No complex IAM/networking setup (just Docker)

**Fallback Options (if your server has issues):**
- **Render.com** (Primary Backup)
  - Free tier sufficient for demo
  - Deploy from GitHub in 15 minutes
  - Automatic HTTPS included
  - Built-in PostgreSQL free tier
- **Railway.app** (Secondary Backup)
  - $5 free credit monthly
  - Simple deployment
  - Good for student projects

### 4. ML Integration Strategy - CRITICAL ⚠️

**REALITY CHECK**: You are responsible for ML integration, not just consuming APIs.

#### Scenario A: ML Team Delivers Working Models ✅
**If they provide trained models, you need to:**

1. **Deploy the Model**
   ```python
   # ml_service.py (separate microservice or same backend)
   from fastapi import FastAPI, File, UploadFile
   import torch
   from PIL import Image
   
   app = FastAPI()
   
   # Load model (provided by ML team)
   model = torch.load('pest_detection_model.pth')
   model.eval()
   
   @app.post("/predict")
   async def predict_pest(file: UploadFile = File(...)):
       image = Image.open(file.file)
       # Preprocessing (ML team provides this)
       processed = preprocess_image(image)
       
       # Inference
       with torch.no_grad():
           prediction = model(processed)
       
       # Post-processing (ML team provides logic)
       result = {
           'pest_name': get_pest_name(prediction),
           'confidence': float(prediction.max()),
           'bounding_boxes': get_bounding_boxes(prediction)
       }
       
       return result
   ```

2. **Create Mock Service for Development**
   ```python
   # mock_ml_service.py
   from fastapi import FastAPI, File, UploadFile
   import random
   
   app = FastAPI()
   
   MOCK_PESTS = ['Stem Borer', 'Rice Leaf Folder', 'Aphids', 'Leaf Miner']
   
   @app.post("/predict")
   async def mock_predict(file: UploadFile = File(...)):
       # Always return fake detection for testing
       return {
           'pest_name': random.choice(MOCK_PESTS),
           'confidence': round(random.uniform(0.75, 0.95), 2),
           'bounding_boxes': [{'x': 100, 'y': 100, 'w': 50, 'h': 50}],
           'risk_level': random.choice(['low', 'medium', 'high'])
       }
   ```

#### Scenario B: ML Team Struggles (HIGH PROBABILITY) ⚠️
**Backup Plan: Use Pre-trained Models**

1. **Roboflow Inference API** (Easiest)
   - Upload pest images to Roboflow
   - Use their hosted inference API
   - Free tier: 1000 predictions/month
   - Docs: https://roboflow.com/
   
2. **Hugging Face Transformers** (More Control)
   ```python
   from transformers import YolosForObjectDetection, YolosImageProcessor
   from PIL import Image
   
   model = YolosForObjectDetection.from_pretrained('hustvl/yolos-tiny')
   processor = YolosImageProcessor.from_pretrained("hustvl/yolos-tiny")
   
   def detect_objects(image_path):
       image = Image.open(image_path)
       inputs = processor(images=image, return_tensors="pt")
       outputs = model(**inputs)
       
       # Process outputs
       target_sizes = torch.tensor([image.size[::-1]])
       results = processor.post_process_object_detection(
           outputs, target_sizes=target_sizes, threshold=0.7
       )[0]
       
       return results
   ```

**ACTION ITEM**: Decide by Week 2
- If ML team has working prototype → use their model
- If not → implement backup plan immediately

### 5. Database Schema - FINALIZED ✅

**Complete Schema with All Best Practices**

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    role VARCHAR(20) DEFAULT 'farmer' CHECK (role IN ('farmer', 'agency', 'admin')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP,  -- Soft delete
    
    INDEX idx_users_email (email),
    INDEX idx_users_active (deleted_at) WHERE deleted_at IS NULL
);

-- Farm sectors table
CREATE TABLE farm_sectors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(255),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    area_hectares DECIMAL(10, 2),
    crop_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_sectors_user (user_id)
);

-- Sensor data table (time-series data)
CREATE TABLE sensor_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sector_id UUID NOT NULL REFERENCES farm_sectors(id) ON DELETE CASCADE,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    temperature DECIMAL(5, 2),  -- Celsius
    humidity DECIMAL(5, 2),  -- Percentage
    soil_moisture DECIMAL(5, 2),  -- Percentage
    soil_temperature DECIMAL(5, 2),  -- Celsius
    solar_radiation DECIMAL(8, 2),  -- W/m²
    wind_speed DECIMAL(5, 2),  -- km/h
    rainfall DECIMAL(6, 2),  -- mm
    
    INDEX idx_sensor_data_sector_time (sector_id, timestamp DESC),
    INDEX idx_sensor_data_timestamp (timestamp DESC)
);

-- Pest detections table
CREATE TABLE pest_detections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    sector_id UUID NOT NULL REFERENCES farm_sectors(id) ON DELETE CASCADE,
    image_url TEXT NOT NULL,
    image_hash VARCHAR(64) NOT NULL,  -- SHA-256 to prevent duplicate uploads
    pest_name VARCHAR(100),
    confidence DECIMAL(5, 4) CHECK (confidence >= 0 AND confidence <= 1),
    risk_level VARCHAR(20) CHECK (risk_level IN ('low', 'medium', 'high')),
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'resolved', 'false_positive')),
    detection_metadata JSONB,  -- Store bounding boxes, recommendations
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    
    INDEX idx_pest_user_detections (user_id, created_at DESC),
    INDEX idx_pest_sector_detections (sector_id, status, created_at DESC),
    INDEX idx_pest_image_hash (image_hash)
);

-- Weather predictions table (if using ML model)
CREATE TABLE weather_predictions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sector_id UUID NOT NULL REFERENCES farm_sectors(id) ON DELETE CASCADE,
    forecast_date DATE NOT NULL,
    temperature_min DECIMAL(5, 2),
    temperature_max DECIMAL(5, 2),
    humidity DECIMAL(5, 2),
    rainfall_probability DECIMAL(5, 2),  -- 0-100
    wind_speed DECIMAL(5, 2),
    confidence DECIMAL(5, 4),
    model_version VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE (sector_id, forecast_date),
    INDEX idx_weather_predictions_sector (sector_id, forecast_date)
);

-- Alerts table
CREATE TABLE alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    sector_id UUID REFERENCES farm_sectors(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL CHECK (type IN ('weather', 'pest', 'system')),
    severity VARCHAR(20) NOT NULL CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    acknowledged BOOLEAN DEFAULT FALSE,
    acknowledged_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    
    INDEX idx_alerts_user_unread (user_id, acknowledged, created_at DESC),
    INDEX idx_alerts_sector (sector_id, created_at DESC)
);

-- Chat history table (if implementing chatbot)
CREATE TABLE chat_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    response TEXT NOT NULL,
    model VARCHAR(50),  -- Which AI model used
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_chat_user (user_id, created_at DESC)
);

-- Audit log table (track important actions)
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50),
    entity_id UUID,
    changes JSONB,
    ip_address INET,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_audit_user (user_id, created_at DESC),
    INDEX idx_audit_entity (entity_type, entity_id)
);
```

**Schema Versioning Strategy (Alembic)**

```bash
# Install Alembic
pip install alembic

# Initialize
alembic init migrations

# Create migration
alembic revision --autogenerate -m "Initial schema"

# Apply migration
alembic upgrade head
```

**Database Triggers for Updated Timestamps**

```sql
-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply to all tables with updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_sectors_updated_at BEFORE UPDATE ON farm_sectors
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_pests_updated_at BEFORE UPDATE ON pest_detections
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

### 6. Backend Framework - FINALIZED ✅

**DECISION: FastAPI (Python)** - But Flask is Also Valid

**Why FastAPI (Your Original Choice is Good):**
- ✅ Automatic API documentation (Swagger UI at `/docs`)
- ✅ Type hints and validation (Pydantic)
- ✅ Async support (useful if ML inference is slow)
- ✅ Faster development with auto-validation
- ✅ Better for AI-assisted coding (clearer patterns)
- ✅ Modern Python features
- ✅ Your research already done

**When to Switch to Flask:**
- If you're struggling with FastAPI concepts after Week 3
- If you find async/await confusing
- If you need more Stack Overflow answers
- If you want absolute simplicity

**Both are acceptable - don't overthink this decision.**

## 🔄 Real-Time Communication Strategy

### Decision: Use Simple HTTP Polling (Regular API Calls)

**What You DON'T Need:**
- ❌ **Webhooks**: Backend pushing to mobile (mobile apps don't have URLs)
- ❌ **Server-Sent Events (SSE)**: Continuous streaming (too complex, battery drain)
- ❌ **WebSockets**: Two-way real-time (overkill for your use case)

**What You SHOULD Use:**
- ✅ **Regular REST API calls** (request-response pattern)
- ✅ **Polling**: Flutter fetches data every 30 seconds
- ✅ **Pull-to-refresh**: User manually refreshes when needed

**Why This is Better:**
```dart
// Simple, battery-efficient, easy to debug
class DashboardScreen extends StatefulWidget {
  @override
  _DashboardScreenState createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  Timer? _timer;
  SensorData? sensorData;
  
  @override
  void initState() {
    super.initState();
    _fetchSensorData();  // Initial load
    
    // Auto-refresh every 30 seconds
    _timer = Timer.periodic(Duration(seconds: 30), (timer) {
      _fetchSensorData();
    });
  }
  
  @override
  void dispose() {
    _timer?.cancel();  // Clean up timer
    super.dispose();
  }
  
  Future<void> _fetchSensorData() async {
    try {
      final response = await http.get('$API_URL/api/sensors/current');
      if (response.statusCode == 200) {
        setState(() {
          sensorData = SensorData.fromJson(jsonDecode(response.body));
        });
      }
    } catch (e) {
      print('Error fetching sensor data: $e');
    }
  }
  
  @override
  Widget build(BuildContext context) {
    return RefreshIndicator(
      onRefresh: _fetchSensorData,  // Pull-to-refresh
      child: ListView(
        children: [
          if (sensorData != null)
            SensorCard(data: sensorData!),
          // ... more widgets
        ],
      ),
    );
  }
}
```

**This approach:**
- ✅ Works 100% of the time (no connection issues)
- ✅ Battery efficient (only fetches when app is open)
- ✅ Easy to debug (just API calls)
- ✅ Works offline (graceful degradation)
- ✅ What 95% of mobile apps use
- ✅ Perfect for your demo

**When You Might Need Real-Time (Phase 2, Optional):**
- Only if you want instant alerts (without 30-second delay)
- Solution: Use **Firebase Cloud Messaging (FCM)** for push notifications
- This is separate from your API (just for alerts)

**Summary: Keep it Simple**
```
Mobile App → (every 30 seconds) → GET /api/sensors → Backend → Database
Mobile App → (pull to refresh) → GET /api/sensors → Backend → Database
Mobile App → (user action) → POST /api/pests/detect → Backend → ML Service

No webhooks. No SSE. No WebSockets. Just regular HTTP calls.
```

## 📚 Understanding Core Concepts

### What is a Web Framework? (Flask vs FastAPI)

**The Analogy:**
Building a web API without a framework is like building a restaurant from scratch (cutting wood, installing plumbing). A web framework is a pre-built restaurant space - you just add your recipes (business logic).

**What Flask/FastAPI Actually Do:**
```python
# WITHOUT a framework - you'd manually handle:
# - Parse HTTP requests
# - Route URLs to functions
# - Manage headers, cookies, sessions
# - Convert data to JSON
# - Handle errors
# ... hundreds of lines of complex code

# WITH Flask (Simple approach):
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/hello')
def hello():
    return jsonify({"message": "Hello World"})

app.run()  # Done! 5 lines vs 500 lines.

# WITH FastAPI (Modern approach):
from fastapi import FastAPI

app = FastAPI()

@app.get('/api/hello')
def hello():
    return {"message": "Hello World"}

# Bonus: Free API docs at /docs
```

**Key Differences:**

| Feature | Flask | FastAPI |
|---------|-------|---------|
| **Complexity** | Simpler, minimal | More features, steeper learning curve |
| **Validation** | Manual (you write checks) | Automatic (Pydantic models) |
| **API Docs** | None (manual) | Auto-generated Swagger UI |
| **Async Support** | No | Yes |
| **Community** | Huge (15+ years) | Growing (newer) |
| **Best For** | Beginners, simple APIs | Modern apps, ML integration |

**For Your Project:**
- ✅ **FastAPI**: Stick with it (you researched it, has auto-docs for demo)
- ✅ **Flask**: Switch if struggling after Week 3 (simpler, more help online)
- ❌ **Don't spend >1 day debating** - both work fine

### Communication Patterns: REST API vs Webhooks vs SSE

**Pattern 1: REST API (What You Should Use) ✅**
```
Mobile asks → Backend responds → Done

Example: User clicks "Refresh" → App calls API → Shows data
```
- ✅ Simple, reliable, battery-efficient
- ✅ Works offline (app doesn't crash)
- ✅ 95% of mobile apps use this

**Pattern 2: Webhooks (Don't Use for Mobile) ❌**
```
Backend pushes → Mobile receives (but mobile needs public URL!)

Problem: Your phone doesn't have a URL like "http://my-phone.com"
```
- ❌ Mobile apps can't receive webhooks directly
- ✅ Only for server-to-server (GitHub → Your Backend)

**Pattern 3: Server-Sent Events (SSE) - Too Complex ⚠️**
```
Backend streams → Mobile receives continuously

Example: Stock prices updating every second
```
- ⚠️ Battery drain (connection stays open)
- ⚠️ More complex to implement
- ❌ Overkill for sensor data that updates every 5 minutes

**Pattern 4: WebSockets - Massive Overkill ❌**
```
Both send messages anytime (two-way)

Example: Chat apps, multiplayer games
```
- ❌ You don't need mobile → backend real-time
- ❌ Too complex for your use case

**Your Implementation (Simple Polling):**
```dart
// Fetch data every 30 seconds - Perfect for your project
Timer.periodic(Duration(seconds: 30), (timer) {
  fetchSensorData();  // Just a regular API call
});

// User can manually refresh anytime
RefreshIndicator(
  onRefresh: fetchSensorData,
  child: Dashboard(),
);
```

### Your Own Server: What This Means

**You said you have a server - this changes everything!**

**What you can do:**
```
Your Server (with public IP)
    ↓
Install Docker
    ↓
Run: docker-compose up -d
    ↓
Backend + Database + Everything running!
    ↓
Access via: http://your-server-ip:8000
    ↓
(Optional) Add domain: https://api.agrisense.com
```

**Why this is BETTER than Azure:**
1. ✅ $0 cost (vs Azure credits running out)
2. ✅ Full control (vs limited by cloud policies)
3. ✅ Real DevOps skills (vs clicking buttons in portal)
4. ✅ No vendor lock-in (vs Azure-specific knowledge)
5. ✅ Can experiment freely (vs worrying about bills)

**Reality Check:**
```
Azure Setup:
- Create account (30 min)
- Configure Resource Group (confused)
- Set up App Service (documentation unclear)
- Configure database (more confusion)
- Set up networking (what's a VNET?)
- Configure SSL (certificate errors)
- Debug deployment (cryptic errors)
- Total: 2-3 days of frustration

Your Server Setup:
- SSH into server (5 min)
- Install Docker (10 min)
- Run docker-compose up (5 min)
- Total: 20 minutes, working API

Winner: Your server.
```
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app initialization
│   ├── config.py            # Settings (database URL, secrets)
│   ├── database.py          # SQLAlchemy connection
│   │
│   ├── models/              # SQLAlchemy models (database tables)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── sector.py
│   │   ├── sensor.py
│   │   ├── pest.py
│   │   └── alert.py
│   │
│   ├── schemas/             # Pydantic schemas (API request/response)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── auth.py
│   │   ├── sensor.py
│   │   └── pest.py
│   │
│   ├── api/                 # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py          # Login, register, logout
│   │   ├── sensors.py       # Get sensor data
│   │   ├── pests.py         # Pest detection endpoints
│   │   ├── weather.py       # Weather forecast
│   │   ├── alerts.py        # Alerts management
│   │   └── chat.py          # Chatbot (optional)
│   │
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── ml_client.py     # Call ML services
│   │   ├── weather_service.py
│   │   └── alert_service.py
│   │
│   └── utils/               # Helpers
│       ├── __init__.py
│       ├── security.py      # Password hashing, JWT
│       └── image.py         # Image processing
│
├── tests/
│   ├── test_auth.py
│   ├── test_pests.py
│   └── test_sensors.py
│
├── alembic/                 # Database migrations
├── requirements.txt
├── Dockerfile
└── .env
```

**Minimal Working Backend (Start Here)**

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AgriSense API", version="1.0.0")

# CORS for Flutter app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify Flutter app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "AgriSense API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Import routers
from app.api import auth, sensors, pests, weather, alerts

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(sensors.router, prefix="/api/sensors", tags=["Sensors"])
app.include_router(pests.router, prefix="/api/pests", tags=["Pest Detection"])
app.include_router(weather.router, prefix="/api/weather", tags=["Weather"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["Alerts"])
```

### 7. Mobile App Framework - FINALIZED ✅

**DECISION: Flutter**

**AI-Assisted Development Strategy**

Since you're new to Flutter and using AI assistants:

1. **Start with a Template**
   ```bash
   flutter create agrisense_mobile
   cd agrisense_mobile
   ```

2. **Use Flutter Packages (Don't Reinvent)**
   ```yaml
   # pubspec.yaml
   dependencies:
     flutter:
       sdk: flutter
     
     # UI
     flutter_svg: ^2.0.0
     google_fonts: ^6.0.0
     
     # State Management (choose one)
     provider: ^6.0.0        # Simplest
     # riverpod: ^2.0.0      # More advanced
     
     # Networking
     dio: ^5.0.0             # HTTP client
     
     # Storage
     shared_preferences: ^2.0.0  # Simple key-value
     
     # Image
     image_picker: ^1.0.0    # Camera/gallery
     cached_network_image: ^3.0.0
     
     # Authentication
     flutter_secure_storage: ^9.0.0  # Store JWT
     
     # UI Components
     flutter_spinkit: ^5.0.0  # Loading indicators
     fluttertoast: ^8.0.0     # Toast messages
   ```

3. **Folder Structure**
   ```
   lib/
   ├── main.dart
   ├── config/
   │   └── api_config.dart      # API base URL
   ├── models/                  # Data models
   │   ├── user.dart
   │   ├── sensor_reading.dart
   │   └── pest_detection.dart
   ├── services/                # API calls
   │   ├── api_service.dart
   │   ├── auth_service.dart
   │   └── pest_service.dart
   ├── providers/               # State management
   │   ├── auth_provider.dart
   │   └── sensor_provider.dart
   ├── screens/                 # UI screens
   │   ├── auth/
   │   │   ├── login_screen.dart
   │   │   └── register_screen.dart
   │   ├── dashboard/
   │   │   └── dashboard_screen.dart
   │   └── pest/
   │       └── pest_detection_screen.dart
   └── widgets/                 # Reusable widgets
       ├── sensor_card.dart
       └── alert_card.dart
   ```

4. **AI Prompting Strategy for Flutter**
   
   **Good Prompts:**
   - "Create a Flutter login screen with email and password fields, using TextFormField with validation"
   - "Build a Flutter card widget to display sensor data (temperature, humidity) with icons"
   - "Implement image picker in Flutter to capture photo from camera and upload to API"
   
   **Bad Prompts:**
   - "Build my entire app" (too vague)
   - "Make it look good" (subjective)

5. **Start with These Screens (in order)**
   ```
   Week 1: Login Screen
   Week 2: Dashboard Screen (static data)
   Week 3: Pest Detection Screen (camera + upload)
   Week 4: Results Screen
   Week 5: Connect to real backend API
   ```

---

## 👥 TEAM STRUCTURE & RESPONSIBILITIES

### Your Role (Primary Developer)
**You are the integration point for everything**

#### Your Responsibilities
1. **Backend Development (70% of your time)**
   - Build FastAPI endpoints
   - Database schema & migrations
   - ML model integration
   - Weather API integration
   - Alert generation logic

2. **Mobile App Development (20% of your time)**
   - Use AI assistants heavily
   - Focus on core screens (login, dashboard, pest detection)
   - API integration with backend

3. **DevOps & Deployment (10% of your time)**
   - Docker setup for local development
   - Deploy to Render/Railway for demo
   - Database backups

#### What You DON'T Do
- ❌ Train ML models (ML team's job)
- ❌ Design UI from scratch (use Material Design + AI)
- ❌ Write extensive documentation (focus on working code)

### ML Team Responsibilities

**What They MUST Deliver:**

1. **Pest Detection Model (Priority 1)**
   - Trained model file (.pth or .h5)
   - Preprocessing code (how to prepare images)
   - Inference code (how to run predictions)
   - Post-processing code (how to interpret results)
   - Expected accuracy metrics

2. **Weather Prediction Model (Priority 2 - Optional)**
   - Trained model file
   - Input data format specification
   - Prediction output format
   - Model confidence scores

**Delivery Format:**
```
ml_models/
├── pest_detection/
│   ├── model.pth
│   ├── preprocess.py
│   ├── inference.py
│   └── README.md (how to use)
└── weather_prediction/
    ├── model.pkl
    ├── predict.py
    └── README.md
```

**Weekly Check-ins:**
- Week 2: Show training progress (loss curves)
- Week 4: Deliver mock API endpoint
- Week 6: Deliver trained model (even if not perfect)
- Week 8: Final model with documentation

**Backup Plan (if ML team fails):**
- Week 6: If no working prototype → switch to pre-trained models
- You implement Roboflow API integration
- Still get full credit (it's about integration, not training)

---

## 📋 PRIORITIZED REQUIREMENTS LIST

### Must-Have (Core MVP) - 80% of Effort ⭐⭐⭐

| # | Requirement | Owner | Status | Priority |
|---|-------------|-------|--------|----------|
| 1 | User registration & login | You | Not Started | Critical |
| 2 | JWT authentication | You | Not Started | Critical |
| 3 | PostgreSQL database setup | You | Not Started | Critical |
| 4 | Pest image upload (mobile) | You | Not Started | Critical |
| 5 | Pest detection API endpoint | You + ML Team | Not Started | Critical |
| 6 | Display pest detection results | You | Not Started | Critical |
| 7 | Store detections in database | You | Not Started | Critical |
| 8 | Dashboard with sensor data | You | Not Started | High |
| 9 | Synthetic sensor data generator | You | Not Started | High |
| 10 | Alert generation system | You | Not Started | High |
| 11 | Weather forecast display | You | Not Started | Medium |
| 12 | Basic API documentation | You | Not Started | Medium |

### Should-Have (If Time Permits) - 15% of Effort ⭐⭐

| # | Requirement | Owner | Status | Priority |
|---|-------------|-------|--------|----------|
| 13 | Historical data visualization | You | Future | Low |
| 14 | User profile management | You | Future | Low |
| 15 | Push notifications | You | Future | Low |
| 16 | AI chatbot | You | Future | Low |
| 17 | Multi-sector management | You | Future | Low |

### Won't-Have (Cut Entirely) - 0% Effort ❌

| # | Requirement | Reason |
|---|-------------|--------|
| 1 | Physical IoT hardware | Out of scope, simulation only |
| 2 | Admin management system | Not needed for MVP |
| 3 | Dataset import functionality | Complexity not justified |
| 4 | Training ML models | ML team responsibility |
| 5 | Multiple mobile platforms | Start with Android only |
| 6 | Real-time WebSocket updates | HTTP polling sufficient |
| 7 | Complex data analytics | Focus on basic display |
| 8 | Multi-language support | English only for MVP |

---

## 🚀 DEVELOPMENT PHASES & TIMELINE

### Phase 0: Setup & Planning (Week 1-2)
**Goal**: Get development environment running

- [ ] Install tools (Python, Flutter, PostgreSQL, Docker)
- [ ] Create GitHub repository
- [ ] Set up Docker Compose for local dev
- [ ] Create database schema
- [ ] Build "Hello World" FastAPI endpoint
- [ ] Build "Hello World" Flutter app
- [ ] Test mobile app can call backend API

**Deliverable**: You can make a successful API call from Flutter to FastAPI

### Phase 1: Authentication (Week 3-4)
**Goal**: Users can register and login

**Backend Tasks:**
- [ ] Implement user registration endpoint
- [ ] Implement login endpoint (return JWT)
- [ ] Password hashing (bcrypt)
- [ ] JWT token generation & validation
- [ ] Protect endpoints with auth middleware

**Mobile Tasks:**
- [ ] Login screen UI
- [ ] Registration screen UI
- [ ] Store JWT in secure storage
- [ ] Navigate to dashboard after login

**Test**: User can register → login → see dashboard

### Phase 2: Dashboard & Sensors (Week 5-6)
**Goal**: Display simulated sensor data

**Backend Tasks:**
- [ ] Build synthetic data generator script
- [ ] Seed database with 7 days of historical data
- [ ] Create `/api/sensors/current` endpoint
- [ ] Create `/api/sensors/history` endpoint

**Mobile Tasks:**
- [ ] Dashboard screen with sensor cards
- [ ] Display temperature, humidity, soil moisture
- [ ] Refresh button to get latest data
- [ ] Simple line chart for historical trends

**Test**: Dashboard shows realistic sensor readings that update

### Phase 3: Pest Detection (Week 7-10) **MOST CRITICAL**
**Goal**: Core feature working end-to-end

**Backend Tasks:**
- [ ] Create mock ML service (returns fake predictions)
- [ ] Build `/api/pests/detect` endpoint
- [ ] Handle image upload (validate size, format)
- [ ] Store uploaded images (database or Cloudinary)
- [ ] Store detection results in database
- [ ] Create `/api/pests/history` endpoint

**Mobile Tasks:**
- [ ] Pest detection screen with camera button
- [ ] Image picker (camera & gallery)
- [ ] Image preview before upload
- [ ] Upload progress indicator
- [ ] Results screen (pest name, confidence, image)
- [ ] History of past detections

**ML Integration:**
- [ ] Week 7: Use mock predictions
- [ ] Week 9: ML team delivers model
- [ ] Week 10: Replace mock with real model

**Test**: Upload pest image → get detection result → see in history

### Phase 4: Weather & Alerts (Week 11-12)
**Goal**: Add weather forecast and alert system

**Backend Tasks:**
- [ ] Integrate OpenWeatherMap API
- [ ] Create `/api/weather/forecast` endpoint
- [ ] Build alert generation logic (thresholds)
- [ ] Create `/api/alerts` endpoint
- [ ] Mark alerts as read

**Mobile Tasks:**
- [ ] Weather screen with 7-day forecast
- [ ] Alerts screen (list of notifications)
- [ ] Alert badge on dashboard
- [ ] Pull-to-refresh

**Test**: Weather shows real forecast, alerts appear when pest detected

### Phase 5: Polish & Deploy (Week 13-14)
**Goal**: Make it demo-ready

- [ ] Fix critical bugs
- [ ] Improve UI (use AI to make it prettier)
- [ ] Deploy backend to Render.com
- [ ] Deploy database to Render
- [ ] Test on real Android device
- [ ] Create demo video
- [ ] Write deployment documentation

---

## 🔧 AI-ASSISTED DEVELOPMENT GUIDE

### How to Use AI Effectively for This Project

#### For Backend (FastAPI)

**Example Prompts:**

1. **Database Models**
```
Create a SQLAlchemy model for a pest_detections table with:
- UUID primary key
- Foreign keys to users and farm_sectors
- Fields: image_url, pest_name, confidence, risk_level, status
- Timestamps (created_at, updated_at)
- Use proper relationships and indexes
```

2. **API Endpoints**
```
Create a FastAPI endpoint POST /api/pests/detect that:
- Accepts image file upload (multipart/form-data)
- Validates image (JPEG/PNG, max 5MB)
- Saves to database
- Returns pest detection result
- Includes error handling
- Use Pydantic for request/response validation
```

3. **Authentication**
```
Create FastAPI JWT authentication with:
- Login endpoint that returns access token
- Dependency to protect routes (get_current_user)
- Use python-jose for JWT
- Hash passwords with passlib
- Return 401 if unauthorized
```

#### For Mobile (Flutter)

**Example Prompts:**

1. **UI Screens**
```
Create a Flutter login screen with:
- Email and password TextFormFields
- Validation (email format, password length)
- Submit button that calls API
- Loading indicator during API call
- Navigate to dashboard on success
- Show error message on failure
- Use Provider for state management
```

2. **API Integration**
```
Create a Flutter service class that:
- Uses Dio for HTTP requests
- Has methods for login, register, getPests, uploadImage
- Includes JWT token in headers
- Handles errors (network, 401, 500)
- Returns strongly-typed models
- Has retry logic for failed requests
```

3. **Widgets**
```
Create a Flutter card widget to display sensor data with:
- Icon on the left
- Label and value in the middle
- Unit (°C, %) on the right
- Rounded corners and shadow
- Color changes based on value (green=good, red=bad)
- Reusable for different sensor types
```

#### What AI Can Do Well
- ✅ Generate boilerplate code (models, schemas, CRUD)
- ✅ Write utility functions (image processing, validation)
- ✅ Create UI components (cards, forms, buttons)
- ✅ Fix syntax errors
- ✅ Explain code snippets
- ✅ Suggest libraries/packages

#### What AI Struggles With
- ❌ Architecture decisions (you need to decide structure)
- ❌ Complex business logic (alert thresholds, rules)
- ❌ Debugging integration issues (between mobile/backend/ML)
- ❌ Performance optimization
- ❌ Security best practices

#### Best Practices
1. **Break down large tasks** into small prompts
2. **Review generated code** - don't blindly copy/paste
3. **Test incrementally** - run code after each change
4. **Ask for explanations** - understand what code does
5. **Iterate** - refine prompts if output isn't right

---

## 🔐 SECURITY CHECKLIST

### Must-Have Security (Don't Skip)

- [ ] **Password Hashing** (use bcrypt or argon2)
  ```python
  from passlib.context import CryptContext
  pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
  hashed = pwd_context.hash(plain_password)
  ```

- [ ] **JWT Tokens** (use python-jose)
  ```python
  from jose import JWTError, jwt
  token = jwt.encode({"sub": user_id}, SECRET_KEY, algorithm="HS256")
  ```

- [ ] **Input Validation** (Pydantic does this automatically)
  ```python
  class PestDetectionRequest(BaseModel):
      sector_id: UUID
      image: UploadFile
  ```

- [ ] **SQL Injection Prevention** (SQLAlchemy ORM prevents this)
  - Never use raw SQL with string formatting
  - Always use parameterized queries

- [ ] **Image Upload Validation**
  ```python
  ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
  MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
  
  if file.size > MAX_FILE_SIZE:
      raise HTTPException(400, "File too large")
  if file.content_type not in ['image/jpeg', 'image/png']:
      raise HTTPException(400, "Invalid file type")
  ```

- [ ] **Rate Limiting** (use slowapi)
  ```python
  from slowapi import Limiter
  limiter = Limiter(key_func=get_remote_address)
  
  @app.post("/api/pests/detect")
  @limiter.limit("10/minute")
  async def detect_pest(...):
      ...
  ```

- [ ] **CORS Configuration** (only allow your Flutter app)
  ```python
  app.add_middleware(
      CORSMiddleware,
      allow_origins=["https://yourdomain.com"],  # Not "*" in production
      allow_credentials=True,
      allow_methods=["GET", "POST", "PUT", "DELETE"],
      allow_headers=["*"],
  )
  ```

- [ ] **HTTPS/TLS** (use Let's Encrypt for free SSL)
  - Required for production
  - Render.com provides this automatically

### Nice-to-Have Security
- [ ] Refresh tokens (JWT with expiry)
- [ ] Email verification (confirm registration)
- [ ] Password reset flow
- [ ] Account lockout (after 5 failed logins)
- [ ] Audit logging (track sensitive actions)

---

## 🐛 TESTING STRATEGY

### Backend Testing (pytest)

```python
# tests/test_auth.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_success():
    response = client.post("/api/auth/register", json={
        "email": "farmer@example.com",
        "password": "securepass123",
        "name": "Test Farmer"
    })
    assert response.status_code == 201
    assert "id" in response.json()

def test_register_duplicate_email():
    # First registration
    client.post("/api/auth/register", json={
        "email": "duplicate@example.com",
        "password": "pass123",
        "name": "Farmer 1"
    })
    # Second registration with same email
    response = client.post("/api/auth/register", json={
        "email": "duplicate@example.com",
        "password": "pass456",
        "name": "Farmer 2"
    })
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

def test_login_success():
    # Register user first
    client.post("/api/auth/register", json={
        "email": "login@example.com",
        "password": "testpass123",
        "name": "Login Test"
    })
    # Login
    response = client.post("/api/auth/login", json={
        "email": "login@example.com",
        "password": "testpass123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password():
    response = client.post("/api/auth/login", json={
        "email": "login@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
```

### Mobile Testing (Flutter)

```dart
// test/widget_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:agrisense_mobile/screens/login_screen.dart';

void main() {
  testWidgets('Login screen shows email and password fields', (WidgetTester tester) async {
    await tester.pumpWidget(MaterialApp(home: LoginScreen()));
    
    expect(find.text('Email'), findsOneWidget);
    expect(find.text('Password'), findsOneWidget);
    expect(find.text('Login'), findsOneWidget);
  });

  testWidgets('Login button disabled when fields empty', (WidgetTester tester) async {
    await tester.pumpWidget(MaterialApp(home: LoginScreen()));
    
    final loginButton = find.text('Login');
    await tester.tap(loginButton);
    await tester.pump();
    
    // Should show validation errors
    expect(find.text('Email is required'), findsOneWidget);
    expect(find.text('Password is required'), findsOneWidget);
  });
}
```

### Manual Testing Checklist

**Before Every Demo:**
- [ ] User can register new account
- [ ] User can login with correct credentials
- [ ] Login fails with wrong password
- [ ] Dashboard shows sensor data
- [ ] Sensor data updates when refreshed
- [ ] User can upload pest image
- [ ] Pest detection returns result
- [ ] Detection shows in history
- [ ] Weather forecast displays
- [ ] Alerts appear on dashboard
- [ ] User can logout

---

## 📚 KEY RESOURCES & DOCUMENTATION

### Official Documentation
- **FastAPI**: https://fastapi.tiangolo.com/
- **Flutter**: https://docs.flutter.dev/
- **PostgreSQL**: https://www.postgresql.org/docs/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **Pydantic**: https://docs.pydantic.dev/

### Tutorials (Start Here if New)
- **FastAPI Tutorial**: https://fastapi.tiangolo.com/tutorial/
- **Flutter Codelabs**: https://docs.flutter.dev/codelabs
- **SQLAlchemy ORM Tutorial**: https://docs.sqlalchemy.org/en/20/orm/quickstart.html
- **JWT Authentication Tutorial**: https://testdriven.io/blog/fastapi-jwt/

### AI Coding Tools
- **GitHub Copilot**: Best for inline code suggestions
- **ChatGPT/Claude**: Best for explaining concepts, debugging
- **Cursor IDE**: AI-powered code editor
- **v0.dev**: Generate Flutter/React UI components

### APIs & Services
- **OpenWeatherMap API**: https://openweathermap.org/api
- **Cloudinary** (image hosting): https://cloudinary.com/
- **Render.com** (deployment): https://render.com/
- **Roboflow** (pre-trained ML): https://roboflow.com/

---

## ⚠️ CRITICAL RISKS & MITIGATION

### Risk 1: ML Team Fails to Deliver ⚠️⚠️⚠️
**Probability**: High (70%)
**Impact**: Critical

**Mitigation**:
1. **Week 2**: Define API contract with ML team
2. **Week 4**: Request mock API endpoint (returns fake predictions)
3. **Week 6**: Check-in on model training progress
4. **Week 8 Deadline**: If no working model → pivot to Roboflow API
5. **Backup Plan**: Use pre-trained YOLOv5 from Hugging Face

**Action Items**:
- [ ] Schedule weekly ML team sync (15 min)
- [ ] Create backup plan document (how to use Roboflow)
- [ ] Test Roboflow API by Week 4 (just in case)

### Risk 2: Scope Creep 🚨🚨
**Probability**: Very High (90%)
**Impact**: High

**Warning Signs**:
- "Can we add this one more feature?"
- "It would be cool if..."
- "This other project has X, we should too"

**Mitigation**:
1. **Say NO** to new features until MVP is done
2. Keep a "Future Work" list
3. Focus on ONE workflow working perfectly
4. Review scope weekly

### Risk 3: Technical Skill Gap 📚
**Probability**: Medium (50%)
**Impact**: Medium

**Mitigation**:
1. **Learn by doing** (don't read for weeks)
2. **Use AI heavily** for code generation
3. **Copy examples** from official docs
4. **Ask for help** in Discord/Stack Overflow
5. **Pair program** with team members

### Risk 4: Poor Time Management ⏰
**Probability**: High (70%)
**Impact**: High

**Mitigation**:
1. **Weekly sprints** (7-day cycles)
2. **Daily standups** (10 min, even solo)
3. **Track time** (how many hours on each task?)
4. **Block 20 hours/week minimum** for this project
5. **Front-load difficult tasks** (don't leave ML integration to last week)

### Risk 5: Deployment Issues 🚀
**Probability**: Medium (50%)
**Impact**: Medium

**Mitigation**:
1. **Deploy early** (Week 6, even if incomplete)
2. **Test on staging** before demo day
3. **Have local backup** (Docker on laptop)
4. **Record demo video** (in case live demo fails)
5. **Practice demo** 5 times before presentation

---

## 📝 WEEKLY PROGRESS TRACKING

### Week Progress Template

```markdown
## Week X Progress (Date Range)

### Completed ✅
- [ ] Task 1
- [ ] Task 2

### In Progress 🔄
- [ ] Task 3 (50% done)

### Blocked 🚫
- [ ] Task 4 (Reason: waiting on ML team)

### Next Week Plan
1. Priority 1
2. Priority 2

### Risks/Issues
- Issue 1: Description and mitigation plan

### Time Spent
- Backend: 10 hours
- Mobile: 5 hours
- Meetings: 2 hours
- **Total: 17 hours**
```

---

## 🎯 SUCCESS CRITERIA

### Technical Success (Must Achieve)
- [ ] User can register and login
- [ ] Dashboard displays real-time sensor data
- [ ] User can upload pest image and receive detection result
- [ ] System stores data persistently in PostgreSQL
- [ ] Backend API documented (Swagger UI)
- [ ] Mobile app works on Android device
- [ ] System deployed and accessible via URL
- [ ] No critical security vulnerabilities

### Demo Success (Goal)
- [ ] 5-minute demo runs smoothly
- [ ] Show 3 core workflows (login → dashboard → pest detection)
- [ ] Explain architecture (mobile → backend → ML → database)
- [ ] Answer questions confidently
- [ ] Have backup video if live demo fails

### Learning Success (Personal)
- [ ] Understand REST API design
- [ ] Can build mobile app with Flutter
- [ ] Know how to integrate ML models
- [ ] Experience with full-stack development
- [ ] Portfolio project to show employers

---

## 🚀 QUICK START GUIDE

### Day 1: Setup Development Environment

```bash
# 1. Install tools
# - Python 3.10+
# - PostgreSQL 15
# - Flutter SDK
# - Docker Desktop
# - VS Code (or your preferred IDE)

# 2. Clone template repository (or create new)
git clone https://github.com/yourusername/agrisense.git
cd agrisense

# 3. Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 4. Database setup
docker run --name agrisense-db -e POSTGRES_PASSWORD=dev123 -p 5432:5432 -d postgres:15
# Or use docker-compose up

# 5. Run backend
uvicorn app.main:app --reload
# Visit http://localhost:8000/docs (Swagger UI)

# 6. Mobile setup
cd ../mobile
flutter pub get
flutter run  # Connect Android device or emulator
```

### Day 2-7: Build Authentication

Follow Phase 1 tasks (see timeline above)

---

## 📞 GETTING HELP

### When Stuck on Code
1. **Read error message carefully** (90% of solutions are there)
2. **Google the exact error** (likely someone solved it)
3. **Ask AI**: "Why am I getting this error? [paste error]"
4. **Stack Overflow**: Search or ask question
5. **Official docs**: Check Flutter/FastAPI docs

### When Stuck on Decisions
1. **Ask supervisor** (they've seen many projects)
2. **Keep it simple** (when in doubt, choose simpler option)
3. **Look at similar projects** on GitHub
4. **Timebox research** (max 2 hours, then decide)

### When Behind Schedule
1. **Cut features** (quality over quantity)
2. **Ask team for help** (divide and conquer)
3. **Use more AI** (speed up development)
4. **Extend deadlines** (communicate early with supervisor)

---

## 🎓 RECOMMENDED LEARNING PATH

### If Completely New to Backend
**Week 1-2: FastAPI Crash Course**
1. Watch: "FastAPI Full Course" on YouTube (3 hours)
2. Build: Simple TODO API (CRUD operations)
3. Read: FastAPI official tutorial (4 hours)
4. Practice: Create 5 endpoints (users, tasks, etc.)

### If Completely New to Flutter
**Week 1-2: Flutter Basics**
1. Watch: "Flutter Course for Beginners" on YouTube (4 hours)
2. Build: Counter app (official tutorial)
3. Build: Simple note-taking app
4. Learn: Provider state management
5. Practice: Make 3 screens (login, list, detail)

### If Completely New to Databases
**Week 1: SQL & PostgreSQL**
1. Watch: "PostgreSQL Tutorial" on YouTube (2 hours)
2. Practice: Create tables, insert data, query
3. Learn: Joins, foreign keys, indexes
4. Tool: Use pgAdmin or DBeaver GUI

---

## 🔄 HANDOVER CHECKLIST

### What to Document for Future Maintainer
- [ ] README.md with setup instructions
- [ ] API documentation (Swagger auto-generated)
- [ ] Database schema diagram
- [ ] Environment variables needed (.env.example)
- [ ] Deployment steps
- [ ] Known bugs/limitations
- [ ] Future improvement ideas

### Repository Structure
```
agrisense/
├── backend/              # FastAPI application
├── mobile/               # Flutter application
├── ml_models/            # ML model files (from ML team)
├── data_simulator/       # Synthetic data generator
├── docs/                 # Documentation
│   ├── API.md
│   ├── DATABASE.md
│   └── DEPLOYMENT.md
├── docker-compose.yml    # Local development
└── README.md             # Start here
```

---

## 📊 SUMMARY: WHAT CHANGED FROM ORIGINAL PLAN

### Tech Stack Changes ⚙️

| Component | Original Plan | Updated Recommendation | Reason |
|-----------|---------------|------------------------|--------|
| **Cloud Platform** | Microsoft Azure | Your Own Server (+ Render backup) | ✅ Free, full control, real DevOps learning, no complexity |
| **Database (Dev)** | PostgreSQL from Day 1 | SQLite → PostgreSQL | ✅ Faster setup, easier debugging, migrate later |
| **IoT Simulation** | Wokwi + Ubidots STEM | Simple Python script | ✅ No external dependencies, full control |
| **Communication** | Unclear | REST API + Polling | ✅ Simple, reliable, battery-efficient |
| **Backend** | FastAPI (uncertain) | FastAPI (Flask backup) | ✅ Confirmed with backup plan |

### Removed / Simplified
1. ❌ **Physical IoT hardware** → Synthetic data generator
2. ❌ **Wokwi simulation** → Simple Python script
3. ❌ **Ubidots STEM** → Direct database insertion
4. ❌ **Azure Cloud** → Your own server (self-hosted)
5. ❌ **Training ML models** → Use pre-trained or ML team's models
6. ❌ **Admin system** → Not needed for MVP
7. ❌ **Multi-sector management** → Single sector only
8. ❌ **Complex visualizations** → Simple charts
9. ❌ **WebSockets/SSE** → Simple HTTP polling

### Added / Clarified
1. ✅ **Complete tech stack overview** with architecture diagram
2. ✅ **Tech stack rationale** (why each choice was made)
3. ✅ **AI-assisted development** strategy
4. ✅ **Mock ML service** for development
5. ✅ **Backup plan** if ML team fails (Roboflow/Hugging Face)
6. ✅ **Realistic timeline** (14 weeks → focused milestones)
7. ✅ **Clear priorities** (pest detection is core)
8. ✅ **Database schema** (complete with best practices)
9. ✅ **Testing strategy**
10. ✅ **Security checklist**
11. ✅ **Development tools list** with requirements
12. ✅ **Package dependencies** (exact versions)
13. ✅ **Communication patterns** (REST + polling explained)
14. ✅ **Server setup guide** (Docker Compose)
15. ✅ **Deployment options** (own server + backups)

### Scope Reduction
- **Original**: 10 major features
- **Revised MVP**: 4 core features (auth, sensors, pest detection, weather)
- **Complexity**: Reduced by ~60%
- **Success Probability**: Increased from 30% → 80%

### Key Improvements in v2.0
1. **✅ Tech Stack Clarity**: Every technology choice explained with rationale
2. **✅ Server Strategy**: Own server prioritized over Azure (saves time & money)
3. **✅ Database Strategy**: SQLite for dev, PostgreSQL for production (faster start)
4. **✅ Communication Pattern**: REST + polling clearly defined (no confusion)
5. **✅ Development Path**: Clear progression from simple to complex
6. **✅ Risk Mitigation**: Multiple backup plans for every critical component
7. **✅ Tool Requirements**: Exact versions and purposes listed
8. **✅ Architecture Diagram**: Visual representation of complete system

---

## ✅ NEXT ACTIONS (This Week)

### Immediate (Next 48 Hours)
1. [ ] Read this entire document
2. [ ] Set up development environment (backend + mobile + database)
3. [ ] Create GitHub repository
4. [ ] Schedule weekly ML team check-in
5. [ ] Build "Hello World" FastAPI endpoint
6. [ ] Build "Hello World" Flutter app
7. [ ] Test mobile → backend communication

### This Week (Days 3-7)
1. [ ] Create database schema (run migrations)
2. [ ] Build user registration endpoint
3. [ ] Build login endpoint (JWT)
4. [ ] Build login screen in Flutter
5. [ ] Test end-to-end authentication flow
6. [ ] Create mock ML service (returns fake predictions)
7. [ ] Document API endpoints in Swagger

### Questions to Answer This Week
1. What is your exact project deadline?
2. How many hours/week can you commit?
3. Does ML team have labeled pest images?
4. Do you have access to Android device for testing?
5. Do you have GitHub Copilot or Claude subscription?

---

## 📌 FINAL RECOMMENDATIONS

### Do This ✅
1. **Start coding immediately** (don't wait for "perfect plan")
2. **Use AI assistants heavily** (GitHub Copilot, ChatGPT, Claude)
3. **Focus on one feature at a time** (don't parallelize until experienced)
4. **Deploy early and often** (Week 6, even if incomplete)
5. **Communicate with ML team weekly**
6. **Cut features aggressively** (quality over quantity)
7. **Test manually after every change**
8. **Commit to GitHub daily**

### Don't Do This ❌
1. **Don't spend weeks planning** (theory ≠ practice)
2. **Don't try to learn everything first** (learn by doing)
3. **Don't build features speculatively** (stick to requirements)
4. **Don't ignore ML team status** (check in proactively)
5. **Don't postpone deployment** (deploy early, deploy often)
6. **Don't skip testing** (broken demo = failed project)
7. **Don't work in isolation** (ask for help early)
8. **Don't commit large changes** (small commits = easy to debug)

---

## 📚 APPENDIX

### A. Complete API Endpoint List

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register` | Register new user | No |
| POST | `/api/auth/login` | Login (get JWT) | No |
| GET | `/api/auth/me` | Get current user | Yes |
| GET | `/api/sensors/current` | Get latest sensor data | Yes |
| GET | `/api/sensors/history` | Get historical data | Yes |
| POST | `/api/pests/detect` | Upload pest image | Yes |
| GET | `/api/pests/history` | Get past detections | Yes |
| PUT | `/api/pests/{id}/status` | Update detection status | Yes |
| GET | `/api/weather/forecast` | Get 7-day forecast | Yes |
| GET | `/api/alerts` | Get user alerts | Yes |
| PUT | `/api/alerts/{id}/acknowledge` | Mark alert as read | Yes |
| GET | `/api/health` | Health check | No |

### B. Mobile App Screen List

1. **Splash Screen** → Auto-navigate after 2s
2. **Login Screen** → Navigate to Dashboard on success
3. **Register Screen** → Navigate to Login on success
4. **Dashboard Screen** → Show sensors, weather, alerts
5. **Pest Detection Screen** → Camera/gallery picker
6. **Detection Result Screen** → Show pest name, confidence
7. **Detection History Screen** → List past detections
8. **Weather Screen** → 7-day forecast
9. **Alerts Screen** → List notifications
10. **Profile Screen** → User info, logout button

### C. Environment Variables

```bash
# .env file for backend
DATABASE_URL=postgresql://user:pass@localhost:5432/agrisense_db
SECRET_KEY=your-secret-key-for-jwt-generation
OPENWEATHER_API_KEY=your-api-key
CLOUDINARY_URL=cloudinary://key:secret@cloud_name
ENVIRONMENT=development
```

### D. Useful Shell Commands

```bash
# Backend
python -m venv venv                # Create virtual environment
pip install -r requirements.txt    # Install dependencies
uvicorn app.main:app --reload      # Run development server
alembic revision --autogenerate    # Create migration
alembic upgrade head               # Apply migrations
pytest                             # Run tests

# Mobile
flutter pub get                    # Install dependencies
flutter run                        # Run on connected device
flutter build apk                  # Build Android APK
flutter test                       # Run tests

# Database
psql -U postgres                   # Connect to PostgreSQL
docker exec -it agrisense-db psql  # Connect via Docker
```

---

---

**Document Version**: 2.1 (Tech Stack Update)  
**Last Updated**: 2025-01-03  
**Status**: Ready for Development  
**Next Milestone**: Complete Phase 0 (Development Setup) by End of Week 2

**Major Changes in v2.1:**
- ✅ Added complete tech stack overview with architecture diagram
- ✅ Explained rationale for every technology choice
- ✅ Prioritized own server over Azure Cloud (cost & complexity)
- ✅ Recommended SQLite for development (faster start)
- ✅ Clarified communication pattern (REST + polling)
- ✅ Added exact package versions and dependencies
- ✅ Included development tools requirements
- ✅ Added tech stack comparison tables

**Remember**: This is a student project. The goal is to **learn and demonstrate** your skills, not build the next billion-dollar startup. Focus on making ONE thing work really well rather than many things work poorly.

**Your Tech Stack is 95% Excellent** - The only change needed was dropping Azure for your own server. Everything else (Flutter, FastAPI, PostgreSQL, JWT, OpenWeatherMap) is solid and well-researched.

Good luck! 🚀