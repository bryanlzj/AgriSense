# PRD Updates: Dual Core Features (Weather + Pest)

**Date:** January 2025  
**Reason:** Corrected project scope to properly reflect DUAL CORE FEATURES with equal priority

---

## 🎯 **Key Changes Made**

### **1. Executive Summary**
**Before:**
- "Primary Feature: AI-powered pest detection"
- "Supporting Features: Weather forecasting"

**After:**
- **DUAL CORE FEATURES (Equal Priority):**
  - 🌤️ Weather Early Warning System
  - 🐛 Pest Risk Management System

---

### **2. Problem Statement**
**Before:**
- Generic list of farmer pain points

**After:**
- **Two Critical Challenges:**
  1. **Unpredictable Weather Patterns** (sudden storms, heavy rains, extreme temperatures)
  2. **Pest and Disease Outbreaks** (lack of early detection, rapid spread)

---

### **3. Solution Description**
**Before:**
- Focused on pest detection with weather as secondary

**After:**
- **Dual-Purpose Early Warning System:**
  - 🌤️ Weather Early Warning (forecasts, alerts, recommendations)
  - 🐛 Pest Risk Management (AI detection, environmental monitoring)
  - 📱 Mobile-First Platform (unified alerts, real-time updates)

---

### **4. User Persona (Ahmad the Farmer)**
**Before:**
- Generic pain points

**After:**
- **Weather-related pain points:** Sudden storms damage crops without warning
- **Pest-related pain points:** Cannot identify pests accurately
- **Primary Goal 1:** Receive early warnings for weather threats
- **Primary Goal 2:** Detect pests early

---

### **5. User Stories**
**Before:**
- 4 Epics (Auth, Pest Detection, Environmental Monitoring, Alerts)

**After:**
- 5 Epics with **Weather and Pest as separate CORE FEATURES:**
  - Epic 1: User Authentication
  - **Epic 2: Weather Early Warning System (CORE FEATURE)**
  - **Epic 3: Pest Risk Management System (CORE FEATURE)**
  - Epic 4: Environmental Monitoring Dashboard
  - Epic 5: Unified Alert System

**New User Stories Added:**
- US-2.1: 7-day weather forecast for planning
- US-2.2: Heavy rain warnings
- US-2.3: Extreme heat alerts
- US-2.4: Current weather conditions
- US-2.5: Historical weather data

---

### **6. Feature Requirements (Reordered)**

**Before:**
- 5.1 User Authentication
- 5.2 Pest Detection ← Listed first (implied primary)
- 5.3 Environmental Monitoring
- 5.4 Alert System
- 5.5 Weather Forecast ← Listed last (implied secondary)

