# AgriSense API Documentation

## Overview

AgriSense is a smart agriculture monitoring system with two core features:
1. **Weather Early Warning System** - Real-time weather monitoring and forecasts
2. **Pest Risk Management** - AI-powered pest detection from images

Base URL: `http://localhost:5000/api/v1`

## Authentication

All endpoints (except registration and login) require JWT authentication.

### Headers
```
Authorization: Bearer <jwt_token>
```

---

## 1. Authentication Endpoints

### 1.1 Register User
**POST** `/auth/register`

Register a new user account.

**Request Body:**
```json
{
  "username": "farmer123",
  "password": "securepassword",
  "full_name": "John Farmer"
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "username": "farmer123",
  "full_name": "John Farmer",
  "created_at": "2025-01-04T10:00:00"
}
```

**Errors:**
- `400` - Username already exists
- `422` - Validation error

---

### 1.2 Login
**POST** `/auth/login`

Login and receive JWT token.

**Request Body:**
```json
{
  "username": "farmer123",
  "password": "securepassword"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Errors:**
- `401` - Invalid credentials

---

### 1.3 Get Current User
**GET** `/auth/me`

Get current authenticated user information.

**Response:** `200 OK`
```json
{
  "id": 1,
  "username": "farmer123",
  "full_name": "John Farmer",
  "created_at": "2025-01-04T10:00:00"
}
```

**Errors:**
- `401` - Not authenticated

---

## 2. Sensor Data Endpoints

### 2.1 Create Sensor Data
**POST** `/sensor/`

Record new sensor data reading.

**Request Body:**
```json
{
  "temperature": 28.5,
  "humidity": 65.0,
  "soil_moisture": 45.0,
  "rainfall": 5.2
}
```

**Validation:**
- `temperature`: -50 to 60°C
- `humidity`: 0 to 100%
- `soil_moisture`: 0 to 100%
- `rainfall`: >= 0 mm

**Response:** `200 OK`
```json
{
  "id": 1,
  "user_id": 1,
  "temperature": 28.5,
  "humidity": 65.0,
  "soil_moisture": 45.0,
  "rainfall": 5.2,
  "created_at": "2025-01-04T10:00:00"
}
```

---

### 2.2 List Sensor Data
**GET** `/sensor/`

Get list of sensor data with optional filtering.

**Query Parameters:**
- `skip` (int): Pagination offset (default: 0)
- `limit` (int): Max results (default: 100)
- `start_date` (datetime): Filter from date
- `end_date` (datetime): Filter to date
- `min_temp` (float): Minimum temperature
- `max_temp` (float): Maximum temperature

**Example:**
```
GET /sensor/?skip=0&limit=10&min_temp=20&max_temp=30
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "temperature": 28.5,
    "humidity": 65.0,
    "soil_moisture": 45.0,
    "rainfall": 5.2,
    "created_at": "2025-01-04T10:00:00"
  }
]
```

---

### 2.3 Get Sensor Data
**GET** `/sensor/{id}`

Get specific sensor data reading.

**Response:** `200 OK`
```json
{
  "id": 1,
  "temperature": 28.5,
  "humidity": 65.0,
  "soil_moisture": 45.0,
  "rainfall": 5.2,
  "created_at": "2025-01-04T10:00:00"
}
```

**Errors:**
- `404` - Sensor data not found

---

### 2.4 Update Sensor Data
**PUT** `/sensor/{id}`

Update existing sensor data.

**Request Body:**
```json
{
  "temperature": 30.0,
  "humidity": 70.0,
  "soil_moisture": 50.0,
  "rainfall": 10.0
}
```

**Response:** `200 OK` (same as create)

---

### 2.5 Delete Sensor Data
**DELETE** `/sensor/{id}`

Delete sensor data reading.

**Response:** `200 OK`
```json
{
  "message": "Sensor data deleted successfully"
}
```

---

### 2.6 Get Statistics
**GET** `/sensor/stats/summary`

Get statistical summary of sensor data.

**Response:** `200 OK`
```json
{
  "avg_temperature": 27.5,
  "min_temperature": 20.0,
  "max_temperature": 35.0,
  "avg_humidity": 65.0,
  "avg_soil_moisture": 45.0,
  "total_rainfall": 125.5,
  "data_count": 100
}
```

---

## 3. Pest Detection Endpoints (CORE FEATURE #2)

### 3.1 Upload Image Only
**POST** `/pest/upload`

Upload pest image without detection.

**Request:**
- Content-Type: `multipart/form-data`
- Field: `file` (image file)

**Supported Formats:** JPEG, PNG  
**Max Size:** 5MB  
**Min Dimensions:** 224x224 pixels

**Response:** `200 OK`
```json
{
  "filename": "abc123-def456.jpg",
  "url": "/uploads/abc123-def456.jpg"
}
```

---

### 3.2 Upload and Detect
**POST** `/pest/detect`

Upload image and run pest detection (mock ML).

**Request:**
- Content-Type: `multipart/form-data`
- Field: `file` (image file)

**Response:** `200 OK`
```json
{
  "id": 1,
  "user_id": 1,
  "image_path": "uploads/abc123-def456.jpg",
  "pest_type": "Aphid",
  "confidence": 0.85,
  "severity": "medium",
  "recommendations": "Apply neem oil spray. Monitor for 3-5 days.",
  "created_at": "2025-01-04T10:00:00"
}
```

**Mock Detection:**
- Randomly selects pest type (Aphid, Whitefly, Caterpillar, etc.)
- Random confidence (0.6-0.95)
- Severity based on confidence
- Actionable recommendations

---

### 3.3 List Detections
**GET** `/pest/`

Get list of pest detections with filtering.

**Query Parameters:**
- `skip` (int): Pagination offset
- `limit` (int): Max results
- `pest_type` (string): Filter by pest type
- `min_confidence` (float): Minimum confidence
- `severity` (string): Filter by severity (low/medium/high)

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "pest_type": "Aphid",
    "confidence": 0.85,
    "severity": "medium",
    "image_path": "uploads/abc123-def456.jpg",
    "created_at": "2025-01-04T10:00:00"
  }
]
```

