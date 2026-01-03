# AgriSense API Structure

This document outlines the API endpoint structure for the AgriSense backend.

## Base URL

- **Development:** `http://localhost:8000`
- **Production:** `https://your-domain.com`

## API Version

All endpoints are prefixed with `/api/v1` for versioning.

---

## 📚 API Documentation

- **Swagger UI:** `/docs` - Interactive API documentation
- **ReDoc:** `/redoc` - Alternative documentation format

---

## 🔐 Authentication Endpoints

**Base Path:** `/api/v1/auth`

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/register` | Register new user | No |
| POST | `/login` | Login and get access token | No |
| GET | `/me` | Get current user profile | Yes |
| PUT | `/me` | Update user profile | Yes |

### Request/Response Examples:

#### Register
```json
POST /api/v1/auth/register
{
  "username": "farmer1",
  "password": "password123",
  "full_name": "John Kamau",
  "location": "Kiambu County"
}

Response: 201 Created
{
  "id": 1,
  "username": "farmer1",
  "full_name": "John Kamau",
  "location": "Kiambu County",
  "created_at": "2025-01-16T10:00:00Z"
}
```

#### Login
```json
POST /api/v1/auth/login
{
  "username": "farmer1",
  "password": "password123"
}

Response: 200 OK
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 2592000
}
```

---

## 📊 Sensor Endpoints

**Base Path:** `/api/v1/sensors`

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/readings` | Create new sensor reading | Yes |
| GET | `/readings` | List sensor readings (paginated) | Yes |
| GET | `/readings/{id}` | Get specific reading | Yes |
| GET | `/readings/latest` | Get latest reading | Yes |
| GET | `/readings/stats` | Get statistics (avg, min, max) | Yes |

### Request/Response Examples:

#### Create Reading
```json
POST /api/v1/sensors/readings
{
  "temperature": 28.5,
  "humidity": 65.2,
  "soil_moisture": 52.3,
  "light_intensity": 45000
}

Response: 201 Created
{
  "id": 1,
  "user_id": 1,
  "temperature": 28.5,
  "humidity": 65.2,
  "soil_moisture": 52.3,
  "light_intensity": 45000,
  "is_anomaly": false,
  "created_at": "2025-01-16T14:30:00Z"
}
```

#### List Readings
```json
GET /api/v1/sensors/readings?skip=0&limit=10&days=7

Response: 200 OK
{
  "total": 168,
  "readings": [
    {
      "id": 168,
      "temperature": 28.5,
      "humidity": 65.2,
      "created_at": "2025-01-16T14:30:00Z"
    },
    // ... more readings
  ]
}
```

---

## 🐛 Pest Detection Endpoints

**Base Path:** `/api/v1/pests`

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/detect` | Upload image for pest detection | Yes |
| GET | `/detections` | List pest detections (paginated) | Yes |
| GET | `/detections/{id}` | Get specific detection | Yes |
| GET | `/detections/stats` | Get pest statistics | Yes |

### Request/Response Examples:

#### Detect Pest
```json
POST /api/v1/pests/detect
Content-Type: multipart/form-data

image: [binary file data]

Response: 201 Created
{
  "id": 1,
  "user_id": 1,
  "pest_name": "Fall Armyworm",
  "confidence": 0.92,
  "severity": "high",
  "image_path": "/uploads/pest_1_20250116_143000.jpg",
  "recommendations": [
    "Apply Bacillus thuringiensis (Bt) spray",
    "Remove and destroy affected plants",
    "Monitor field daily for new infestations"
  ],
  "created_at": "2025-01-16T14:30:00Z"
}
```

#### List Detections
```json
GET /api/v1/pests/detections?skip=0&limit=10

Response: 200 OK
{
  "total": 5,
  "detections": [
    {
      "id": 5,
      "pest_name": "Fall Armyworm",
      "confidence": 0.92,
      "severity": "high",
      "created_at": "2025-01-16T14:30:00Z"
    },
    // ... more detections
  ]
}
```

---

## 🔔 Alert Endpoints

**Base Path:** `/api/v1/alerts`

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | List alerts (paginated) | Yes |
| GET | `/{id}` | Get specific alert | Yes |
| PUT | `/{id}/read` | Mark alert as read | Yes |
| DELETE | `/{id}` | Delete alert | Yes |
| GET | `/unread/count` | Get unread alert count | Yes |
| GET | `/urgent` | Get urgent unread alerts | Yes |

### Request/Response Examples:

#### List Alerts
```json
GET /api/v1/alerts?skip=0&limit=10&unread_only=true

Response: 200 OK
{
  "total": 3,
  "alerts": [
    {
      "id": 1,
      "alert_type": "heavy_rain",
      "severity": "high",
      "title": "Heavy Rain Warning",
      "message": "Heavy rain (65mm) expected tomorrow.",
      "recommendations": ["Cover crops", "Prepare drainage"],
      "is_read": false,
      "created_at": "2025-01-16T10:00:00Z"
    },
    // ... more alerts
  ]
}
```

#### Mark as Read
```json
PUT /api/v1/alerts/1/read

Response: 200 OK
{
  "id": 1,
  "is_read": true,
  "read_at": "2025-01-16T15:00:00Z"
}
```

---

## 🌤️ Weather Endpoints

**Base Path:** `/api/v1/weather`

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/forecast` | Get 7-day weather forecast | Yes |
| GET | `/current` | Get current weather | Yes |
| POST | `/alerts/check` | Check for weather anomalies | Yes |

### Request/Response Examples:

#### Get Forecast
```json
GET /api/v1/weather/forecast?location=Kiambu

Response: 200 OK
{
  "location": "Kiambu, Kenya",
  "forecast": [
    {
      "date": "2025-01-17",
      "temperature_max": 28.5,
      "temperature_min": 18.2,
      "precipitation": 5.0,
      "humidity": 65,
      "description": "Partly cloudy",
      "icon": "02d"
    },
    // ... 6 more days
  ]
}
```

---

## 🔒 Authentication

All protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Token Expiration

- Access tokens expire after **30 days**
- No refresh tokens (simplified authentication)
- User must login again after expiration

---

## 📄 Pagination

List endpoints support pagination with query parameters:

- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum records to return (default: 10, max: 100)

Example: `/api/v1/sensors/readings?skip=20&limit=10`

---

## ⚠️ Error Responses

All errors follow a consistent format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | Resource retrieved |
| 201 | Created | Resource created |
| 400 | Bad Request | Invalid input data |
| 401 | Unauthorized | Missing or invalid token |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 422 | Validation Error | Pydantic validation failed |
| 500 | Server Error | Internal server error |

---

## 🧪 Testing the API

### Using Swagger UI

1. Start the backend: `uvicorn main:app --reload`
2. Open browser: `http://localhost:8000/docs`
3. Click "Authorize" button
4. Login to get token
5. Paste token in authorization dialog
6. Test endpoints interactively

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

# Get readings (with token)
curl -X GET http://localhost:8000/api/v1/sensors/readings \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 📝 Notes

- All timestamps are in UTC (ISO 8601 format)
- All responses are JSON
- File uploads use `multipart/form-data`
- Maximum file size: 10MB (for pest images)
- Rate limiting: Not implemented (add in production)

---

## 🚀 Next Steps

1. Implement authentication router (Task 1.1.1)
2. Implement sensor data router (Task 1.2.1)
3. Implement pest detection router (Task 1.3.1)
4. Implement alert router (Task 1.4.1)
5. Implement weather router (Task 1.5.1)
