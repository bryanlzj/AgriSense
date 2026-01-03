# AgriSense - Product Requirements Document (PRD)

**Version:** 1.0  
**Last Updated:** January 2025  
**Project Type:** Final Year Capstone Project (Bachelor of Software Engineering)  
**Project Duration:** 14 Weeks  
**Document Owner:** Integration Lead

> **📚 IMPORTANT: Personal Learning Project**  
> This is a personal project for learning full-stack mobile development (Flutter + FastAPI) with AI assistance. It is NOT for the Access platform or enterprise deployment. Focus is on educational value, practical implementation, and demonstrating technical capabilities.

---

## 📋 Table of Contents

1. [Executive Summary](#executive-summary)
2. [Project Overview](#project-overview)
3. [Goals & Success Metrics](#goals--success-metrics)
4. [User Personas & Stories](#user-personas--stories)
5. [Feature Requirements](#feature-requirements)
6. [Technical Architecture](#technical-architecture)
7. [Database Schema](#database-schema)
8. [API Specifications](#api-specifications)
9. [Mobile App Screens](#mobile-app-screens)
10. [Non-Functional Requirements](#non-functional-requirements)
11. [Constraints & Assumptions](#constraints--assumptions)
12. [Timeline & Milestones](#timeline--milestones)
13. [Risk Management](#risk-management)
14. [Acceptance Criteria](#acceptance-criteria)

---

## 1. Executive Summary

**AgriSense** is an IoT-driven **Early Warning System for Weather and Pest Risk Management** designed for Malaysian farmers. This is a **simulation-based capstone project** with NO physical hardware - all sensor data is synthetically generated.

### Key Highlights:
- **DUAL CORE FEATURES (Equal Priority):**
  - 🌤️ **Weather Early Warning System:** Real-time weather monitoring, 7-day forecasts, anomaly detection, and weather-based alerts
  - 🐛 **Pest Risk Management System:** AI-powered pest detection, environmental monitoring, and pest outbreak predictions
- **Target Users:** Small-to-medium scale farmers in Malaysia
- **Platform:** Cross-platform mobile app (Flutter) + REST API backend (FastAPI/Python)
- **Deployment:** Self-hosted server (Docker) + Render.com backup
- **Timeline:** 14 weeks from setup to deployment

---

## 2. Project Overview

### 2.1 Problem Statement
Malaysian farmers face **two critical challenges** that threaten crop yields and farm profitability:

**1. Unpredictable Weather Patterns:**
- Sudden heavy rains, storms, and extreme temperatures damage crops
- Lack of timely weather warnings leads to preventable losses
- Farmers cannot plan irrigation, harvesting, or protective measures effectively

**2. Pest and Disease Outbreaks:**
- Pest infestations spread rapidly without early detection
- Farmers lack tools to identify pests accurately
- Delayed response leads to widespread crop damage

**Result:** Farmers experience significant crop losses, reduced yields, and financial instability due to lack of actionable, real-time information.

### 2.2 Solution
AgriSense provides a **dual-purpose early warning system** that addresses both challenges:

**🌤️ Weather Early Warning System:**
- Real-time weather monitoring and 7-day forecasts
- Automated alerts for heavy rain, storms, and extreme temperatures
- Weather-based recommendations for farming activities
- Historical weather data for trend analysis

**🐛 Pest Risk Management System:**
- AI-powered pest identification from smartphone photos
- Environmental monitoring (temperature, humidity, soil moisture)
- Automated pest risk alerts based on environmental conditions
- Historical pest detection records for outbreak tracking

**📱 Mobile-First Platform:**
- User-friendly Flutter app for Android/iOS
- Real-time data updates every 30 seconds
- Unified alert system for weather and pest warnings
- Offline mode with cached data

### 2.3 Scope (MVP)
**In Scope:**
- ✅ User authentication (register, login, JWT - simplified)
- ✅ **Weather Early Warning System:**
  - 7-day weather forecast (OpenWeatherMap API)
  - Weather anomaly alerts (heavy rain, extreme heat)
  - Weather-based recommendations
- ✅ **Pest Risk Management System:**
  - AI-powered pest detection (upload image → analysis → results)
  - Environmental monitoring dashboard (temp, humidity, soil moisture)
  - Pest risk alerts based on environmental conditions
- ✅ **Unified Alert System:**
  - Weather warnings (heavy rain, storms, extreme heat)
  - Pest risk notifications (high confidence detections)
  - Alert history and read/unread status
- ✅ **Historical Data:**
  - Past pest detections with timestamps
  - 7-day sensor data trends
  - Weather history

**Out of Scope (Future Enhancements):**
- ❌ Real physical IoT sensors
- ❌ Real-time WebSocket connections
- ❌ Multi-language support (English only for MVP)
- ❌ Social features (community forum, sharing)
- ❌ E-commerce integration (pesticide marketplace)
- ❌ Advanced analytics (ML-based predictions)

---

## 3. Goals & Success Metrics

### 3.1 Project Goals
1. **Functional Goal:** Deliver working end-to-end workflows for BOTH weather early warning AND pest risk management
2. **Academic Goal:** Meet capstone project requirements (documentation, demo, defense)
3. **Technical Goal:** Demonstrate full-stack integration (mobile + backend + ML + external APIs)
4. **Learning Goal:** Gain hands-on experience with modern development tools and IoT simulation
5. **Impact Goal:** Create a practical tool that addresses real farmer pain points (weather + pest risks)

### 3.2 Success Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| **Core Feature Completion** | 100% of BOTH weather AND pest features working | Manual testing checklist |
| **Weather Forecast Accuracy** | 7-day forecast displayed correctly | OpenWeatherMap API validation |
| **Weather Alert Timeliness** | Alerts generated within 1 minute of trigger | Backend logs |
| **Pest Detection Accuracy** | > 70% confidence for known pests | ML model evaluation |
| **API Response Time** | < 2 seconds (excluding ML inference) | Backend logs |
| **ML Inference Time** | < 5 seconds per image | Backend logs |
| **Sensor Data Refresh Rate** | Every 30 seconds | Mobile app logs |
| **App Crash Rate** | < 5% during demo | Flutter error tracking |
| **Code Coverage** | > 60% for critical paths | pytest coverage report |
| **Documentation Completeness** | All APIs documented in Swagger | Swagger UI review |
| **Deployment Success** | Backend accessible via HTTPS | curl test from mobile |
| **Demo Readiness** | 5-minute demo showcasing BOTH features | Rehearsal testing |

---

## 4. User Personas & Stories

### 4.1 Primary Persona: Ahmad (Small-Scale Farmer)

**Demographics:**
- Age: 35-50
- Location: Rural Malaysia (Kedah/Perak)
- Farm Size: 2-5 acres
- Crops: Rice, vegetables
- Tech Literacy: Basic smartphone user

**Pain Points:**
- **Weather-related:** Sudden storms and heavy rains damage crops without warning; cannot plan irrigation or harvesting schedules
- **Pest-related:** Cannot identify pest species accurately; discovers infestations too late
- **Data-related:** No historical data for decision-making; lacks tools to track patterns
- **Alert-related:** No timely warnings for weather or pest threats

**Goals:**
- **Primary Goal 1:** Receive early warnings for weather threats (rain, storms, extreme heat) to protect crops
- **Primary Goal 2:** Detect pests early to minimize crop loss
- Monitor environmental conditions remotely (temperature, humidity, soil moisture)
- Receive actionable alerts for immediate response
- Access historical data for planning future seasons

### 4.2 User Stories

#### Epic 1: User Authentication
- **US-1.1:** As a farmer, I want to register an account so that I can access the app securely
- **US-1.2:** As a farmer, I want to log in with my credentials so that I can view my personalized data
- **US-1.3:** As a farmer, I want my session to persist so that I don't have to log in repeatedly

#### Epic 2: Weather Early Warning System (CORE FEATURE)
- **US-2.1:** As a farmer, I want to see a 7-day weather forecast so that I can plan farming activities (irrigation, harvesting, planting)
- **US-2.2:** As a farmer, I want to receive alerts for heavy rain warnings so that I can protect my crops from flooding
- **US-2.3:** As a farmer, I want to receive alerts for extreme heat so that I can increase irrigation
- **US-2.4:** As a farmer, I want to see current weather conditions (temperature, humidity) so that I can make immediate decisions
- **US-2.5:** As a farmer, I want to view historical weather data so that I can identify seasonal patterns

#### Epic 3: Pest Risk Management System (CORE FEATURE)
- **US-3.1:** As a farmer, I want to take a photo of a pest so that the app can identify it
- **US-3.2:** As a farmer, I want to upload an existing photo from my gallery so that I can analyze past images
- **US-3.3:** As a farmer, I want to see the pest species name and confidence score so that I can verify the detection
- **US-3.4:** As a farmer, I want to view my detection history so that I can track pest patterns over time
- **US-3.5:** As a farmer, I want to see environmental conditions (temp, humidity, soil moisture) so that I can understand pest risk factors

#### Epic 4: Environmental Monitoring Dashboard
- **US-4.1:** As a farmer, I want to see current temperature, humidity, and soil moisture so that I can assess crop conditions
- **US-4.2:** As a farmer, I want to view historical sensor data (last 7 days) so that I can identify trends
- **US-4.3:** As a farmer, I want the dashboard to auto-refresh every 30 seconds so that I have up-to-date information

#### Epic 5: Unified Alert System
- **US-5.1:** As a farmer, I want to receive weather alerts (heavy rain, storms, extreme heat) so that I can take protective action
- **US-5.2:** As a farmer, I want to receive pest risk alerts when high-confidence detections occur so that I can respond quickly
- **US-5.3:** As a farmer, I want to see all alerts in one place so that I don't miss critical warnings
- **US-5.4:** As a farmer, I want to mark alerts as read so that I can track which ones I've addressed
- **US-5.5:** As a farmer, I want alerts to be prioritized (High/Medium/Low) so that I know which to address first

---

## 5. Feature Requirements

### 5.1 Feature: User Authentication (Simplified)

**Description:** Basic user registration and login system with simplified JWT-based authentication.

**Functional Requirements:**
- FR-1.1: System shall allow users to register with username and password
- FR-1.2: System shall validate password strength (min 6 chars - simplified for demo)
- FR-1.3: System shall hash passwords using bcrypt before storing
- FR-1.4: System shall generate JWT tokens upon successful login (30-day expiry)
- FR-1.5: System shall validate JWT tokens for protected endpoints
- FR-1.6: System shall return user profile data after authentication

**Simplifications (Student Project):**
- ❌ No email requirement (username only)
- ❌ No password reset flow
- ❌ No email verification
- ❌ No refresh tokens (long-lived access tokens instead)
- ❌ No token blacklisting
- ✅ Simple username/password authentication
- ✅ JWT for mobile app compatibility
- ✅ Password hashing for security best practice

**Acceptance Criteria:**
- ✅ User can register with valid username/password
- ✅ Duplicate username registration returns error
- ✅ User can log in with correct credentials
- ✅ Invalid credentials return 401 error
- ✅ JWT token expires after 30 days (long-lived for demo convenience)
- ✅ Protected endpoints reject requests without valid token

---

### 5.2 Feature: Weather Early Warning System (CORE FEATURE #1)

**Description:** Real-time weather monitoring, 7-day forecasts, and automated weather anomaly alerts to help farmers protect crops from weather threats.

**Functional Requirements:**
- FR-2.1: System shall integrate with OpenWeatherMap API for weather data
- FR-2.2: System shall fetch 7-day weather forecast for user's location (default: Kuala Lumpur, Malaysia)
- FR-2.3: System shall display current weather conditions (temperature, humidity, weather description, wind speed)
- FR-2.4: System shall cache weather data for 30 minutes to reduce API calls
- FR-2.5: System shall generate weather alerts for:
  - Heavy rain (> 50mm precipitation forecast)
  - Extreme heat (temperature > 35°C)
  - Storms (wind speed > 40 km/h)
- FR-2.6: System shall provide endpoint for weather forecast data
- FR-2.7: System shall provide endpoint for weather-based recommendations
- FR-2.8: System shall handle API rate limits gracefully (1000 calls/day free tier)

**Weather Data Points:**
- Current temperature (°C)
- Current humidity (%)
- Weather condition (clear, rain, cloudy, storm)
- 7-day forecast (daily high/low, precipitation probability, weather icon)
- Wind speed (km/h)
- Sunrise/sunset times

**Weather Alert Triggers:**
| Alert Type | Trigger Condition | Priority | Recommendation |
|-----------|------------------|----------|----------------|
| Heavy Rain Warning | Precipitation > 50mm in forecast | High | Cover crops, prepare drainage |
| Extreme Heat Alert | Temperature > 35°C | Medium | Increase irrigation, provide shade |
| Storm Warning | Wind speed > 40 km/h | High | Secure equipment, harvest if ready |
| Low Temperature | Temperature < 15°C | Low | Protect sensitive crops |

**Acceptance Criteria:**
- ✅ 7-day weather forecast displays correctly with icons
- ✅ Current weather updates every 30 minutes
- ✅ Weather alerts generated within 1 minute of forecast update
- ✅ Recommendations are actionable and relevant to Malaysian farming
- ✅ System handles OpenWeatherMap API failures gracefully
- ✅ Last cached weather data shown during API outage
- ✅ Weather data specific to Kuala Lumpur region

---

### 5.3 Feature: Pest Risk Management System (CORE FEATURE #2)

**Description:** AI-powered pest identification from uploaded images with confidence scoring and environmental risk assessment.

**Functional Requirements:**
- FR-3.1: System shall accept image uploads (JPEG/PNG, max 5MB)
- FR-3.2: System shall send images to ML service for inference
- FR-3.3: System shall return pest species name, confidence score, and timestamp
- FR-3.4: System shall store detection results in database
- FR-3.5: System shall provide detection history endpoint (paginated)
- FR-3.6: System shall handle ML service failures gracefully (fallback to mock)
- FR-3.7: System shall correlate pest detections with environmental conditions (temp, humidity)
- FR-3.8: System shall generate pest risk alerts when confidence > 80%

**ML Service Integration:**
- **Phase 1 (Weeks 1-8):** Mock ML service returns hardcoded predictions
- **Phase 2 (Weeks 9-12):** Integrate ML team's trained model
- **Phase 3 (Backup):** Use Roboflow API if ML team doesn't deliver

**Acceptance Criteria:**
- ✅ User can upload image from camera or gallery
- ✅ Detection completes within 5 seconds
- ✅ Results display pest name and confidence %
- ✅ Detection is saved to history
- ✅ User can view past detections with timestamps
- ✅ System handles unsupported image formats gracefully

---

### 5.4 Feature: Environmental Monitoring Dashboard

**Description:** Real-time display of simulated IoT sensor data (temperature, humidity, soil moisture) to support both weather and pest risk assessment.

**Functional Requirements:**
- FR-4.1: System shall generate synthetic sensor data every 30 seconds
- FR-4.2: System shall provide endpoint for current sensor readings
- FR-4.3: System shall provide endpoint for historical sensor data (last 7 days)
- FR-4.4: System shall correlate sensor data with weather forecasts
- FR-4.5: System shall provide data visualization endpoints (charts, trends)
- FR-4.6: Mobile app shall poll sensor data every 30 seconds

**Sensor Data Points:**
- Temperature (°C): Range 20-35°C
- Humidity (%): Range 40-90%
- Soil Moisture (%): Range 30-80%

**Acceptance Criteria:**
- ✅ Dashboard displays current sensor readings
- ✅ Data refreshes every 30 seconds
- ✅ Weather widget shows 7-day forecast
- ✅ Historical data shows line chart (last 7 days)
- ✅ Pull-to-refresh updates all data
- ✅ Offline mode shows last cached data

---

### 5.5 Feature: Unified Alert System

**Description:** Automated notifications for BOTH weather warnings AND pest risks, providing farmers with actionable alerts in one place.

**Functional Requirements:**
- FR-5.1: System shall generate weather alerts for severe conditions (rain > 50mm, temp > 35°C, wind > 40 km/h)
- FR-5.2: System shall generate pest risk alerts when confidence > 80%
- FR-5.3: System shall generate environmental alerts (low soil moisture < 40%)
- FR-5.4: System shall provide endpoint to fetch unread alerts
- FR-5.5: System shall provide endpoint to mark alerts as read
- FR-5.6: System shall prioritize alerts (High/Medium/Low)
- FR-5.7: Mobile app shall display alert badge on dashboard
- FR-5.8: Mobile app shall show alert list with timestamps and priorities

**Alert Types:**
| Type | Trigger Condition | Priority | Source |
|------|------------------|----------|--------|
| Heavy Rain Warning | Forecast shows > 50mm rain | High | Weather API |
| Storm Warning | Wind speed > 40 km/h | High | Weather API |
| Extreme Heat Alert | Temperature > 35°C | Medium | Weather API |
| Pest Risk Alert | Pest detected with confidence > 80% | High | ML Detection |
| Low Soil Moisture | Soil moisture < 40% | Low | Sensor Data |
| Low Temperature | Temperature < 15°C | Low | Weather API |

**Acceptance Criteria:**
- ✅ Alerts appear within 1 minute of trigger
- ✅ Alert badge shows unread count
- ✅ User can tap alert to view details
- ✅ User can mark alert as read
- ✅ Read alerts are visually distinct
- ✅ Alerts are sorted by timestamp (newest first)

---

## 6. Technical Architecture

### 6.1 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Flutter Mobile App                       │
│  (Android/iOS - Cross-platform)                             │
│  - UI Screens (Login, Dashboard, Pest Detection)           │
│  - State Management (Provider/Riverpod)                     │
│  - HTTP Client (Dio)                                        │
│  - Local Storage (SharedPreferences for JWT)               │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ HTTPS REST API (Polling every 30s)
                     │
┌────────────────────▼────────────────────────────────────────┐
│                   FastAPI Backend (Python 3.10+)            │
│  - Authentication (JWT)                                     │
│  - Pest Detection API                                       │
│  - Sensor Data API                                          │
│  - Weather API (OpenWeatherMap proxy)                       │
│  - Alert Generation Logic                                   │
└────────┬───────────────────────────┬────────────────────────┘
         │                           │
         │                           │
┌────────▼────────┐         ┌────────▼────────────────────────┐
│  PostgreSQL DB  │         │  ML Service (Mock → Real Model) │
│  (or SQLite)    │         │  - Image preprocessing          │
│  - Users        │         │  - Model inference              │
│  - Detections   │         │  - Confidence scoring           │
│  - Sensor Data  │         └─────────────────────────────────┘
│  - Alerts       │
└─────────────────┘

External Services:
- OpenWeatherMap API (Weather data)
- Roboflow API (Backup ML service)
```

### 6.2 Technology Stack

| Layer | Technology | Justification |
|-------|-----------|---------------|
| **Mobile** | Flutter (Dart) | Cross-platform (Android/iOS), fast development, rich UI |
| **Backend** | FastAPI (Python 3.10+) | Fast, async, auto-generated Swagger docs, easy ML integration |
| **Database** | PostgreSQL (prod) / SQLite (dev) | Relational data, ACID compliance, easy migration |
| **Authentication** | JWT (JSON Web Tokens) | Stateless, scalable, mobile-friendly |
| **ML Framework** | TensorFlow/PyTorch (team's choice) | Industry standard, good documentation |
| **Weather API** | OpenWeatherMap (Free tier) | Reliable, 1000 calls/day free |
| **Deployment** | Docker + Your Own Server | Cost-effective, full control, learning opportunity |
| **Backup Hosting** | Render.com (Free tier) | Easy deployment, HTTPS included |

### 6.3 Communication Protocol

**REST API with Polling (NOT WebSockets)**

**Why Polling?**
- ✅ Simpler to implement (no connection management)
- ✅ Works reliably on mobile networks
- ✅ Easier to debug and test
- ✅ Sufficient for 30-second update intervals

**Polling Strategy:**
- Dashboard: Poll every 30 seconds for sensor data
- Alerts: Poll every 60 seconds for new alerts
- Weather: Cache for 30 minutes (no frequent polling)

---

## 7. Database Schema

### 7.1 Entity Relationship Diagram

```
┌─────────────────┐
│     users       │
├─────────────────┤
│ id (PK)         │
│ email (UNIQUE)  │
│ password_hash   │
│ full_name       │
│ created_at      │
└────────┬────────┘
         │
         │ 1:N
         │
┌────────▼────────────┐
│    detections       │
├─────────────────────┤
│ id (PK)             │
│ user_id (FK)        │
│ image_url           │
│ pest_name           │
│ confidence          │
│ detected_at         │
└─────────────────────┘

┌─────────────────────┐
│   sensor_readings   │
├─────────────────────┤
│ id (PK)             │
│ temperature         │
│ humidity            │
│ soil_moisture       │
│ recorded_at         │
└─────────────────────┘

┌─────────────────────┐
│      alerts         │
├─────────────────────┤
│ id (PK)             │
│ user_id (FK)        │
│ alert_type          │
│ message             │
│ severity            │
│ is_read             │
│ created_at          │
└─────────────────────┘
```

### 7.2 Table Definitions

#### Table: `users`
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Indexes:**
- `idx_users_username` on `username` (for login queries)

---

#### Table: `detections`
```sql
CREATE TABLE detections (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    image_url VARCHAR(500) NOT NULL,
    pest_name VARCHAR(255) NOT NULL,
    confidence DECIMAL(5,2) NOT NULL CHECK (confidence >= 0 AND confidence <= 100),
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Indexes:**
- `idx_detections_user_id` on `user_id` (for history queries)
- `idx_detections_detected_at` on `detected_at` (for sorting)

---

#### Table: `sensor_readings`
```sql
CREATE TABLE sensor_readings (
    id SERIAL PRIMARY KEY,
    temperature DECIMAL(5,2) NOT NULL CHECK (temperature >= -50 AND temperature <= 60),
    humidity DECIMAL(5,2) NOT NULL CHECK (humidity >= 0 AND humidity <= 100),
    soil_moisture DECIMAL(5,2) NOT NULL CHECK (soil_moisture >= 0 AND soil_moisture <= 100),
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Indexes:**
- `idx_sensor_readings_recorded_at` on `recorded_at` (for time-series queries)

**Data Retention:**
- Keep last 30 days of data
- Automated cleanup job runs daily

---

#### Table: `alerts`
```sql
CREATE TABLE alerts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    alert_type VARCHAR(50) NOT NULL CHECK (alert_type IN ('pest_risk', 'heavy_rain', 'extreme_heat', 'low_soil_moisture')),
    message TEXT NOT NULL,
    severity VARCHAR(20) NOT NULL CHECK (severity IN ('low', 'medium', 'high')),
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Indexes:**
- `idx_alerts_user_id` on `user_id` (for user-specific alerts)
- `idx_alerts_is_read` on `is_read` (for unread count)
- `idx_alerts_created_at` on `created_at` (for sorting)

---

## 8. API Specifications

### 8.1 Base URL
- **Development:** `http://localhost:5000/api/v1`
- **Production:** `https://your-server.com/api/v1`

### 8.2 Authentication Endpoints

#### POST `/auth/register`
**Description:** Register a new user account (simplified)

**Request Body:**
```json
{
  "username": "ahmad_farmer",
  "password": "Pass123"
}
```

**Response (201 Created):**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "ahmad_farmer",
    "created_at": "2025-01-15T10:30:00Z"
  },
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Responses:**
- `400 Bad Request`: Invalid username format or weak password (min 6 chars)
- `409 Conflict`: Username already registered

---

#### POST `/auth/login`
**Description:** Authenticate user and receive JWT token (30-day expiry)

**Request Body:**
```json
{
  "username": "ahmad_farmer",
  "password": "Pass123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 2592000,
  "user": {
    "id": 1,
    "username": "ahmad_farmer",
    "created_at": "2025-01-15T10:30:00Z"
  }
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid credentials

---

#### GET `/auth/me`
**Description:** Get current user profile (requires authentication)

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "username": "ahmad_farmer",
  "created_at": "2025-01-15T10:30:00Z"
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid or expired token

---

### 8.3 Pest Detection Endpoints

#### POST `/detections/upload`
**Description:** Upload image for pest detection

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: multipart/form-data
```

**Request Body (Form Data):**
```
image: <binary_file> (JPEG/PNG, max 5MB)
```

**Response (200 OK):**
```json
{
  "detection_id": 42,
  "pest_name": "Fall Armyworm",
  "confidence": 87.5,
  "image_url": "/uploads/detections/42_image.jpg",
  "detected_at": "2025-01-15T14:22:00Z",
  "recommendations": [
    "Apply neem oil spray",
    "Remove affected leaves",
    "Monitor daily for 7 days"
  ]
}
```

**Error Responses:**
- `400 Bad Request`: Invalid file format or size
- `401 Unauthorized`: Missing or invalid token
- `500 Internal Server Error`: ML service unavailable

---

#### GET `/detections/history`
**Description:** Get user's detection history (paginated)

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Query Parameters:**
- `page` (optional, default: 1)
- `limit` (optional, default: 20, max: 100)

**Response (200 OK):**
```json
{
  "total": 45,
  "page": 1,
  "limit": 20,
  "detections": [
    {
      "id": 42,
      "pest_name": "Fall Armyworm",
      "confidence": 87.5,
      "image_url": "/uploads/detections/42_image.jpg",
      "detected_at": "2025-01-15T14:22:00Z"
    },
    {
      "id": 41,
      "pest_name": "Aphids",
      "confidence": 92.3,
      "image_url": "/uploads/detections/41_image.jpg",
      "detected_at": "2025-01-14T09:15:00Z"
    }
  ]
}
```

---

### 8.4 Sensor Data Endpoints

#### GET `/sensors/current`
**Description:** Get current sensor readings (latest data point)

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response (200 OK):**
```json
{
  "temperature": 28.5,
  "humidity": 72.3,
  "soil_moisture": 65.8,
  "recorded_at": "2025-01-15T14:30:00Z"
}
```

---

#### GET `/sensors/history`
**Description:** Get historical sensor data (last 7 days)

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Query Parameters:**
- `days` (optional, default: 7, max: 30)

**Response (200 OK):**
```json
{
  "readings": [
    {
      "temperature": 28.5,
      "humidity": 72.3,
      "soil_moisture": 65.8,
      "recorded_at": "2025-01-15T14:30:00Z"
    },
    {
      "temperature": 27.8,
      "humidity": 70.1,
      "soil_moisture": 64.2,
      "recorded_at": "2025-01-15T14:00:00Z"
    }
  ]
}
```

---

### 8.5 Weather Endpoints

#### GET `/weather/forecast`
**Description:** Get 7-day weather forecast

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Query Parameters:**
- `location` (optional, default: "Kuala Lumpur")

**Response (200 OK):**
```json
{
  "location": "Kuala Lumpur",
  "forecast": [
    {
      "date": "2025-01-16",
      "temp_high": 32,
      "temp_low": 24,
      "condition": "Partly Cloudy",
      "icon": "partly_cloudy",
      "precipitation_probability": 20,
      "humidity": 75
    },
    {
      "date": "2025-01-17",
      "temp_high": 31,
      "temp_low": 23,
      "condition": "Thunderstorms",
      "icon": "thunderstorm",
      "precipitation_probability": 80,
      "humidity": 85
    }
  ]
}
```

---

### 8.6 Alert Endpoints

#### GET `/alerts`
**Description:** Get user's alerts (unread first)

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Query Parameters:**
- `unread_only` (optional, default: false)

**Response (200 OK):**
```json
{
  "unread_count": 3,
  "alerts": [
    {
      "id": 15,
      "alert_type": "pest_risk",
      "message": "High confidence pest detection: Fall Armyworm (87.5%)",
      "severity": "high",
      "is_read": false,
      "created_at": "2025-01-15T14:22:00Z"
    },
    {
      "id": 14,
      "alert_type": "heavy_rain",
      "message": "Heavy rain expected tomorrow (65mm)",
      "severity": "medium",
      "is_read": false,
      "created_at": "2025-01-15T08:00:00Z"
    }
  ]
}
```

---

#### PUT `/alerts/{alert_id}/read`
**Description:** Mark alert as read

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response (200 OK):**
```json
{
  "message": "Alert marked as read",
  "alert_id": 15
}
```

---

## 9. Mobile App Screens

### 9.1 Screen Flow Diagram

```
┌─────────────┐
│   Splash    │
│   Screen    │
└──────┬──────┘
       │
       ▼
┌─────────────┐     Register     ┌──────────────┐
│    Login    │ ────────────────▶│   Register   │
│   Screen    │                  │    Screen    │
└──────┬──────┘                  └──────────────┘
       │
       │ (After Auth)
       │
       ▼
┌─────────────────────────────────────────────┐
│            Dashboard (Home)                  │
│  - Sensor Data Cards                        │
│  - Weather Widget                           │
│  - Alert Badge                              │
│  - Quick Action Buttons                     │
└──┬────────┬────────┬────────┬───────────────┘
   │        │        │        │
   │        │        │        │
   ▼        ▼        ▼        ▼
┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐
│ Pest │ │Sensor│ │Weather│ │Alerts│
│Detect│ │History│ │Detail│ │ List │
└──┬───┘ └──────┘ └──────┘ └──────┘
   │
   ▼
┌──────────┐
│Detection │
│ Results  │
└──────────┘
```

---

### 9.2 Screen Specifications

#### Screen 1: Login Screen
**Purpose:** User authentication entry point

**UI Elements:**
- App logo and name (AgriSense)
- Email input field (with validation)
- Password input field (obscured text)
- "Login" button (primary action)
- "Don't have an account? Register" link
- Error message display area

**Interactions:**
- Tap "Login" → Validate inputs → Call `/auth/login` → Navigate to Dashboard
- Tap "Register" → Navigate to Register Screen
- Show loading spinner during API call
- Display error toast for invalid credentials

**Validation Rules:**
- Email: Must be valid format
- Password: Cannot be empty

---

#### Screen 2: Register Screen
**Purpose:** New user account creation

**UI Elements:**
- "Create Account" header
- Full name input field
- Email input field
- Password input field (with strength indicator)
- Confirm password input field
- "Register" button
- "Already have an account? Login" link

**Interactions:**
- Tap "Register" → Validate inputs → Call `/auth/register` → Auto-login → Navigate to Dashboard
- Password strength indicator (weak/medium/strong)
- Show error for duplicate email

**Validation Rules:**
- Full name: Min 3 characters
- Email: Valid format
- Password: Min 8 characters, at least 1 uppercase, 1 number
- Confirm password: Must match password

---

#### Screen 3: Dashboard (Home Screen)
**Purpose:** Central hub showing all key information

**Layout Sections:**

1. **Header:**
   - App name/logo
   - Alert badge (shows unread count)
   - User profile icon

2. **Sensor Data Cards (3 cards in grid):**
   - Temperature Card: Shows current temp + icon
   - Humidity Card: Shows current humidity + icon
   - Soil Moisture Card: Shows current moisture + icon
   - Each card has timestamp "Updated 2 min ago"

3. **Weather Widget:**
   - Current day weather (icon, temp, condition)
   - "View 7-day forecast" button

4. **Quick Actions:**
   - Large "Detect Pest" button (primary CTA)
   - "View History" button

5. **Recent Alerts (if any):**
   - Shows last 2 unread alerts
   - "View All" link

**Interactions:**
- Pull-to-refresh: Refreshes all data
- Auto-refresh: Polls sensor data every 30 seconds
- Tap alert badge → Navigate to Alerts List
- Tap "Detect Pest" → Navigate to Pest Detection Screen
- Tap weather widget → Navigate to Weather Detail Screen
- Tap sensor card → Navigate to Sensor History Screen

---

#### Screen 4: Pest Detection Screen
**Purpose:** Capture/upload image for pest identification

**UI Elements:**
- Camera preview (full screen)
- "Take Photo" button (bottom center)
- "Choose from Gallery" button (bottom left)
- Back button (top left)
- Flash toggle (top right)

**Interactions:**
- Tap "Take Photo" → Capture image → Show preview with "Analyze" button
- Tap "Choose from Gallery" → Open gallery picker → Show preview
- Tap "Analyze" → Upload to `/detections/upload` → Show loading → Navigate to Results Screen
- Show progress indicator during upload/analysis

---

#### Screen 5: Detection Results Screen
**Purpose:** Display pest identification results

**UI Elements:**
- Uploaded image (top half)
- Pest name (large text)
- Confidence score (progress bar + percentage)
- Recommendations section (bulleted list)
- "Save to History" button (auto-saved, just confirmation)
- "Detect Another" button
- "Back to Dashboard" button

**Interactions:**
- Tap "Detect Another" → Navigate back to Pest Detection Screen
- Tap "Back to Dashboard" → Navigate to Dashboard
- Auto-save detection to history

---

#### Screen 6: Detection History Screen
**Purpose:** View past pest detections

**UI Elements:**
- List of detection cards (scrollable)
- Each card shows:
  - Thumbnail image
  - Pest name
  - Confidence score
  - Date/time
- Pull-to-refresh
- Empty state: "No detections yet"

**Interactions:**
- Tap card → Navigate to Detection Results Screen (read-only)
- Pull-to-refresh → Reload history from API
- Infinite scroll pagination

---

#### Screen 7: Weather Detail Screen
**Purpose:** Show 7-day weather forecast

**UI Elements:**
- Location name (Kuala Lumpur)
- List of 7 daily forecast cards:
  - Day name (Today, Tomorrow, Wed, etc.)
  - Weather icon
  - High/Low temperature
  - Condition text
  - Precipitation probability
  - Humidity percentage

**Interactions:**
- Pull-to-refresh → Reload forecast
- Back button → Return to Dashboard

---

#### Screen 8: Alerts List Screen
**Purpose:** View all alerts (unread and read)

**UI Elements:**
- Tabs: "Unread" | "All"
- List of alert cards:
  - Alert icon (based on type)
  - Alert message
  - Timestamp
  - Severity indicator (color-coded)
  - Read/unread visual state
- Empty state: "No alerts"

**Interactions:**
- Tap alert → Mark as read (call API) → Update UI
- Pull-to-refresh → Reload alerts
- Swipe to dismiss (marks as read)

---

#### Screen 9: Sensor History Screen
**Purpose:** View historical sensor data trends

**UI Elements:**
- Time range selector (24h, 7d, 30d)
- Line chart showing:
  - Temperature (red line)
  - Humidity (blue line)
  - Soil Moisture (green line)
- Legend
- Data table (below chart) with timestamps

**Interactions:**
- Tap time range → Reload data for selected range
- Pinch to zoom on chart
- Scroll data table

---

## 10. Non-Functional Requirements

### 10.1 Performance
- **API Response Time:** < 2 seconds (excluding ML inference)
- **ML Inference Time:** < 5 seconds per image
- **App Launch Time:** < 3 seconds on mid-range devices
- **Dashboard Load Time:** < 1 second (with cached data)
- **Image Upload:** Support up to 5MB images

### 10.2 Scalability
- **Concurrent Users:** Support 10 concurrent users (demo scenario)
- **Database:** Handle 10,000 detections without performance degradation
- **API Rate Limiting:** 100 requests/minute per user

### 10.3 Security
- **Authentication:** JWT tokens with 24-hour expiration
- **Password Storage:** bcrypt hashing (cost factor 12)
- **HTTPS:** All API communication over TLS 1.2+
- **Input Validation:** Sanitize all user inputs to prevent SQL injection
- **File Upload:** Validate file types and scan for malware (basic check)

### 10.4 Reliability
- **Uptime:** 95% during demo period (Week 13-14)
- **Error Handling:** Graceful degradation (show cached data if API fails)
- **Data Backup:** Daily database backups
- **Logging:** Comprehensive error logging for debugging

### 10.5 Usability
- **Language:** English only (MVP)
- **Accessibility:** Basic accessibility (readable fonts, color contrast)
- **Offline Mode:** Show last cached data when offline
- **Error Messages:** User-friendly error messages (no technical jargon)

### 10.6 Compatibility
- **Mobile OS:** Android 8.0+ (API 26+), iOS 12.0+
- **Screen Sizes:** Support 4.5" to 7" screens
- **Backend OS:** Linux (Ubuntu 20.04+)
- **Database:** PostgreSQL 13+ or SQLite 3.35+

---

## 11. Constraints & Assumptions

### 11.1 Constraints
- **Budget:** RM 0 (free tier services only)
- **Timeline:** 14 weeks (fixed deadline)
- **Team Size:** 1 integration lead + 2 ML team members (external)
- **Hardware:** No physical IoT sensors (simulation only)
- **Deployment:** Self-hosted server (no cloud budget)

### 11.2 Assumptions
- ✅ User has smartphone with camera (Android/iOS)
- ✅ User has internet connection (3G minimum)
- ✅ ML team will deliver trained model by Week 10 (70% confidence)
- ✅ OpenWeatherMap API will remain free (1000 calls/day)
- ✅ Server will have 99% uptime during demo period
- ✅ Users are comfortable with English interface
- ✅ Pest images will be clear enough for detection (not blurry)

### 11.3 Dependencies
- **External APIs:**
  - OpenWeatherMap API (weather data)
  - Roboflow API (backup ML service)
- **ML Team Deliverables:**
  - Trained pest detection model (TensorFlow/PyTorch)
  - Model API wrapper (REST endpoint)
- **Infrastructure:**
  - Your own server (Docker-ready)
  - Domain name with SSL certificate

---

## 12. Timeline & Milestones

### Phase 0: Setup (Week 1-2)
**Goal:** Development environment ready

**Milestones:**
- ✅ Backend repo initialized (FastAPI + PostgreSQL)
- ✅ Mobile repo initialized (Flutter)
- ✅ Database schema created and migrated
- ✅ Docker setup complete
- ✅ CI/CD pipeline configured (optional)

---

### Phase 1: Backend Development (Week 3-8)

#### Week 3: Authentication System
**Deliverables:**
- ✅ User registration endpoint
- ✅ Login endpoint (JWT generation)
- ✅ Auth middleware
- ✅ Password hashing
- ✅ Swagger documentation

#### Week 4: Sensor Data API
**Deliverables:**
- ✅ Synthetic data generator script
- ✅ Current readings endpoint
- ✅ Historical data endpoint
- ✅ Database seeding

#### Week 5-6: Pest Detection API
**Deliverables:**
- ✅ Image upload endpoint
- ✅ Mock ML service (returns fake predictions)
- ✅ Detection storage in database
- ✅ History endpoint (paginated)
- ✅ File storage setup

#### Week 7: Weather API
**Deliverables:**
- ✅ OpenWeatherMap integration
- ✅ Forecast endpoint
- ✅ Response caching (30 min)
- ✅ Error handling

#### Week 8: Alert System
**Deliverables:**
- ✅ Alert generation logic
- ✅ Alerts endpoint
- ✅ Mark as read endpoint
- ✅ Alert triggers (pest risk, weather warnings)

---

### Phase 2: Mobile Development (Week 9-12)

#### Week 9: Authentication Screens
**Deliverables:**
- ✅ Login screen
- ✅ Register screen
- ✅ JWT storage (SharedPreferences)
- ✅ API integration
- ✅ Form validation

#### Week 10: Dashboard Screen
**Deliverables:**
- ✅ Sensor data cards
- ✅ Weather widget
- ✅ Alert badge
- ✅ Pull-to-refresh
- ✅ Auto-refresh (30s polling)

#### Week 11: Pest Detection Flow
**Deliverables:**
- ✅ Camera screen
- ✅ Image picker
- ✅ Upload to API
- ✅ Results screen
- ✅ History screen

#### Week 12: Polish & Testing
**Deliverables:**
- ✅ UI/UX improvements
- ✅ Error handling
- ✅ Offline mode
- ✅ Bug fixes
- ✅ Performance optimization

---

### Phase 3: Integration & Deployment (Week 13-14)

#### Week 13: ML Integration
**Deliverables:**
- ✅ Replace mock ML service with real model (if available)
- ✅ Test accuracy and performance
- ✅ Fallback to Roboflow if needed
- ✅ End-to-end testing

#### Week 14: Final Deployment
**Deliverables:**
- ✅ Deploy backend to your server
- ✅ Build APK (Android)
- ✅ Test on real devices
- ✅ Create demo video
- ✅ Finalize documentation
- ✅ Prepare presentation

---

## 13. Risk Management

### Risk 1: ML Team Doesn't Deliver Model
**Probability:** 70% (High)  
**Impact:** High (core feature blocked)  
**Mitigation:**
- ✅ Build mock ML service first (Week 5)
- ✅ Test entire workflow with mock data
- ✅ Backup plan: Use Roboflow API (pre-trained model)
- ✅ Set deadline: Week 10 for ML team delivery

---

### Risk 2: Scope Creep
**Probability:** 90% (Very High)  
**Impact:** Medium (delays MVP)  
**Mitigation:**
- ✅ Strict MVP definition (this PRD)
- ✅ Weekly progress reviews
- ✅ Defer non-essential features to "Future Enhancements"
- ✅ Use AI assistance to speed up development

---

### Risk 3: Technical Skill Gap
**Probability:** 60% (Medium)  
**Impact:** Medium (slower development)  
**Mitigation:**
- ✅ Use AI coding assistants (GitHub Copilot, ChatGPT, Claude)
- ✅ Follow tutorials for unfamiliar tech
- ✅ Ask for help in online communities
- ✅ Simplify architecture (no WebSockets, no microservices)

---

### Risk 4: Server Downtime During Demo
**Probability:** 30% (Low)  
**Impact:** High (demo failure)  
**Mitigation:**
- ✅ Deploy to Render.com as backup
- ✅ Test deployment 1 week before demo
- ✅ Have local backend running as fallback
- ✅ Record demo video as backup

---

### Risk 5: OpenWeatherMap API Rate Limit
**Probability:** 20% (Low)  
**Impact:** Low (weather feature unavailable)  
**Mitigation:**
- ✅ Cache responses for 30 minutes
- ✅ Limit API calls to 1 per user per 30 min
- ✅ Show cached data if API fails
- ✅ Monitor daily usage

---

## 14. Acceptance Criteria

### 14.1 Feature-Level Acceptance

#### Authentication
- ✅ User can register with valid email/password
- ✅ User can log in and receive JWT token
- ✅ Token persists across app restarts
- ✅ Invalid credentials show error message
- ✅ Duplicate email registration is rejected

#### Pest Detection
- ✅ User can take photo with camera
- ✅ User can upload photo from gallery
- ✅ Detection completes within 5 seconds
- ✅ Results show pest name and confidence score
- ✅ Detection is saved to history
- ✅ User can view past detections

#### Dashboard
- ✅ Sensor data displays current readings
- ✅ Data refreshes every 30 seconds
- ✅ Weather widget shows 7-day forecast
- ✅ Alert badge shows unread count
- ✅ Pull-to-refresh updates all data

#### Alerts
- ✅ Pest risk alert generated when confidence > 80%
- ✅ Weather alert generated for severe conditions
- ✅ User can view alert list
- ✅ User can mark alert as read
- ✅ Unread alerts are visually distinct

---

### 14.2 System-Level Acceptance

#### Performance
- ✅ API responds within 2 seconds (95th percentile)
- ✅ App launches within 3 seconds
- ✅ Dashboard loads within 1 second (cached)
- ✅ No crashes during 30-minute usage session

#### Security
- ✅ Passwords are hashed (not stored in plaintext)
- ✅ JWT tokens expire after 24 hours
- ✅ All API calls use HTTPS
- ✅ Unauthorized requests return 401 error

#### Reliability
- ✅ App shows cached data when offline
- ✅ Error messages are user-friendly
- ✅ Backend logs errors for debugging
- ✅ Database backups run daily

#### Usability
- ✅ UI is intuitive (no training required)
- ✅ Error messages guide user to fix issues
- ✅ Loading states are clear (spinners, progress bars)
- ✅ App works on 4.5" to 7" screens

---

### 14.3 Demo Acceptance Criteria

**The demo is considered successful if:**
1. ✅ User can register and log in without errors
2. ✅ Dashboard displays sensor data and weather
3. ✅ User can upload pest image and get detection result
4. ✅ Detection is saved to history
5. ✅ Alert is generated for high-confidence detection
6. ✅ User can view alert and mark as read
7. ✅ No crashes or freezes during 5-minute demo
8. ✅ Backend API is accessible via HTTPS

---

## 15. Future Enhancements (Post-MVP)

**Not included in capstone project, but potential improvements:**

1. **Real IoT Sensors:**
   - Integrate with ESP32/Arduino sensors
   - Real-time data streaming via MQTT

2. **Advanced Analytics:**
   - ML-based pest outbreak predictions
   - Crop yield forecasting
   - Historical trend analysis

3. **Multi-Language Support:**
   - Bahasa Malaysia
   - Tamil
   - Mandarin

4. **Social Features:**
   - Community forum
   - Share detections with other farmers
   - Expert Q&A

5. **E-Commerce Integration:**
   - Pesticide marketplace
   - Fertilizer recommendations
   - Direct purchase from app

6. **Push Notifications:**
   - Real-time alerts (not polling)
   - Firebase Cloud Messaging

7. **Offline Mode:**
   - Full offline detection (on-device ML)
   - Sync when online

8. **Multi-Farm Support:**
   - Manage multiple farms
   - Switch between farm profiles

---

## 16. Glossary

| Term | Definition |
|------|------------|
| **JWT** | JSON Web Token - stateless authentication token |
| **ML** | Machine Learning - AI model for pest detection |
| **API** | Application Programming Interface - backend endpoints |
| **REST** | Representational State Transfer - API architecture |
| **Polling** | Repeatedly checking for updates at intervals |
| **Synthetic Data** | Artificially generated data (not from real sensors) |
| **Confidence Score** | ML model's certainty percentage (0-100%) |
| **Swagger** | API documentation tool (auto-generated) |
| **Docker** | Containerization platform for deployment |
| **Alembic** | Database migration tool for Python |

---

## 17. Appendices

### Appendix A: API Error Codes

| Code | Message | Description |
|------|---------|-------------|
| 400 | Bad Request | Invalid input data |
| 401 | Unauthorized | Missing or invalid JWT token |
| 403 | Forbidden | User lacks permission |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate resource (e.g., email) |
| 413 | Payload Too Large | Image exceeds 5MB |
| 422 | Unprocessable Entity | Validation error |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Backend error |
| 503 | Service Unavailable | ML service down |

---

### Appendix B: Environment Variables

**Backend (.env file):**
```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/agrisense
# or for SQLite: sqlite:///./agrisense.db

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# OpenWeatherMap
OPENWEATHER_API_KEY=your-api-key-here
OPENWEATHER_BASE_URL=https://api.openweathermap.org/data/2.5

# ML Service
ML_SERVICE_URL=http://localhost:8001/predict
ML_SERVICE_TIMEOUT=10

# File Storage
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE_MB=5

# Server
HOST=0.0.0.0
PORT=5000
DEBUG=False
```

**Mobile (config.dart):**
```dart
class Config {
  static const String apiBaseUrl = 'https://your-server.com/api/v1';
  static const int apiTimeout = 30; // seconds
  static const int pollInterval = 30; // seconds
  static const String defaultLocation = 'Kuala Lumpur';
}
```

---

### Appendix C: Testing Checklist

**Backend Tests:**
- [ ] User registration with valid data
- [ ] User registration with duplicate email (409 error)
- [ ] Login with correct credentials
- [ ] Login with wrong password (401 error)
- [ ] Protected endpoint without token (401 error)
- [ ] Image upload with valid file
- [ ] Image upload with oversized file (413 error)
- [ ] Sensor data generation (30-second intervals)
- [ ] Weather API caching (30-minute TTL)
- [ ] Alert generation for high-confidence detection

**Mobile Tests:**
- [ ] Login screen validation
- [ ] Register screen validation
- [ ] Dashboard data refresh
- [ ] Camera capture and upload
- [ ] Gallery image selection
- [ ] Detection results display
- [ ] History pagination
- [ ] Alert badge update
- [ ] Offline mode (cached data)
- [ ] Token expiration handling

---

## Document Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| **Integration Lead** | [Your Name] | __________ | _______ |
| **Academic Supervisor** | [Supervisor Name] | __________ | _______ |
| **ML Team Lead** | [ML Lead Name] | __________ | _______ |

---

**End of PRD**

*This document is a living document and will be updated as requirements evolve during the project lifecycle.*
