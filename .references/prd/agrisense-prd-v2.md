# AgriSense - Product Requirements Document (PRD)

**Version:** 2.0  
**Last Updated:** January 2025  
**Project Type:** Final Year Capstone Project (Bachelor of Software Engineering)  
**Project Duration:** 14 Weeks  
**Document Owner:** Integration Lead

> **📚 PROJECT CONTEXT**  
> This is a Final Year Project (FYP) serving as a proof of concept for an IoT-driven agricultural early warning system. The focus is on demonstrating technical capabilities and solving real agricultural problems within academic constraints. This is NOT a production-ready commercial application.

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Project Overview](#2-project-overview)
3. [Goals & Success Metrics](#3-goals--success-metrics)
4. [User Personas & Stories](#4-user-personas--stories)
5. [Feature Requirements](#5-feature-requirements)
6. [Technical Architecture](#6-technical-architecture)
7. [Database Schema](#7-database-schema)
8. [API Specifications](#8-api-specifications)
9. [Mobile App Screens](#9-mobile-app-screens)
10. [Non-Functional Requirements](#10-non-functional-requirements)
11. [Constraints & Assumptions](#11-constraints--assumptions)
12. [Timeline & Milestones](#12-timeline--milestones)
13. [Risk Management](#13-risk-management)
14. [Acceptance Criteria](#14-acceptance-criteria)

---

## 1. Executive Summary

**AgriSense** is an IoT-driven **Early Warning System for Weather and Pest Risk Management** designed for Malaysian farmers. This is a **proof-of-concept capstone project** where sensor data is sourced from weather APIs (simulating IoT sensors) and predictions are generated using custom ML models.

### Key Highlights

| Aspect | Description |
|--------|-------------|
| **Core Feature 1** | 🌤️ Weather Early Warning - ML-powered weather prediction, real-time monitoring, anomaly detection, and actionable alerts |
| **Core Feature 2** | 🐛 Pest Risk Management - AI-powered pest detection from images, weather-based pest risk prediction, and prevention recommendations |
| **Target Users** | Small-to-medium scale farmers in Malaysia (single crop focus: Rice) |
| **Platform** | Cross-platform mobile app (Flutter) + REST API backend (FastAPI/Python) |
| **AI Integration** | Custom ML models for weather/pest + OpenRouter API for recommendations and chatbot |
| **Deployment** | Self-hosted server (Docker) + Render.com backup |

### What Makes This an "Early Warning" System

1. **Weather Early Warning:** Custom ML model predicts weather anomalies (heavy rain, extreme heat, storms) before they occur, giving farmers time to prepare
2. **Pest Risk Early Warning:** Weather-pest correlation analysis predicts pest outbreak risk based on environmental conditions, alerting farmers before pests appear

---

## 2. Project Overview

### 2.1 Problem Statement

Malaysian farmers face **three critical challenges** that threaten crop yields and farm profitability:

**Problem 1: Unpredictable Weather Conditions Affect Farming Decisions**
- Sudden heavy rains, storms, and extreme temperatures damage crops
- Lack of timely weather warnings leads to preventable losses
- Farmers cannot plan irrigation, harvesting, or protective measures effectively

**Problem 2: Lack of Early Detection of Pest Infestations**
- Pest infestations spread rapidly without early detection
- Farmers lack tools to identify pests accurately
- Reactive pesticide application occurs after damage is already done
- No predictive system warns farmers before pest outbreaks occur

**Problem 3: Limited Accessibility to Real-time Decision Support**
- Farmers in rural areas struggle to access intuitive, real-time systems
- Complex data is not translated into simple, actionable advice
- Multiple apps needed for weather, pest info, and farming guidance

**Result:** Farmers experience significant crop losses, reduced yields, and financial instability due to lack of actionable, real-time information and early warnings.

### 2.2 Solution

AgriSense provides a **unified early warning platform** that addresses all three challenges:

**🌤️ Weather Early Warning System:**
- Real-time weather monitoring via OpenWeatherMap API (acting as sensor data)
- Custom ML model for weather prediction and anomaly detection
- Automated alerts for heavy rain, storms, extreme heat, and dry spells
- Crop-specific recommendations for weather conditions

**🐛 Pest Risk Management System:**
- AI-powered pest identification from smartphone photos
- Weather-based pest risk prediction using pest-weather correlations
- Early warning alerts when conditions favor pest outbreaks
- AI-generated treatment and prevention recommendations

**💬 AI-Powered Decision Support:**
- Integrated chatbot for farmer questions and guidance
- Context-aware recommendations based on location, crop, and conditions
- Simple, actionable advice for farmers with limited technical knowledge

**📱 Unified Mobile Platform:**
- Single app for weather, pest management, and farming advice
- Real-time data updates
- Alert system for weather and pest warnings
- Detection history and tracking

### 2.3 Scope

**In Scope (MVP):**
- ✅ User authentication (register, login, logout)
- ✅ User profile with farm location and crop type
- ✅ Weather monitoring (current conditions + 7-day forecast)
- ✅ Weather prediction (custom ML model)
- ✅ Weather alerts (heavy rain, extreme heat, storms, dry spells)
- ✅ Pest detection (image upload → ML analysis)
- ✅ Pest risk prediction (weather-based correlations)
- ✅ Pest risk alerts (early warning before outbreak)
- ✅ AI-generated recommendations (OpenRouter API)
- ✅ AI chatbot for farmer queries
- ✅ Manual pest reporting (for unidentified pests)
- ✅ Detection and alert history
- ✅ Dashboard with unified overview

**Out of Scope (Future Enhancements):**
- ❌ Physical IoT sensors (using weather API as data source)
- ❌ Real-time WebSocket connections (polling approach)
- ❌ Multi-language support (English only)
- ❌ Multiple farms per user (single farm per user)
- ❌ Farm sector management (single location per farm)
- ❌ Push notifications (in-app alerts only)
- ❌ Notification preferences (all alerts enabled)
- ❌ Password reset flow (admin reset if needed)
- ❌ Social login (username/password only)
- ❌ Offline mode

---

## 3. Goals & Success Metrics

### 3.1 Project Goals

| # | Goal Type | Description |
|---|-----------|-------------|
| 1 | **Functional** | Deliver working end-to-end workflows for weather early warning AND pest risk management |
| 2 | **Academic** | Meet capstone project requirements (documentation, demo, defense) |
| 3 | **Technical** | Demonstrate full-stack integration (mobile + backend + ML + external APIs + AI) |
| 4 | **Problem-Solving** | Prove the concept solves real farmer problems with early warnings |
| 5 | **Learning** | Gain hands-on experience with modern development tools and AI integration |

### 3.2 Success Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Core Feature Completion | 100% of weather AND pest features working | Manual testing checklist |
| Weather Prediction | ML model provides predictions beyond raw API data | Compare ML output vs raw API |
| Weather Alert Accuracy | Alerts generated within 5 minutes of threshold breach | Backend logs |
| Pest Detection Accuracy | > 70% confidence for known pests | ML model evaluation |
| Pest Risk Prediction | Correlations trigger appropriate warnings | Manual scenario testing |
| API Response Time | < 2 seconds (excluding ML inference) | Backend logs |
| ML Inference Time | < 5 seconds per image | Backend logs |
| AI Recommendation Quality | Relevant, actionable advice generated | Manual review |
| Chatbot Response Time | < 3 seconds | Backend logs |
| App Crash Rate | < 5% during demo | Error tracking |
| Code Coverage | > 60% for critical paths | Test coverage report |
| Documentation | All APIs documented in Swagger | Swagger UI review |
| Demo Readiness | 5-minute demo showcasing all features | Rehearsal |

---

## 4. User Personas & Stories

### 4.1 Primary Persona: Ahmad (Rice Farmer)

| Attribute | Description |
|-----------|-------------|
| **Age** | 35-50 |
| **Location** | Rural Malaysia (Kedah/Perak) |
| **Farm Size** | 2-5 acres |
| **Crop** | Rice (primary focus for this FYP) |
| **Tech Literacy** | Basic smartphone user |

**Pain Points:**
- Sudden storms and heavy rains damage crops without warning
- Cannot identify pest species accurately
- Discovers infestations too late, after visible damage
- No single app for weather AND pest management
- Complex apps are difficult to use

**Goals:**
- Receive early warnings for weather threats to protect crops
- Get alerted about pest risk BEFORE seeing pests in field
- Identify pests quickly when found
- Receive simple, actionable advice
- Use ONE app for all farming decisions

### 4.2 User Stories

#### Epic 1: User Authentication & Setup
| ID | Story | Priority |
|----|-------|----------|
| US-1.1 | As a farmer, I want to register with my farm details so that I can receive relevant information | Must Have |
| US-1.2 | As a farmer, I want to select my farm location so that weather data is accurate for my area | Must Have |
| US-1.3 | As a farmer, I want to specify my crop type so that recommendations are relevant | Must Have |
| US-1.4 | As a farmer, I want to log in securely so that my data is protected | Must Have |
| US-1.5 | As a farmer, I want my session to persist so that I don't log in repeatedly | Must Have |

#### Epic 2: Weather Early Warning System
| ID | Story | Priority |
|----|-------|----------|
| US-2.1 | As a farmer, I want to see current weather conditions so that I know the situation now | Must Have |
| US-2.2 | As a farmer, I want to see a 7-day forecast so that I can plan activities | Must Have |
| US-2.3 | As a farmer, I want ML-enhanced weather predictions so that forecasts are more accurate | Must Have |
| US-2.4 | As a farmer, I want alerts for heavy rain so that I can protect crops from flooding | Must Have |
| US-2.5 | As a farmer, I want alerts for extreme heat so that I can increase irrigation | Must Have |
| US-2.6 | As a farmer, I want alerts for storms so that I can secure equipment | Must Have |
| US-2.7 | As a farmer, I want crop-specific recommendations with alerts so that I know what to do | Must Have |
| US-2.8 | As a farmer, I want to see historical weather data so that I can identify patterns | Should Have |

#### Epic 3: Pest Detection System
| ID | Story | Priority |
|----|-------|----------|
| US-3.1 | As a farmer, I want to photograph a pest so that the app identifies it | Must Have |
| US-3.2 | As a farmer, I want to upload an existing photo so that I can analyze saved images | Must Have |
| US-3.3 | As a farmer, I want to see pest name and confidence so that I can verify detection | Must Have |
| US-3.4 | As a farmer, I want AI-generated recommendations so that I know how to treat it | Must Have |
| US-3.5 | As a farmer, I want danger level assessment so that I know urgency | Must Have |
| US-3.6 | As a farmer, I want to retry if detection fails so that I can get better results | Must Have |
| US-3.7 | As a farmer, I want to report unidentified pests so that I still get help | Should Have |
| US-3.8 | As a farmer, I want to view detection history so that I can track patterns | Should Have |

#### Epic 4: Pest Risk Early Warning
| ID | Story | Priority |
|----|-------|----------|
| US-4.1 | As a farmer, I want pest risk predictions based on weather so that I can prepare before outbreaks | Must Have |
| US-4.2 | As a farmer, I want alerts when conditions favor pest outbreaks so that I can take preventive action | Must Have |
| US-4.3 | As a farmer, I want prevention tips with pest risk alerts so that I know what to do | Must Have |

#### Epic 5: AI Chatbot
| ID | Story | Priority |
|----|-------|----------|
| US-5.1 | As a farmer, I want to ask questions in chat so that I get farming advice | Should Have |
| US-5.2 | As a farmer, I want to upload images in chat so that I can get visual analysis | Should Have |
| US-5.3 | As a farmer, I want context-aware responses so that advice is relevant to my situation | Should Have |

#### Epic 6: Alert System
| ID | Story | Priority |
|----|-------|----------|
| US-6.1 | As a farmer, I want all alerts in one place so that I don't miss warnings | Must Have |
| US-6.2 | As a farmer, I want to see alert severity so that I prioritize urgent ones | Must Have |
| US-6.3 | As a farmer, I want actionable recommendations with alerts so that I know what to do | Must Have |
| US-6.4 | As a farmer, I want to mark alerts as read so that I track what I've addressed | Must Have |

---

## 5. Feature Requirements

### 5.1 Feature: User Authentication & Profile

**Description:** User registration and login system with farm profile setup including location and crop type.

**Functional Requirements:**
| ID | Requirement |
|----|-------------|
| FR-1.1 | System shall allow users to register with username, password, full name |
| FR-1.2 | System shall require farm location selection (Malaysian states/districts dropdown) |
| FR-1.3 | System shall require primary crop type selection |
| FR-1.4 | System shall validate password strength (minimum 6 characters) |
| FR-1.5 | System shall hash passwords using bcrypt before storing |
| FR-1.6 | System shall generate JWT tokens upon successful login (7-day expiry) |
| FR-1.7 | System shall validate JWT tokens for protected endpoints |
| FR-1.8 | System shall store location coordinates for weather API queries |

**Location Options (Malaysian States/Districts):**
- Perlis, Kedah, Penang, Perak, Selangor, Negeri Sembilan, Melaka, Johor, Pahang, Terengganu, Kelantan, Sabah, Sarawak, Kuala Lumpur, Labuan, Putrajaya

**Crop Type Options:**
- Rice (primary for FYP)
- Vegetables, Corn, Oil Palm, Rubber (for extensibility)

**Acceptance Criteria:**
- ✅ User can register with all required fields
- ✅ Location selection shows Malaysian states with coordinates
- ✅ Crop type selection available
- ✅ Duplicate username returns error
- ✅ Invalid credentials return 401
- ✅ JWT token works for protected endpoints

---

### 5.2 Feature: Weather Early Warning System

**Description:** Real-time weather monitoring using OpenWeatherMap API (as sensor data source) combined with custom ML model for enhanced predictions and anomaly detection.

**Functional Requirements:**
| ID | Requirement |
|----|-------------|
| FR-2.1 | System shall fetch weather data from OpenWeatherMap API based on user's location |
| FR-2.2 | System shall cache weather data for 30 minutes to reduce API calls |
| FR-2.3 | System shall display current conditions (temperature, humidity, weather, wind) |
| FR-2.4 | System shall display 7-day forecast |
| FR-2.5 | System shall process weather data through custom ML model for predictions |
| FR-2.6 | System shall detect weather anomalies using ML model |
| FR-2.7 | System shall generate alerts when thresholds are exceeded |
| FR-2.8 | System shall call AI API (OpenRouter) for crop-specific recommendations |
| FR-2.9 | System shall run weather check every 30 minutes (background job) |
| FR-2.10 | System shall store historical weather data for trend analysis |

**Weather Data Points:**
- Temperature (°C)
- Humidity (%)
- Weather condition (clear, rain, cloudy, storm)
- Wind speed (km/h)
- Precipitation (mm)
- 7-day forecast (daily high/low, conditions, precipitation probability)

**Alert Thresholds (Malaysia-Specific):**
| Alert Type | Threshold | Severity | Trigger |
|------------|-----------|----------|---------|
| Heavy Rain Warning | > 60mm in 24hrs | High | Immediate crop protection needed |
| Extreme Heat Alert | > 35°C | Medium | Irrigation and shade needed |
| Strong Wind Warning | > 50 km/h | High | Secure equipment, harvest if ready |
| Prolonged Dry Spell | < 5mm over 7 days | Medium | Increase irrigation planning |
| High Humidity Alert | > 90% for 48+ hrs | Medium | Fungal disease risk |
| Low Temperature | < 20°C | Low | Rare, affects highland crops |

**AI Recommendation Integration:**
When alert is generated, system calls OpenRouter API with context:
```
Context: {crop_type}, {location}, {weather_condition}, {alert_type}
Request: Generate 3-5 specific actionable recommendations for farmer
```

**Acceptance Criteria:**
- ✅ Weather displays correctly for user's selected location
- ✅ 7-day forecast shows with icons and data
- ✅ ML model processes weather data and provides predictions
- ✅ Alerts generated within 5 minutes of threshold breach
- ✅ Alerts include AI-generated recommendations
- ✅ Weather cache reduces redundant API calls
- ✅ Historical data stored and viewable

---

### 5.3 Feature: Pest Detection System

**Description:** AI-powered pest identification from uploaded images with confidence scoring, danger assessment, and treatment recommendations.

**Functional Requirements:**
| ID | Requirement |
|----|-------------|
| FR-3.1 | System shall accept image uploads (JPEG/PNG, max 5MB) |
| FR-3.2 | System shall send images to pest detection ML model |
| FR-3.3 | System shall return pest name and confidence score |
| FR-3.4 | System shall implement tiered response based on confidence |
| FR-3.5 | System shall call AI API for recommendations when pest detected |
| FR-3.6 | System shall assess danger level (Low/Medium/High) |
| FR-3.7 | System shall store detection results in database |
| FR-3.8 | System shall track retry attempts for failed detections |
| FR-3.9 | System shall offer manual reporting after 3 failed attempts |
| FR-3.10 | System shall generate alert for high-danger detections |

**Confidence Tiering:**
| Confidence | Response | Action |
|------------|----------|--------|
| ≥ 70% | Successful detection | Show pest info + AI recommendations |
| 50-69% | Partial match | Show possible pest + "Try again or report" option |
| < 50% | Unknown | Prompt retry with tips, after 3 fails → manual report |

**Retry System:**
| Attempt | Message |
|---------|---------|
| 1st fail | "Image unclear. Please try again with better lighting and focus on the pest." |
| 2nd fail | "Still having trouble. Tips: Get closer, ensure pest is centered, avoid shadows." |
| 3rd fail | "Unable to identify. Would you like to report this pest for assistance?" |

**AI Recommendation Request:**
```
Context: Detected {pest_name} with {confidence}% confidence
Crop: {crop_type}
Weather: {current_conditions}
Request: Provide pest description, danger level, 3 treatment options, prevention tips
```

**Acceptance Criteria:**
- ✅ User can upload image from camera or gallery
- ✅ Detection completes within 5 seconds
- ✅ Results show pest name, confidence, danger level
- ✅ AI recommendations are relevant and actionable
- ✅ Low confidence triggers retry flow
- ✅ After 3 fails, manual report option appears
- ✅ Detection saved to history
- ✅ High-danger detection generates alert

---

### 5.4 Feature: Pest Risk Early Warning

**Description:** Predictive pest risk alerts based on weather-pest correlations, warning farmers before pest outbreaks occur.

**Functional Requirements:**
| ID | Requirement |
|----|-------------|
| FR-4.1 | System shall maintain pest-weather correlation reference data |
| FR-4.2 | System shall check weather against pest risk conditions every 30 minutes |
| FR-4.3 | System shall generate pest risk alerts when conditions match |
| FR-4.4 | System shall include specific pest predictions in alerts |
| FR-4.5 | System shall include prevention tips in pest risk alerts |
| FR-4.6 | System shall filter correlations by user's crop type |

**Pest-Weather Correlations (Rice Crop):**

| Pest | Risk Conditions | Risk Level |
|------|-----------------|------------|
| Rice Stem Borer | Temp 25-35°C, Humidity >70%, after heavy rain | High |
| Rice Leaf Folder | Temp 25-30°C, Humidity 60-80%, cloudy | Medium |
| Brown Planthopper | Humidity >85%, dense canopy conditions | High |
| Rice Bug | Dry periods during grain filling stage | Medium |
| Rice Blast (fungal) | Humidity >90% for 48hrs, Temp 24-28°C | High |
| Bacterial Leaf Blight | Heavy rain + flooding + high humidity | High |
| Sheath Blight | Humidity >85%, dense planting | Medium |
| Green Leafhopper | Warm humid conditions, Temp 25-32°C | Medium |

**Alert Example:**
```json
{
  "alert_type": "pest_risk_warning",
  "severity": "high",
  "title": "Elevated Rice Stem Borer Risk",
  "message": "Weather conditions in the next 3-5 days favor Rice Stem Borer activity.",
  "risk_factors": ["High humidity (85%)", "Temperature 28°C", "Recent rainfall"],
  "predicted_pest": "Rice Stem Borer",
  "recommendations": [
    "Increase field monitoring frequency",
    "Check rice stems for entry holes",
    "Consider preventive Trichogramma release",
    "Prepare neem-based spray if signs detected"
  ],
  "confidence_note": "Based on weather-pest correlation data"
}
```

**Acceptance Criteria:**
- ✅ Pest risk check runs every 30 minutes
- ✅ Correlations filtered by user's crop type
- ✅ Alert generated when conditions match risk patterns
- ✅ Alert includes specific pest prediction
- ✅ Prevention recommendations included
- ✅ Alert clearly marked as "risk prediction" not confirmed detection

---

### 5.5 Feature: Manual Pest Reporting

**Description:** Fallback mechanism for farmers to report pests that the AI cannot identify, still providing assistance through general AI advice.

**Functional Requirements:**
| ID | Requirement |
|----|-------------|
| FR-5.1 | System shall offer manual reporting after 3 failed detection attempts |
| FR-5.2 | System shall collect: image, description (optional), observed severity |
| FR-5.3 | System shall call AI API for best-guess analysis and general advice |
| FR-5.4 | System shall store report for potential future model improvement |
| FR-5.5 | System shall provide general pest management guidance |

**Report Form Fields:**
- Image (required) - already uploaded from failed attempts
- Description (optional) - "Describe what you see"
- Observed Severity (required) - Minor / Moderate / Severe

**AI Response Request:**
```
Context: Farmer uploaded image of unknown pest
Description: {user_description}
Severity observed: {severity}
Crop: {crop_type}
Request: Provide best-guess identification, general pest management advice, when to seek expert help
```

**Acceptance Criteria:**
- ✅ Manual report option appears after 3 failed detections
- ✅ Form captures image, description, severity
- ✅ AI provides helpful general advice
- ✅ Report saved to database
- ✅ Farmer receives actionable guidance even without positive ID

---

### 5.6 Feature: AI Chatbot

**Description:** Conversational AI assistant for farmer queries, providing context-aware advice and supporting image uploads for visual analysis.

**Functional Requirements:**
| ID | Requirement |
|----|-------------|
| FR-6.1 | System shall provide chat interface for text queries |
| FR-6.2 | System shall support image uploads within chat |
| FR-6.3 | System shall gather context (location, crop, weather, recent detections) |
| FR-6.4 | System shall construct prompts with user context |
| FR-6.5 | System shall call OpenRouter API for responses |
| FR-6.6 | System shall maintain conversation within session (not persisted) |
| FR-6.7 | System shall route image uploads to pest detection flow |

**Context Injection:**
```
System Context:
- Farmer location: {location}
- Crop type: {crop_type}
- Current weather: {weather_summary}
- Recent alerts: {recent_alerts}
- Recent detections: {recent_detections}

User Question: {user_message}

Instructions: Provide helpful, practical farming advice. Keep responses concise. 
If asked about pests, recommend using the pest detection feature for accurate ID.
```

**Example Interactions:**
| User Query | Expected Response Type |
|------------|----------------------|
| "Why are my rice leaves turning yellow?" | Diagnostic questions + possible causes + recommendations |
| "Is it safe to fertilize today?" | Check weather context, provide advice |
| "What pest is this?" + image | Route to pest detection, return results in chat |
| "How do I prevent stem borer?" | Prevention tips specific to rice + current season |

**Acceptance Criteria:**
- ✅ Chat interface functional
- ✅ Text queries receive relevant responses
- ✅ Image uploads trigger pest detection
- ✅ Responses consider user's context (location, crop, weather)
- ✅ Conversation flows naturally within session
- ✅ Response time < 3 seconds

---

### 5.7 Feature: Alert System

**Description:** Unified alert management for weather warnings, pest detections, and pest risk predictions.

**Functional Requirements:**
| ID | Requirement |
|----|-------------|
| FR-7.1 | System shall aggregate all alert types in one view |
| FR-7.2 | System shall display alert severity (Low/Medium/High) |
| FR-7.3 | System shall show alert badge count on dashboard |
| FR-7.4 | System shall allow marking alerts as read |
| FR-7.5 | System shall sort alerts by timestamp (newest first) |
| FR-7.6 | System shall include recommendations in all alerts |
| FR-7.7 | System shall distinguish between alert types visually |

**Alert Types:**
| Type | Source | Icon/Color |
|------|--------|------------|
| weather_heavy_rain | Weather check | 🌧️ Blue |
| weather_extreme_heat | Weather check | 🌡️ Orange |
| weather_storm | Weather check | ⛈️ Purple |
| weather_dry_spell | Weather check | ☀️ Yellow |
| pest_detection | Pest detection | 🐛 Red |
| pest_risk_warning | Pest risk check | ⚠️ Amber |

**Acceptance Criteria:**
- ✅ All alert types appear in unified list
- ✅ Severity clearly indicated
- ✅ Badge shows unread count
- ✅ Mark as read updates UI immediately
- ✅ Recommendations included in all alerts
- ✅ Alert details accessible on tap

---

### 5.8 Feature: Dashboard

**Description:** Central hub displaying weather overview, active alerts, recent activity, and quick actions.

**Functional Requirements:**
| ID | Requirement |
|----|-------------|
| FR-8.1 | System shall display current weather summary |
| FR-8.2 | System shall show active/unread alert count |
| FR-8.3 | System shall display recent alerts (top 3) |
| FR-8.4 | System shall show recent pest detections (top 3) |
| FR-8.5 | System shall provide quick action buttons |
| FR-8.6 | System shall auto-refresh on app foreground |
| FR-8.7 | System shall support pull-to-refresh |

**Dashboard Sections:**
1. **Weather Card** - Current conditions + "View Forecast" button
2. **Alert Banner** - Active alerts count + severity indicator
3. **Recent Alerts** - Top 3 alerts with tap to view
4. **Quick Actions** - "Detect Pest" button, "Chat" button
5. **Recent Detections** - Last 3 detections with thumbnails

**Acceptance Criteria:**
- ✅ Dashboard loads within 2 seconds
- ✅ All sections populated with relevant data
- ✅ Quick actions navigate correctly
- ✅ Pull-to-refresh updates all data
- ✅ Alert badge updates in real-time

---

## 6. Technical Architecture

### 6.1 System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                       Flutter Mobile App                         │
│  (Android/iOS - Cross-platform)                                 │
│  - UI Screens (Auth, Dashboard, Detection, Chat, Alerts)        │
│  - State Management (Provider/Riverpod)                         │
│  - HTTP Client (http/dio package)                               │
│  - Local Storage (SharedPreferences for JWT)                    │
│  - Camera/Image Picker                                          │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          │ HTTPS REST API
                          │
┌─────────────────────────▼───────────────────────────────────────┐
│                   FastAPI Backend (Python 3.10+)                 │
│  - Authentication (JWT)                                          │
│  - Weather Service (OpenWeatherMap + ML Model)                   │
│  - Pest Detection Service (ML Model)                             │
│  - Pest Risk Service (Correlation Engine)                        │
│  - AI Service (OpenRouter API)                                   │
│  - Alert Service                                                 │
│  - Background Jobs (Weather/Pest Risk Checks)                    │
└────────┬──────────────────┬──────────────────┬──────────────────┘
         │                  │                  │
         ▼                  ▼                  ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────────────┐
│  PostgreSQL DB  │ │   ML Models     │ │   External APIs         │
│  - Users        │ │  - Weather      │ │  - OpenWeatherMap       │
│  - Detections   │ │    Prediction   │ │  - OpenRouter (AI)      │
│  - Alerts       │ │  - Pest         │ │                         │
│  - Weather Cache│ │    Detection    │ │                         │
│  - Pest Reports │ │                 │ │                         │
│  - Correlations │ │                 │ │                         │
└─────────────────┘ └─────────────────┘ └─────────────────────────┘
```

### 6.2 Technology Stack

| Layer | Technology | Justification |
|-------|------------|---------------|
| **Mobile** | Flutter | Cross-platform, teammate already built ~60% of app |
| **Backend** | FastAPI (Python 3.10+) | Fast, async, auto Swagger docs, excellent ML integration |
| **Database** | PostgreSQL | Relational, ACID compliant, JSON support for flexible data |
| **Authentication** | JWT | Stateless, mobile-friendly, 7-day expiry |
| **Weather API** | OpenWeatherMap | Reliable, free tier (1000 calls/day), good documentation |
| **Weather ML** | TBD (Docker microservice) | Team-built for weather condition classification (framework pending) |
| **Pest ML** | TBD (Docker microservice) | Team-built for pest type classification (framework pending) |
| **AI API** | OpenRouter | Generates recommendations for weather and pest (not classification) |
| **Deployment** | Docker + Self-hosted | Cost-effective, full control |
| **Backup Hosting** | Render.com | Easy deployment, HTTPS included |

> **⚠️ NOTE:** ML framework (TensorFlow/PyTorch/other) is TBD - awaiting teammate confirmation.

### 6.3 Data Flow

**Weather Alert Flow:**
```
Background Job (every 30 min)
    → Fetch weather from OpenWeatherMap (by user locations)
    → Cache weather data
    → Run through Weather ML Model
    → Check against alert thresholds
    → IF threshold exceeded:
        → Call OpenRouter for recommendations
        → Create alert record
        → Alert available on next app refresh
```

**Pest Detection Flow:**
```
User uploads image
    → Backend receives image
    → Send to Pest ML Model
    → Receive: pest_name, confidence
    → IF confidence >= 70%:
        → Call OpenRouter for recommendations
        → Save detection
        → IF danger = high: Create alert
        → Return results to app
    → ELSE IF confidence 50-69%:
        → Return partial match + retry option
    → ELSE:
        → Increment retry counter
        → IF retries >= 3: Offer manual report
        → ELSE: Return retry prompt
```

**Pest Risk Prediction Flow:**
```
Background Job (every 30 min)
    → Get latest weather data from cache
    → Load pest-weather correlations for crop type
    → FOR each correlation:
        → Check if weather matches risk conditions
        → IF match:
            → Create pest risk alert
            → Include prevention recommendations
```

### 6.4 Background Jobs

| Job | Frequency | Purpose |
|-----|-----------|---------|
| Weather Fetch | Every 30 minutes | Update weather cache, run ML predictions |
| Weather Alert Check | Every 30 minutes | Check thresholds, generate alerts |
| Pest Risk Check | Every 30 minutes | Check correlations, generate risk alerts |
| Cache Cleanup | Daily | Remove old weather cache entries |

### 6.5 ML Architecture (Classification vs Recommendations)

The system uses **two types of intelligence** with clear separation of concerns:

1. **ML Models (Framework TBD)** - Classification only (what is it?)
2. **AI API (OpenRouter)** - Recommendations and actions (what to do?)

> **⚠️ NOTE:** ML framework (TensorFlow/PyTorch/other) is TBD - awaiting teammate confirmation.
> The architecture is framework-agnostic; only the Docker configuration will change based on framework.

#### ML Model Outputs

**Weather ML Model:**
- **Input:** Weather data (temperature, humidity, pressure, wind speed, etc.)
- **Output:** Weather condition classification + confidence
```json
{
  "condition": "heavy_rain",  // Categories TBD - awaiting teammate's model
  "confidence": 0.92
}
```
- **Note:** Does NOT generate recommendations - that's handled by AI API

**Pest ML Model:**
- **Input:** Image (base64 encoded)
- **Output:** Pest type classification + confidence
```json
{
  "pest_type": "Rice Stem Borer",  // Pest types TBD - awaiting teammate's model
  "confidence": 0.87
}
```
- **Note:** Does NOT generate recommendations - that's handled by AI API

#### When to Use What

| Scenario | ML Model | AI API | Correlation Table |
|----------|----------|--------|-------------------|
| Weather condition classification | ✅ Weather ML | ❌ | ❌ |
| Weather farming recommendations | ❌ | ✅ OpenRouter | ❌ |
| Pest detection from image | ✅ Pest ML | ❌ | ❌ |
| Pest treatment recommendations | ❌ | ✅ OpenRouter | ❌ |
| Pest risk prediction (from weather) | ❌ | ❌ | ✅ Use stored `prevention_tips` |
| Chatbot Q&A | ❌ | ✅ OpenRouter | ❌ |

#### Key Decision: No AI API for Pest Risk Warnings

Pest risk predictions based on weather-pest correlations use **pre-stored `prevention_tips`** from the `pest_weather_correlations` table instead of calling the AI API. Rationale:
1. Prevention tips are consistent and vetted (from MARDI, IRRI sources)
2. Reduces API costs and latency
3. Works offline if needed
4. AI API is reserved for actual pest detections and weather recommendations

#### ML Service Architecture

The ML models run as a **separate microservice** (Docker container) on port 8001:

```
┌─────────────────────────────────────────────────────────────────┐
│                    ML SERVICE (Port 8001)                        │
│               ML Models via Docker (Framework TBD)               │
├─────────────────────────────────────────────────────────────────┤
│  POST /predict/weather              POST /predict/pest           │
│  Input: weather features            Input: image (base64)        │
│  Output: condition + confidence     Output: pest_type + conf     │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                   FASTAPI BACKEND (Port 8000)                    │
│                                                                  │
│  - Receives ML classification results                            │
│  - Calls AI API (OpenRouter) for recommendations                 │
│  - Checks pest-weather correlations (uses stored tips)           │
│  - Generates alerts with recommendations                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 7. Database Schema

### 7.1 Entity Relationship Overview

```
users (1) ──────< (N) pest_detections
users (1) ──────< (N) pest_reports
users (1) ──────< (N) alerts
weather_cache (shared across users by location)
pest_weather_correlations (reference data, not user-specific)
```

### 7.2 Table Definitions

#### Table: `users`
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    farm_location_name VARCHAR(100) NOT NULL,  -- "Kedah", "Perak", etc.
    farm_location_lat DECIMAL(10, 8) NOT NULL,
    farm_location_lng DECIMAL(11, 8) NOT NULL,
    crop_type VARCHAR(50) NOT NULL DEFAULT 'rice',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_username ON users(username);
```

#### Table: `pest_detections`
```sql
CREATE TABLE pest_detections (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    image_url VARCHAR(500) NOT NULL,
    pest_name VARCHAR(100) NOT NULL,
    confidence DECIMAL(5, 2) NOT NULL CHECK (confidence >= 0 AND confidence <= 100),
    danger_level VARCHAR(20) NOT NULL CHECK (danger_level IN ('low', 'medium', 'high')),
    ai_recommendations JSONB,  -- Array of recommendation strings
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_detections_user_id ON pest_detections(user_id);
CREATE INDEX idx_detections_detected_at ON pest_detections(detected_at DESC);
```

#### Table: `pest_reports`
```sql
CREATE TABLE pest_reports (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    image_url VARCHAR(500) NOT NULL,
    description TEXT,
    observed_severity VARCHAR(20) NOT NULL CHECK (observed_severity IN ('minor', 'moderate', 'severe')),
    ai_response JSONB,  -- AI's best-guess response
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'reviewed')),
    reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_reports_user_id ON pest_reports(user_id);
```

#### Table: `alerts`
```sql
CREATE TABLE alerts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    alert_type VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    recommendations JSONB,  -- Array of recommendation strings
    severity VARCHAR(20) NOT NULL CHECK (severity IN ('low', 'medium', 'high')),
    source_data JSONB,  -- Weather conditions or detection data that triggered alert
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_alerts_user_id ON alerts(user_id);
CREATE INDEX idx_alerts_is_read ON alerts(is_read);
CREATE INDEX idx_alerts_created_at ON alerts(created_at DESC);
```

#### Table: `weather_cache`
```sql
CREATE TABLE weather_cache (
    id SERIAL PRIMARY KEY,
    location_key VARCHAR(50) NOT NULL UNIQUE,  -- "lat_lng" combined
    location_name VARCHAR(100) NOT NULL,
    current_conditions JSONB NOT NULL,
    forecast_data JSONB NOT NULL,
    ml_predictions JSONB,  -- Output from weather ML model
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_weather_cache_location ON weather_cache(location_key);
CREATE INDEX idx_weather_cache_fetched ON weather_cache(fetched_at);
```

#### Table: `pest_weather_correlations`
```sql
CREATE TABLE pest_weather_correlations (
    id SERIAL PRIMARY KEY,
    pest_name VARCHAR(100) NOT NULL,
    scientific_name VARCHAR(150),
    affected_crops JSONB NOT NULL,  -- ["rice", "vegetables"]
    risk_conditions JSONB NOT NULL,  -- {"temp_min": 25, "temp_max": 35, "humidity_min": 70}
    risk_level VARCHAR(20) NOT NULL CHECK (risk_level IN ('low', 'medium', 'high')),
    risk_message TEXT NOT NULL,
    prevention_tips JSONB NOT NULL,  -- Array of tip strings
    data_source VARCHAR(200),  -- "MARDI Guidelines", etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_correlations_crop ON pest_weather_correlations USING GIN (affected_crops);
```

### 7.3 Seed Data: Malaysian Locations

```sql
-- Location reference (can be stored in code or separate table)
-- Format: name, latitude, longitude

('Perlis', 6.4449, 100.2048),
('Kedah', 6.1184, 100.3685),
('Penang', 5.4164, 100.3327),
('Perak', 4.5921, 101.0901),
('Selangor', 3.0738, 101.5183),
('Negeri Sembilan', 2.7258, 101.9424),
('Melaka', 2.1896, 102.2501),
('Johor', 1.4854, 103.7618),
('Pahang', 3.8126, 103.3256),
('Terengganu', 5.3117, 103.1324),
('Kelantan', 6.1254, 102.2381),
('Sabah', 5.9788, 116.0753),
('Sarawak', 1.5533, 110.3592),
('Kuala Lumpur', 3.1390, 101.6869)
```

### 7.4 Seed Data: Pest-Weather Correlations (Rice)

```sql
INSERT INTO pest_weather_correlations (pest_name, scientific_name, affected_crops, risk_conditions, risk_level, risk_message, prevention_tips, data_source) VALUES

('Rice Stem Borer', 'Scirpophaga incertulas', '["rice"]',
 '{"temp_min": 25, "temp_max": 35, "humidity_min": 70, "trigger": "after_rain"}',
 'high',
 'Stem Borer activity increases in warm, humid conditions following rainfall. Moths lay eggs on leaves, larvae bore into stems.',
 '["Monitor rice stems for entry holes and frass", "Apply Trichogramma biological control", "Remove and destroy infected stems", "Avoid excessive nitrogen fertilizer"]',
 'MARDI Pest Management Guidelines'),

('Rice Leaf Folder', 'Cnaphalocrocis medinalis', '["rice"]',
 '{"temp_min": 25, "temp_max": 30, "humidity_min": 60, "humidity_max": 80, "condition": "cloudy"}',
 'medium',
 'Leaf Folder larvae fold leaves and feed inside. Common during cloudy, humid weather.',
 '["Scout for folded leaves with larvae inside", "Maintain field hygiene", "Avoid dense planting", "Apply neem-based spray if >10% damage"]',
 'MARDI Pest Management Guidelines'),

('Brown Planthopper', 'Nilaparvata lugens', '["rice"]',
 '{"humidity_min": 85, "temp_min": 25, "temp_max": 30}',
 'high',
 'Brown Planthopper thrives in high humidity with dense crop canopy. Can cause hopper burn.',
 '["Avoid excessive nitrogen application", "Maintain proper plant spacing", "Drain fields periodically", "Use resistant varieties if available"]',
 'IRRI Rice Knowledge Bank'),

('Rice Bug', 'Leptocorisa oratorius', '["rice"]',
 '{"humidity_max": 70, "trigger": "dry_period", "stage": "grain_filling"}',
 'medium',
 'Rice bugs attack during grain filling stage, especially in dry periods. Cause empty or discolored grains.',
 '["Monitor during flowering and grain filling", "Remove weeds around field", "Early morning collection when bugs are sluggish", "Apply insecticide if >5 bugs per hill"]',
 'Philippine Rice Research Institute'),

('Rice Blast', 'Magnaporthe oryzae', '["rice"]',
 '{"humidity_min": 90, "humidity_sustained_hours": 48, "temp_min": 24, "temp_max": 28}',
 'high',
 'Fungal disease favored by prolonged high humidity and moderate temperatures. Causes lesions on leaves and neck rot.',
 '["Use certified disease-free seeds", "Apply fungicide preventively in high-risk conditions", "Avoid excessive nitrogen", "Ensure good field drainage"]',
 'IRRI Rice Knowledge Bank'),

('Bacterial Leaf Blight', 'Xanthomonas oryzae', '["rice"]',
 '{"trigger": "after_heavy_rain", "humidity_min": 80, "condition": "flooding"}',
 'high',
 'Bacterial disease spreads rapidly after heavy rain and flooding. Causes yellowing leaf margins.',
 '["Avoid field flooding", "Ensure proper drainage", "Remove infected plant debris", "Use resistant varieties"]',
 'MARDI Pest Management Guidelines'),

('Sheath Blight', 'Rhizoctonia solani', '["rice"]',
 '{"humidity_min": 85, "temp_min": 28, "temp_max": 32}',
 'medium',
 'Fungal disease common in dense plantings with high humidity. Causes oval lesions on leaf sheaths.',
 '["Maintain proper plant spacing", "Avoid excessive nitrogen", "Remove crop residue after harvest", "Apply fungicide if lesions spread"]',
 'IRRI Rice Knowledge Bank'),

('Green Leafhopper', 'Nephotettix virescens', '["rice"]',
 '{"temp_min": 25, "temp_max": 32, "humidity_min": 70}',
 'medium',
 'Vector for tungro virus disease. Common in warm, humid conditions.',
 '["Monitor for hopper populations", "Remove infected plants immediately", "Synchronize planting in area", "Use resistant varieties"]',
 'Philippine Rice Research Institute');
```

---

## 8. API Specifications

### 8.1 Base URL
- **Development:** `http://localhost:8000/api/v1`
- **Production:** `https://your-server.com/api/v1`

### 8.2 Authentication Endpoints

#### POST `/auth/register`
Register new user with farm details.

**Request:**
```json
{
  "username": "ahmad_farmer",
  "password": "SecurePass123",
  "full_name": "Ahmad bin Ibrahim",
  "farm_location_name": "Kedah",
  "farm_location_lat": 6.1184,
  "farm_location_lng": 100.3685,
  "crop_type": "rice"
}
```

**Response (201):**
```json
{
  "message": "Registration successful",
  "user": {
    "id": 1,
    "username": "ahmad_farmer",
    "full_name": "Ahmad bin Ibrahim",
    "farm_location_name": "Kedah",
    "crop_type": "rice",
    "created_at": "2025-01-15T10:30:00Z"
  },
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 604800
}
```

#### POST `/auth/login`
Authenticate and receive JWT token.

**Request:**
```json
{
  "username": "ahmad_farmer",
  "password": "SecurePass123"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 604800,
  "user": {
    "id": 1,
    "username": "ahmad_farmer",
    "full_name": "Ahmad bin Ibrahim",
    "farm_location_name": "Kedah",
    "crop_type": "rice"
  }
}
```

#### GET `/auth/me`
Get current user profile.

**Response (200):**
```json
{
  "id": 1,
  "username": "ahmad_farmer",
  "full_name": "Ahmad bin Ibrahim",
  "farm_location_name": "Kedah",
  "farm_location_lat": 6.1184,
  "farm_location_lng": 100.3685,
  "crop_type": "rice",
  "created_at": "2025-01-15T10:30:00Z"
}
```

---

### 8.3 Weather Endpoints

#### GET `/weather/current`
Get current weather for user's location.

**Response (200):**
```json
{
  "location": "Kedah",
  "temperature": 31.5,
  "humidity": 78,
  "condition": "Partly Cloudy",
  "condition_icon": "partly_cloudy",
  "wind_speed": 12.5,
  "precipitation": 0,
  "fetched_at": "2025-01-15T14:30:00Z",
  "ml_prediction": {
    "trend": "stable",
    "anomaly_detected": false,
    "confidence": 0.85
  }
}
```

#### GET `/weather/forecast`
Get 7-day forecast with ML predictions.

**Response (200):**
```json
{
  "location": "Kedah",
  "forecast": [
    {
      "date": "2025-01-16",
      "day_name": "Thursday",
      "temp_high": 33,
      "temp_low": 25,
      "condition": "Thunderstorms",
      "condition_icon": "thunderstorm",
      "precipitation_probability": 80,
      "precipitation_mm": 45,
      "humidity": 85
    }
  ],
  "ml_predictions": {
    "heavy_rain_probability": 0.75,
    "anomaly_alert": "Elevated rainfall expected",
    "confidence": 0.82
  }
}
```

#### GET `/weather/history`
Get historical weather data.

**Query Parameters:**
- `days` (optional, default: 7, max: 30)

**Response (200):**
```json
{
  "location": "Kedah",
  "period": "7 days",
  "data": [
    {
      "date": "2025-01-14",
      "temp_avg": 29.5,
      "humidity_avg": 75,
      "precipitation_total": 12.5,
      "condition_summary": "Mostly sunny with afternoon showers"
    }
  ]
}
```

---

### 8.4 Pest Detection Endpoints

#### POST `/pests/detect`
Upload image for pest detection.

**Request:** `multipart/form-data`
- `image`: File (JPEG/PNG, max 5MB)
- `retry_count`: Integer (0-2)

**Response (200) - Successful Detection:**
```json
{
  "status": "detected",
  "detection_id": 42,
  "pest_name": "Rice Stem Borer",
  "confidence": 87.5,
  "danger_level": "high",
  "description": "The Rice Stem Borer is a major pest...",
  "recommendations": [
    "Immediately inspect surrounding plants for signs of infestation",
    "Remove and destroy affected stems",
    "Apply Trichogramma biological control agents",
    "Consider targeted insecticide if infestation is severe"
  ],
  "image_url": "/uploads/detections/42.jpg",
  "detected_at": "2025-01-15T14:22:00Z",
  "alert_generated": true
}
```

**Response (200) - Partial Match:**
```json
{
  "status": "partial",
  "possible_pest": "Rice Leaf Folder",
  "confidence": 58.3,
  "message": "Detection confidence is low. Please try again with a clearer image.",
  "tips": [
    "Ensure good lighting",
    "Focus camera directly on the pest",
    "Get closer to the subject"
  ],
  "retry_count": 1,
  "can_retry": true
}
```

**Response (200) - Unknown (After 3 retries):**
```json
{
  "status": "unknown",
  "message": "Unable to identify this pest after multiple attempts.",
  "retry_count": 3,
  "can_retry": false,
  "offer_report": true,
  "report_url": "/pests/report"
}
```

#### POST `/pests/report`
Submit manual pest report.

**Request:**
```json
{
  "image_url": "/uploads/temp/abc123.jpg",
  "description": "Small green insects on rice leaves",
  "observed_severity": "moderate"
}
```

**Response (201):**
```json
{
  "report_id": 15,
  "status": "submitted",
  "ai_response": {
    "possible_identification": "Based on description, this could be Green Leafhopper or Rice Aphids",
    "general_advice": [
      "Monitor the affected area daily",
      "Remove heavily infested leaves",
      "Consider applying neem oil spray",
      "Consult local agricultural extension office for confirmation"
    ],
    "when_to_seek_help": "If infestation spreads to more than 20% of plants"
  },
  "reported_at": "2025-01-15T14:35:00Z"
}
```

#### GET `/pests/history`
Get user's detection history.

**Query Parameters:**
- `page` (default: 1)
- `limit` (default: 20, max: 100)

**Response (200):**
```json
{
  "total": 45,
  "page": 1,
  "limit": 20,
  "detections": [
    {
      "id": 42,
      "pest_name": "Rice Stem Borer",
      "confidence": 87.5,
      "danger_level": "high",
      "image_url": "/uploads/detections/42.jpg",
      "detected_at": "2025-01-15T14:22:00Z"
    }
  ]
}
```

---

### 8.5 Pest Risk Endpoints

#### GET `/pests/risk`
Get current pest risk assessment based on weather.

**Response (200):**
```json
{
  "assessment_time": "2025-01-15T14:30:00Z",
  "weather_summary": {
    "temperature": 28,
    "humidity": 85,
    "recent_rainfall": true
  },
  "risks": [
    {
      "pest_name": "Rice Stem Borer",
      "risk_level": "high",
      "risk_factors": [
        "High humidity (85%)",
        "Optimal temperature (28°C)",
        "Recent rainfall detected"
      ],
      "message": "Stem Borer activity increases in warm, humid conditions following rainfall.",
      "prevention_tips": [
        "Monitor rice stems for entry holes",
        "Apply Trichogramma biological control",
        "Avoid excessive nitrogen fertilizer"
      ]
    }
  ],
  "overall_risk": "elevated"
}
```

---

### 8.6 Alert Endpoints

#### GET `/alerts`
Get user's alerts.

**Query Parameters:**
- `unread_only` (boolean, default: false)
- `limit` (default: 50)

**Response (200):**
```json
{
  "unread_count": 3,
  "alerts": [
    {
      "id": 15,
      "alert_type": "pest_risk_warning",
      "title": "Elevated Rice Stem Borer Risk",
      "message": "Weather conditions favor pest activity in the next 3-5 days.",
      "severity": "high",
      "recommendations": [
        "Increase field monitoring",
        "Check stems for entry holes",
        "Prepare preventive measures"
      ],
      "is_read": false,
      "created_at": "2025-01-15T14:00:00Z"
    }
  ]
}
```

#### PUT `/alerts/{alert_id}/read`
Mark alert as read.

**Response (200):**
```json
{
  "message": "Alert marked as read",
  "alert_id": 15
}
```

---

### 8.7 Chat Endpoints

#### POST `/chat/message`
Send message to AI chatbot.

**Request:**
```json
{
  "message": "Why are my rice leaves turning yellow?",
  "session_id": "optional-session-uuid"
}
```

**Response (200):**
```json
{
  "response": "Yellow leaves in rice can have several causes...",
  "session_id": "uuid-for-conversation",
  "context_used": {
    "location": "Kedah",
    "crop": "rice",
    "current_weather": "Hot and humid"
  }
}
```

#### POST `/chat/image`
Upload image in chat for analysis.

**Request:** `multipart/form-data`
- `image`: File (JPEG/PNG, max 5MB)
- `message`: String (optional context)
- `session_id`: String (optional)

**Response (200):**
```json
{
  "response": "I've analyzed the image. This appears to be Rice Leaf Folder damage...",
  "detection_result": {
    "pest_name": "Rice Leaf Folder",
    "confidence": 78.5,
    "danger_level": "medium"
  },
  "session_id": "uuid-for-conversation"
}
```

---

### 8.8 Dashboard Endpoint

#### GET `/dashboard`
Get aggregated dashboard data.

**Response (200):**
```json
{
  "weather": {
    "temperature": 31.5,
    "humidity": 78,
    "condition": "Partly Cloudy",
    "condition_icon": "partly_cloudy"
  },
  "alerts": {
    "unread_count": 3,
    "recent": [
      {
        "id": 15,
        "title": "Elevated Pest Risk",
        "severity": "high",
        "created_at": "2025-01-15T14:00:00Z"
      }
    ]
  },
  "recent_detections": [
    {
      "id": 42,
      "pest_name": "Rice Stem Borer",
      "confidence": 87.5,
      "detected_at": "2025-01-15T14:22:00Z"
    }
  ],
  "pest_risk_status": "elevated",
  "last_updated": "2025-01-15T14:30:00Z"
}
```

---

## 9. Mobile App Screens

### 9.1 Screen Flow

```
Splash Screen
    │
    ▼
┌─────────────┐     ┌─────────────┐
│   Login     │◄───►│  Register   │
└──────┬──────┘     └─────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│           Dashboard (Home)           │
│  - Weather Card                      │
│  - Alert Banner                      │
│  - Quick Actions                     │
│  - Recent Activity                   │
└──┬─────────┬─────────┬─────────┬────┘
   │         │         │         │
   ▼         ▼         ▼         ▼
┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐
│Detect│ │Weather│ │Alerts│ │ Chat │
│ Pest │ │Detail │ │ List │ │      │
└──┬───┘ └──────┘ └──┬───┘ └──────┘
   │                 │
   ▼                 ▼
┌──────┐         ┌──────┐
│Result│         │Alert │
│Screen│         │Detail│
└──────┘         └──────┘
```

### 9.2 Screen Specifications

#### Screen 1: Login
- Username input
- Password input (obscured)
- "Login" button
- "Create Account" link
- Error message display

#### Screen 2: Register
- Username input
- Password input
- Full name input
- Farm location dropdown (Malaysian states)
- Crop type dropdown
- "Register" button
- "Already have account?" link

#### Screen 3: Dashboard
- **Weather Card:** Temperature, condition, humidity, icon
- **Alert Banner:** Unread count, tap to view alerts
- **Recent Alerts:** Top 3 alerts, severity badges
- **Quick Actions:** "Detect Pest" button, "Chat" button
- **Recent Detections:** Last 3, with thumbnails
- Pull-to-refresh

#### Screen 4: Weather Detail
- Current conditions (expanded)
- 7-day forecast cards
- ML prediction insights
- Historical trends button

#### Screen 5: Pest Detection
- Camera/gallery picker
- Image preview
- "Analyze" button
- Loading indicator
- Retry guidance (if needed)

#### Screen 6: Detection Result
- Image displayed
- Pest name (large)
- Confidence bar
- Danger level badge
- AI recommendations list
- "Detect Another" button
- "View History" button

#### Screen 7: Alerts List
- Tabs: All / Unread
- Alert cards with:
  - Icon by type
  - Title
  - Severity badge
  - Time ago
  - Read/unread indicator
- Tap to view detail

#### Screen 8: Alert Detail
- Alert title
- Full message
- Severity indicator
- Recommendations list
- "Mark as Read" button
- Source data (what triggered it)

#### Screen 9: Chat
- Message list (conversation)
- Text input
- Image upload button
- Send button
- Loading indicator for AI response

#### Screen 10: Detection History
- List of past detections
- Thumbnail, pest name, confidence, date
- Tap for detail view
- Pagination/infinite scroll

---

## 10. Non-Functional Requirements

### 10.1 Performance
| Metric | Target |
|--------|--------|
| API Response Time | < 2 seconds (excluding ML) |
| ML Inference Time | < 5 seconds |
| AI Chat Response | < 3 seconds |
| App Launch Time | < 3 seconds |
| Dashboard Load | < 2 seconds |
| Image Upload | Support up to 5MB |

### 10.2 Scalability
| Metric | Target |
|--------|--------|
| Concurrent Users | 20 (demo scenario) |
| Database Records | 10,000 detections |
| API Rate Limit | 100 requests/minute/user |

### 10.3 Security
- JWT tokens with 7-day expiry
- bcrypt password hashing (cost 12)
- HTTPS for all API communication
- Input validation and sanitization
- File type validation for uploads

### 10.4 Reliability
- 95% uptime during demo period
- Graceful error handling
- Fallback for external API failures
- Daily database backups

### 10.5 Compatibility
- Android 10+ (API 29+)
- iOS 13+
- Screen sizes: 4.5" to 7"

---

## 11. Constraints & Assumptions

### 11.1 Constraints
- **Budget:** RM 0 (free tier services only)
- **Timeline:** 14 weeks
- **Team:** Small team with divided responsibilities
- **Hardware:** No physical IoT sensors
- **Data:** Simulated via weather API

### 11.2 Assumptions
- Users have smartphone with camera
- Users have internet connection (3G minimum)
- ML models will be delivered by team
- OpenWeatherMap free tier sufficient (1000 calls/day)
- OpenRouter free tier sufficient for AI calls
- Users comfortable with English interface

### 11.3 Dependencies
- OpenWeatherMap API
- OpenRouter API
- Team-built ML models (weather + pest)
- Self-hosted server availability

---

## 12. Timeline & Milestones

### Phase 1: Foundation (Weeks 1-4)
- Environment setup
- Database schema implementation
- Authentication system
- Basic API structure

### Phase 2: Core Features (Weeks 5-9)
- Weather integration + ML model
- Pest detection + ML model
- Pest risk correlation engine
- Alert system

### Phase 3: AI Integration (Weeks 10-11)
- OpenRouter integration
- Chatbot implementation
- Recommendation generation

### Phase 4: Mobile App (Weeks 9-13)
- React Native setup
- All screens implementation
- API integration
- Testing

### Phase 5: Polish & Deploy (Weeks 13-14)
- Bug fixes
- Performance optimization
- Deployment
- Demo preparation

---

## 13. Risk Management

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| ML models delayed | Medium | High | Start with mock responses, integrate real models when ready |
| API rate limits hit | Low | Medium | Implement caching, monitor usage |
| AI API costs | Low | Medium | Use free tier, implement rate limiting |
| Server downtime | Low | High | Render.com backup, local demo fallback |
| Scope creep | High | Medium | Strict adherence to this PRD |

---

## 14. Acceptance Criteria

### 14.1 Demo Checklist
- [ ] User can register with farm details
- [ ] User can login successfully
- [ ] Dashboard displays weather and alerts
- [ ] Weather forecast shows 7-day data
- [ ] Weather alerts generated for thresholds
- [ ] Pest image upload works
- [ ] Pest detection returns results
- [ ] AI recommendations displayed
- [ ] Pest risk alerts generated from correlations
- [ ] Chatbot responds to queries
- [ ] Alert list shows all alerts
- [ ] Mark as read works
- [ ] Detection history accessible
- [ ] No crashes during 5-minute demo

### 14.2 Success Definition
The project is successful if:
1. Both core features (weather + pest) work end-to-end
2. Early warnings are generated before problems occur
3. AI provides relevant, actionable recommendations
4. Demo completes without critical failures
5. Documentation is complete

---

## Appendix A: Error Codes

| Code | Message |
|------|---------|
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Invalid credentials/token |
| 404 | Not Found |
| 413 | Payload Too Large - Image > 5MB |
| 422 | Validation Error |
| 429 | Rate Limit Exceeded |
| 500 | Internal Server Error |
| 503 | Service Unavailable - External API down |

---

## Appendix B: Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/agrisense

# JWT
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRY_DAYS=7

# OpenWeatherMap
OPENWEATHER_API_KEY=your-api-key
OPENWEATHER_BASE_URL=https://api.openweathermap.org/data/2.5

# OpenRouter (AI)
OPENROUTER_API_KEY=your-api-key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1

# ML Service (separate microservice on port 8001)
ML_SERVICE_URL=http://ml-service:8001
ML_SERVICE_TIMEOUT=10
ML_WEATHER_ENDPOINT=/predict/weather
ML_PEST_ENDPOINT=/predict/pest

# Storage
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE_MB=5

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=False
```

---

**End of PRD v2.0**