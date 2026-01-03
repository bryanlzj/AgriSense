# Task List Updates: Dual Core Features

**Date:** January 2025  
**Reason:** Updated task list to reflect DUAL CORE FEATURES (Weather + Pest) with equal priority

---

## ✅ **Changes Made to Task List**

### **1. Header Updated**
**Before:**
```
Project: AgriSense - IoT Agricultural Monitoring System
```

**After:**
```
Project: AgriSense - IoT-Driven Early Warning System for Weather and Pest Risk Management

🎯 DUAL CORE FEATURES (Equal Priority):
1. 🌤️ Weather Early Warning System - Real-time forecasts, weather alerts, recommendations
2. 🐛 Pest Risk Management System - AI-powered pest detection, environmental monitoring
```

---

### **2. Task 1.7: Weather API Integration → Weather Early Warning System**

**Before:**
```
### Task 1.7: Weather API Integration
**Goal:** Integrate OpenWeatherMap API for weather forecasts
**Estimated Time:** 3 hours
```

**After:**
```
### Task 1.7: Weather Early Warning System (CORE FEATURE #1) 🌤️
**Goal:** Integrate OpenWeatherMap API for weather forecasts, alerts, and recommendations
**Estimated Time:** 4 hours
⚠️ CRITICAL: This is a CORE FEATURE with equal priority to Pest Detection
```

**Why:** Emphasizes that weather is NOT a supporting feature, but a PRIMARY feature

---

### **3. Task 1.4: Pest Detection → Pest Risk Management System**

**Before:**
```
### Task 1.4: Pest Detection API - Image Upload
**Goal:** Implement image upload and storage
**Estimated Time:** 3 hours
```

**After:**
```
### Task 1.4: Pest Risk Management System - Image Upload (CORE FEATURE #2) 🐛
**Goal:** Implement image upload and storage for pest detection
**Estimated Time:** 3 hours
⚠️ CRITICAL: This is a CORE FEATURE with equal priority to Weather Early Warning
```

**Why:** Makes it clear that pest detection is CORE FEATURE #2, not the only core feature

---

### **4. Task 1.8.2: Weather-Based Alerts Enhanced**

**Before:**
```
- [ ] 1.8.2: Implement weather-based alerts
  - Check for rain forecast (>70% chance = rain alert)
  - Check for extreme temperatures
  - Check for storms or severe weather
```

**After:**
```
- [ ] 1.8.2: Implement weather-based alerts (CORE FEATURE)
  - Check for heavy rain forecast (>50mm = high priority alert)
  - Check for extreme heat (>35°C = medium priority alert)
  - Check for storms (wind >40 km/h = high priority alert)
  - Check for low temperature (<15°C = low priority alert)
  - Generate actionable recommendations (e.g., "Cover crops, prepare drainage")
```

**Why:** 
- Aligns with PRD specifications
- Adds specific thresholds from PRD
- Includes actionable recommendations
- Emphasizes it's a CORE FEATURE

---

## 📊 **Task Priority Clarification**

### **TIER 1: CORE FEATURES (Must Complete for MVP)**