---

### 3.4 Get Detection
**GET** `/pest/{id}`

Get specific pest detection.

**Response:** `200 OK` (same as detect response)

---

### 3.5 Delete Detection
**DELETE** `/pest/{id}`

Delete pest detection and associated image.

**Response:** `200 OK`
```json
{
  "message": "Pest detection deleted successfully"
}
```

---

### 3.6 Get Statistics
**GET** `/pest/stats/summary`

Get pest detection statistics.

**Response:** `200 OK`
```json
{
  "total_detections": 50,
  "by_pest_type": {
    "Aphid": 20,
    "Whitefly": 15,
    "Caterpillar": 10,
    "Leafhopper": 5
  },
  "by_severity": {
    "low": 10,
    "medium": 25,
    "high": 15
  },
  "avg_confidence": 0.78
}
```

---

## 4. Weather Endpoints (CORE FEATURE #1)

### 4.1 Get Current Weather
**GET** `/weather/current`

Get current weather conditions with alerts and recommendations.

**Query Parameters:**
- `lat` (float, required): Latitude
- `lon` (float, required): Longitude

**Example:**
```
GET /weather/current?lat=14.5995&lon=120.9842
```

**Response:** `200 OK`
```json
{
  "location": {
    "name": "Manila",
    "country": "PH",
    "lat": 14.5995,
    "lon": 120.9842
  },
  "current": {
    "temperature": 28.5,
    "feels_like": 32.0,
    "humidity": 75,
    "pressure": 1012,
    "wind_speed": 15.5,
    "wind_direction": 180,
    "description": "Partly cloudy",
    "icon": "02d"
  },
  "alerts": [
    {
      "type": "high_temperature",
      "severity": "warning",
      "message": "High temperature detected (28.5°C)"
    }
  ],
  "recommendations": [
    "Ensure adequate irrigation",
    "Monitor for heat stress in crops"
  ],
  "timestamp": "2025-01-04T10:00:00"
}
```

---

### 4.2 Get Weather Forecast
**GET** `/weather/forecast`

Get 5-day weather forecast (3-hour intervals).

**Query Parameters:**
- `lat` (float, required): Latitude
- `lon` (float, required): Longitude

**Response:** `200 OK`
```json
{
  "location": {
    "name": "Manila",
    "country": "PH"
  },
  "forecast": [
    {
      "datetime": "2025-01-04T12:00:00",
      "temperature": 29.0,
      "humidity": 70,
      "wind_speed": 12.0,
      "description": "Clear sky",
      "rain_probability": 10,
      "rainfall": 0.0
    }
  ]
}
```

---

### 4.3 Get Weather Summary
**GET** `/weather/summary`