**After:**
- 5.1 User Authentication (Simplified)
- **5.2 Weather Early Warning System (CORE FEATURE #1)** ← NEW, comprehensive
- **5.3 Pest Risk Management System (CORE FEATURE #2)** ← Enhanced
- 5.4 Environmental Monitoring Dashboard
- 5.5 Unified Alert System
- ~~5.6 Weather Forecast~~ ← Removed (merged into 5.2)

---

### **7. Feature 5.2: Weather Early Warning System (NEW)**

**Comprehensive weather feature including:**

**Functional Requirements:**
- FR-2.1 to FR-2.8: OpenWeatherMap integration, 7-day forecasts, caching, alerts

**Weather Data Points:**
- Current temperature, humidity, weather condition
- 7-day forecast (high/low, precipitation, icons)
- Wind speed, sunrise/sunset

**Weather Alert Triggers:**
| Alert Type | Trigger | Priority | Recommendation |
|-----------|---------|----------|----------------|
| Heavy Rain Warning | > 50mm | High | Cover crops, prepare drainage |
| Extreme Heat Alert | > 35°C | Medium | Increase irrigation |
| Storm Warning | Wind > 40 km/h | High | Secure equipment |
| Low Temperature | < 15°C | Low | Protect sensitive crops |

**Acceptance Criteria:**
- ✅ 7-day forecast displays correctly
- ✅ Weather alerts within 1 minute
- ✅ Actionable recommendations
- ✅ Handles API failures gracefully

---

### **8. Feature 5.3: Pest Risk Management (Enhanced)**

**Before:**
- Basic pest detection only

**After:**
- FR-3.7: Correlate pest detections with environmental conditions
- FR-3.8: Generate pest risk alerts (confidence > 80%)
- Enhanced description: "AI-powered pest identification with environmental risk assessment"

---

### **9. Feature 5.5: Unified Alert System (Enhanced)**

**Before:**
- Generic alert system

**After:**
- **Emphasis on BOTH weather AND pest alerts**
- FR-5.1: Weather alerts (rain, heat, wind)
- FR-5.2: Pest risk alerts
- FR-5.3: Environmental alerts (soil moisture)
- FR-5.6: Alert prioritization (High/Medium/Low)

**Alert Types Table Updated:**
| Type | Source | Priority |
|------|--------|----------|
| Heavy Rain Warning | Weather API | High |
| Storm Warning | Weather API | High |
| Extreme Heat Alert | Weather API | Medium |
| Pest Risk Alert | ML Detection | High |
| Low Soil Moisture | Sensor Data | Low |
| Low Temperature | Weather API | Low |

---

### **10. Success Metrics (Updated)**

**New Metrics Added:**
- **Weather Forecast Accuracy:** 7-day forecast displayed correctly
- **Weather Alert Timeliness:** Alerts within 1 minute of trigger
- **Pest Detection Accuracy:** > 70% confidence for known pests
- **Sensor Data Refresh Rate:** Every 30 seconds
- **Demo Readiness:** 5-minute demo showcasing **BOTH features**

---

### **11. Project Goals (Updated)**

**Before:**
1. Deliver working pest detection workflow

**After:**
1. Deliver working workflows for **BOTH weather early warning AND pest risk management**
2. Demonstrate full-stack integration (mobile + backend + **ML + external APIs**)
3. Gain experience with **IoT simulation**
4. **Create practical tool addressing real farmer pain points (weather + pest risks)**

---

## 📊 **Feature Priority Clarification**

### **TIER 1: DUAL CORE FEATURES (Equal Weight)**
1. **🌤️ Weather Early Warning System**
   - 7-day forecasts
   - Weather anomaly alerts
   - Weather-based recommendations
   - Historical weather data

2. **🐛 Pest Risk Management System**
   - AI-powered pest detection
   - Environmental monitoring
   - Pest risk alerts
   - Detection history

### **TIER 2: Supporting Infrastructure**
3. Environmental Monitoring Dashboard (displays weather + pest data)
4. Unified Alert System (combines weather + pest alerts)
5. User Authentication (access control)

---

## ✅ **What This Means for Development**

### **Time Allocation (14 weeks):**
- **Week 1-2:** Setup + Database + Auth
- **Week 3-4:** Weather Early Warning System (OpenWeatherMap integration, alerts)
- **Week 5-6:** Pest Risk Management System (ML integration, detection)
- **Week 7-8:** Environmental Monitoring Dashboard (sensor data, visualization)
- **Week 9-10:** Unified Alert System (combine weather + pest alerts)
- **Week 11-12:** Mobile App (Flutter UI for all features)
- **Week 13-14:** Integration, Testing, Deployment

### **Demo Narrative:**
1. **Show Weather Early Warning:** "Farmer checks 7-day forecast, receives heavy rain alert"
2. **Show Pest Risk Management:** "Farmer uploads pest photo, gets identification + risk alert"
3. **Show Unified Dashboard:** "All data (weather + pests + sensors) in one place"
4. **Show Alert System:** "Farmer receives timely warnings for BOTH weather AND pest threats"

---

## 🎯 **Success Criteria**

**For Weather Early Warning System:**
- ✅ 7-day forecast displays correctly
- ✅ Weather alerts generated for heavy rain, storms, extreme heat
- ✅ Recommendations are actionable (e.g., "Cover crops, prepare drainage")
- ✅ Handles OpenWeatherMap API failures gracefully

**For Pest Risk Management System:**
- ✅ Pest detection works (upload image → get result)
- ✅ Confidence score > 70% for known pests
- ✅ Pest risk alerts generated (confidence > 80%)
- ✅ Detection history saved and viewable

**For Unified System:**
- ✅ Dashboard shows BOTH weather AND pest data
- ✅ Alert system combines weather + pest warnings
- ✅ Mobile app provides seamless experience for BOTH features

---

## 📝 **Justification for Lecturers**

**Why This Project Has Dual Core Features:**

1. **Real-World Problem:** Malaysian farmers face BOTH weather unpredictability AND pest outbreaks
2. **Comprehensive Solution:** Addressing one without the other is incomplete
3. **Technical Complexity:** Demonstrates integration of:
   - External APIs (OpenWeatherMap)
   - Machine Learning (pest detection)
   - IoT simulation (sensor data)
   - Mobile development (Flutter)
   - Backend development (FastAPI)
4. **Academic Value:** Shows full-stack capability across multiple domains
5. **Practical Impact:** Farmers need BOTH weather warnings AND pest alerts to protect crops

---

## 🚀 **Next Steps**

1. ✅ PRD updated to reflect dual core features
2. ⏳ Task list needs updating to reflect equal priority
3. ⏳ Development should allocate equal time to weather + pest features
4. ⏳ Demo should showcase BOTH features prominently

---

**Document Owner:** Integration Lead  
**Last Updated:** January 2025  
**Status:** PRD Updated ✅ | Task List Pending ⏳