**Backend Tasks:**
- ✅ Task 1.7: Weather Early Warning System (CORE FEATURE #1) 🌤️
  - OpenWeatherMap API integration
  - 7-day forecast endpoint
  - Current weather endpoint
  - Weather caching (30 min)
  - Weather-based alert generation

- ✅ Task 1.4-1.6: Pest Risk Management System (CORE FEATURE #2) 🐛
  - Image upload and validation
  - Mock ML service
  - Pest detection endpoint
  - Detection history
  - Pest risk alert generation

**Mobile Tasks:**
- ✅ Weather screens (forecast, current weather, weather alerts)
- ✅ Pest detection screens (camera, upload, results, history)

### **TIER 2: Supporting Features**

- Task 1.3: Sensor Data API (supports both weather and pest risk assessment)
- Task 1.8-1.9: Unified Alert System (combines weather + pest alerts)
- Task 1.1-1.2: Authentication (access control)

---

## 🎯 **Development Timeline Emphasis**

### **Week 3-4: Weather Early Warning System (CORE #1)**
- Set up OpenWeatherMap API
- Implement weather service with caching
- Create weather endpoints (current + forecast)
- Implement weather-based alert generation
- Test weather API integration

**Success Criteria:**
- ✅ 7-day forecast displays correctly
- ✅ Weather alerts generated for heavy rain, storms, extreme heat
- ✅ Recommendations are actionable
- ✅ API failures handled gracefully

### **Week 5-6: Pest Risk Management System (CORE #2)**
- Implement image upload and validation
- Create mock ML service
- Implement pest detection endpoint
- Store detections in database
- Implement pest risk alert generation

**Success Criteria:**
- ✅ Image upload works (camera + gallery)
- ✅ Detection completes within 5 seconds
- ✅ Results display pest name and confidence
- ✅ Pest risk alerts generated (confidence > 80%)

### **Week 7-8: Supporting Features**
- Sensor data API
- Unified alert system
- Backend testing and documentation

### **Week 9-12: Mobile App**
- Weather screens (Week 9)
- Pest detection screens (Week 10)
- Dashboard and alerts (Week 11)
- Polish and testing (Week 12)

---

## 📝 **Demo Narrative (Updated)**

### **5-Minute Demo Flow:**

**1. Weather Early Warning (2 minutes) - CORE FEATURE #1**
- Open app → Dashboard shows current weather
- Navigate to Weather Forecast → Show 7-day forecast
- Demonstrate weather alert: "Heavy rain warning - Cover crops, prepare drainage"
- Show weather-based recommendation

**2. Pest Risk Management (2 minutes) - CORE FEATURE #2**
- Navigate to Pest Detection
- Upload pest image (or take photo)
- Show AI detection result with confidence score
- Show pest risk alert: "High pest risk detected - Apply treatment immediately"
- View detection history

**3. Unified Dashboard (1 minute) - Integration**
- Show dashboard with BOTH weather AND pest data
- Show unified alert list (weather + pest alerts combined)
- Demonstrate real-time data updates (30-second refresh)

**Key Message:** "AgriSense provides farmers with DUAL protection: early warnings for BOTH weather threats AND pest outbreaks"

---

## ✅ **Task List Status**

**Total Tasks:** 87 subtasks  
**Completed:** 3/87 (3%)  
**Current Phase:** Phase 0 - Setup & Planning

**CORE FEATURE Tasks:**
- [ ] Task 1.7: Weather Early Warning System (0/6 subtasks)
- [ ] Task 1.4-1.6: Pest Risk Management System (0/12 subtasks)

**Next Steps:**
1. Complete Phase 0 setup tasks (0.2-0.4)
2. Implement authentication (Task 1.1-1.2)
3. **Implement Weather Early Warning System (Task 1.7)** ← CORE FEATURE #1
4. **Implement Pest Risk Management System (Task 1.4-1.6)** ← CORE FEATURE #2
5. Implement supporting features (sensors, alerts)
6. Build mobile app with BOTH core features

---

## 🚀 **Success Criteria for Lecturers**

**To demonstrate project completeness, BOTH core features must work:**

### **Weather Early Warning System:**
- ✅ 7-day forecast displays correctly with icons
- ✅ Current weather updates every 30 minutes
- ✅ Weather alerts generated within 1 minute
- ✅ Recommendations are actionable and relevant
- ✅ Handles API failures gracefully

### **Pest Risk Management System:**
- ✅ Pest detection works (upload → result)
- ✅ Detection completes within 5 seconds
- ✅ Confidence score displayed
- ✅ Pest risk alerts generated (confidence > 80%)
- ✅ Detection history saved and viewable

### **Unified System:**
- ✅ Dashboard shows BOTH weather AND pest data
- ✅ Alert system combines weather + pest warnings
- ✅ Mobile app provides seamless experience

---

**Document Owner:** Integration Lead  
**Last Updated:** January 2025  
**Status:** Task List Updated ✅