Get complete weather summary (current + forecast + alerts).

**Query Parameters:**
- `lat` (float, required): Latitude
- `lon` (float, required): Longitude

**Response:** `200 OK`
```json
{
  "current": { /* current weather object */ },
  "forecast": [ /* forecast array */ ],
  "alerts": [ /* alerts array */ ],
  "recommendations": [ /* recommendations array */ ]
}
```

---

### 4.4 Test Weather API
**GET** `/weather/test`

Test OpenWeatherMap API configuration.

**Response:** `200 OK`
```json
{
  "status": "ok",
  "api_configured": true,
  "message": "Weather API is properly configured"
}
```

---

## 5. Alert Endpoints

### 5.1 List Alerts
**GET** `/alert/`

Get list of alerts with filtering.

**Query Parameters:**
- `skip` (int): Pagination offset
- `limit` (int): Max results
- `type` (string): Filter by type (sensor/weather/pest/system)
- `severity` (string): Filter by severity (info/warning/critical)
- `is_read` (bool): Filter by read status
- `is_acknowledged` (bool): Filter by acknowledged status

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "type": "sensor",
    "severity": "warning",
    "title": "High Temperature Alert",
    "message": "Temperature exceeds 32°C (current: 35°C)",
    "is_read": false,
    "is_acknowledged": false,
    "created_at": "2025-01-04T10:00:00"
  }
]
```

---

### 5.2 Get Alert
**GET** `/alert/{id}`

Get specific alert.

**Response:** `200 OK` (same as list item)

---

### 5.3 Update Alert
**PUT** `/alert/{id}`

Update alert (mark as read/acknowledged).

**Request Body:**
```json
{
  "is_read": true,
  "is_acknowledged": true
}
```

**Response:** `200 OK` (updated alert)

---

### 5.4 Delete Alert
**DELETE** `/alert/{id}`

Delete alert.

**Response:** `200 OK`
```json
{
  "message": "Alert deleted successfully"
}
```

---

### 5.5 Bulk Update Alerts
**PUT** `/alert/bulk`

Bulk update multiple alerts.

**Request Body:**
```json
{
  "alert_ids": [1, 2, 3],
  "is_read": true,
  "is_acknowledged": true
}
```

**Response:** `200 OK`
```json
{
  "updated_count": 3,
  "message": "3 alerts updated successfully"
}
```

---

### 5.6 Bulk Delete Alerts
**DELETE** `/alert/bulk`

Bulk delete multiple alerts.

**Request Body:**
```json
{
  "alert_ids": [1, 2, 3]
}
```

**Response:** `200 OK`
```json
{
  "deleted_count": 3,
  "message": "3 alerts deleted successfully"
}
```

---

### 5.7 Get Alert Statistics
**GET** `/alert/stats/summary`

Get alert statistics.

**Response:** `200 OK`
```json
{
  "total_alerts": 50,
  "unread_count": 15,
  "unacknowledged_count": 20,
  "by_type": {
    "sensor": 20,
    "weather": 15,
    "pest": 10,
    "system": 5
  },
  "by_severity": {
    "info": 10,
    "warning": 30,
    "critical": 10
  }
}
```

---

### 5.8 Trigger Alert Check
**POST** `/alert/check`

Manually trigger alert generation checks.

**Response:** `200 OK`
```json
{
  "message": "Alert checks completed",
  "alerts_generated": 3
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Username already registered"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "temperature"],
      "msg": "ensure this value is greater than or equal to -50",
      "type": "value_error"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Rate Limiting

Currently no rate limiting is implemented. In production, consider:
- 100 requests per minute per user
- 1000 requests per hour per user
- Special limits for image upload (10 per minute)

---

## Swagger Documentation

Interactive API documentation is available at:
- **Swagger UI:** `http://localhost:5000/swagger`
- **ReDoc:** `http://localhost:5000/redoc`

---

## Testing

Run tests with:
```bash
cd backend
pytest
```

Run with coverage:
```bash
pytest --cov=backend --cov-report=html
```

---

## Notes

1. **Mock ML:** Pest detection currently uses mock ML. Replace with real model in production.
2. **Weather API:** Requires OpenWeatherMap API key in `.env` file.
3. **Image Storage:** Images stored in `backend/uploads/` directory.
4. **Token Expiry:** JWT tokens expire after 30 days.
5. **Database:** Currently uses SQLite. Migrate to PostgreSQL for production.
