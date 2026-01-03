# AgriSense API Contract

**Version:** 1.0  
**Last Updated:** January 4, 2026  
**Status:** Draft (Phase 0 Complete, Phase 1 Starting)

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Base URLs](#base-urls)
3. [Authentication](#authentication)
4. [Common Response Formats](#common-response-formats)
5. [Error Handling](#error-handling)
6. [Endpoints](#endpoints)
   - [Authentication](#authentication-endpoints)
   - [Sensor Readings](#sensor-readings-endpoints)
   - [Pest Detection](#pest-detection-endpoints)
   - [Alerts](#alerts-endpoints)
   - [Weather](#weather-endpoints)
7. [Data Models](#data-models)
8. [Testing](#testing)

---

## 🌐 Overview

This document defines the API contract between the AgriSense backend (FastAPI) and frontend (Flutter mobile app).

**Purpose:**
- Ensure backend and frontend teams can work in parallel
- Provide clear expectations for request/response formats
- Document all available endpoints
- Serve as reference during development

**Principles:**
- RESTful design
- JSON request/response bodies
- JWT token authentication
- Consistent error handling
- Pagination for list endpoints

---

## 🔗 Base URLs

### Development
```
http://localhost:8000
```

### Production
```
https://api.agrisense.com
```

**All endpoints are prefixed with `/api/v1`**

Example:
```
Full URL: http://localhost:8000/api/v1/auth/login
```

---

## 🔐 Authentication

### Authentication Method

**JWT (JSON Web Token) Bearer Authentication**

All protected endpoints require a JWT token in the `Authorization` header:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Token Lifetime

- **Access Token:** 30 days (simplified for learning project)
- **No refresh tokens** (simplified authentication)

### Getting a Token

1. Register a new user: `POST /api/v1/auth/register`
2. Login: `POST /api/v1/auth/login`
3. Receive token in response
4. Include token in all subsequent requests

### Token Format

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

## 📦 Common Response Formats

### Success Response

```json
{
  "id": 1,
  "field1": "value1",
  "field2": "value2"
}
```

### List Response (with Pagination)

```json
{
  "total": 100,
  "limit": 20,
  "offset": 0,
  "items": [
    {"id": 1, "...": "..."},
    {"id": 2, "...": "..."}
  ]
}
```

### Error Response

```json
{
  "detail": "Error message here"
}
```

### Validation Error Response

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

## ⚠️ Error Handling

### HTTP Status Codes

| Code | Meaning | When Used |
|------|---------|-----------|
| **200** | OK | Successful GET, PUT, DELETE |
| **201** | Created | Successful POST (resource created) |
| **400** | Bad Request | Invalid input data |
| **401** | Unauthorized | Missing or invalid authentication token |
| **403** | Forbidden | Valid token but insufficient permissions |
| **404** | Not Found | Resource doesn't exist |
| **422** | Unprocessable Entity | Validation error (detailed error info) |
| **500** | Internal Server Error | Server error (should be rare) |

### Error Response Format

All errors return JSON with a `detail` field:

```json
{
  "detail": "Human-readable error message"
}
```

### Common Error Scenarios

#### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

#### 404 Not Found
```json
{
  "detail": "Sensor reading not found"
}
```

#### 422 Validation Error
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

## 🔌 Endpoints

---

## 1. Authentication Endpoints

### 1.1 Register User

Create a new user account.

**Endpoint:** `POST /api/v1/auth/register`

**Authentication:** None (public endpoint)

**Request Body:**
```json
{
  "username": "farmer1",
  "password": "password123"
}
```

**Validation Rules:**
- `username`: Required, 3-50 characters, alphanumeric + underscore
- `password`: Required, minimum 8 characters

**Success Response (201 Created):**
```json
{
  "id": 1,
  "username": "farmer1",
  "is_active": true,
  "created_at": "2026-01-04T10:30:00.123456Z"
}
```

**Error Responses:**

**400 Bad Request** - Username already exists:
```json
{
  "detail": "Username already registered"
}
```

**422 Unprocessable Entity** - Validation error:
```json
{
  "detail": [
    {
      "loc": ["body", "password"],
      "msg": "ensure this value has at least 8 characters",
      "type": "value_error.any_str.min_length"
    }
  ]
}
```

**Example cURL:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"farmer1","password":"password123"}'
```

---

### 1.2 Login User

Authenticate user and receive JWT token.

**Endpoint:** `POST /api/v1/auth/login`

**Authentication:** None (public endpoint)

**Request Body:**
```json
{
  "username": "farmer1",
  "password": "password123"
}
```

**Success Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmYXJtZXIxIiwiZXhwIjoxNzA0NDUxMjAwfQ.abc123...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "farmer1",
    "is_active": true
  }
}
```

**Error Responses:**

**401 Unauthorized** - Invalid credentials:
```json
{
  "detail": "Incorrect username or password"
}
```

**Example cURL:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"farmer1","password":"password123"}'
```

**Flutter Example:**
```dart
// services/auth_service.dart
Future<AuthResponse> login(String username, String password) async {
  final response = await http.post(
    Uri.parse('$baseUrl/api/v1/auth/login'),
    headers: {'Content-Type': 'application/json'},
    body: json.encode({
      'username': username,
      'password': password,
    }),
  );
  
  if (response.statusCode == 200) {
    return AuthResponse.fromJson(json.decode(response.body));
  } else {
    throw Exception('Login failed');
  }
}
```

---

### 1.3 Get Current User

Get authenticated user's information.

**Endpoint:** `GET /api/v1/auth/me`

**Authentication:** Required (Bearer token)

**Request Headers:**
```http
Authorization: Bearer eyJhbGc...
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "username": "farmer1",
  "is_active": true,
  "created_at": "2026-01-04T10:30:00.123456Z",
  "updated_at": "2026-01-04T10:30:00.123456Z"
}
```

**Error Responses:**

**401 Unauthorized** - Missing or invalid token:
```json
{
  "detail": "Not authenticated"
}
```

**Example cURL:**
```bash
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer eyJhbGc..."
```

---

## 2. Sensor Readings Endpoints

### 2.1 Submit Sensor Reading

Submit a new sensor reading.

**Endpoint:** `POST /api/v1/sensors/readings`

**Authentication:** Required

**Request Headers:**
```http
Authorization: Bearer eyJhbGc...
Content-Type: application/json
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

**Validation Rules:**
- `temperature`: Required, float, -50 to 60 (°C)
- `humidity`: Required, float, 0 to 100 (%)
- `soil_moisture`: Required, float, 0 to 100 (%)
- `light_intensity`: Required, float, 0 to 200000 (lux)

**Success Response (201 Created):**
```json
{
  "id": 1,
  "user_id": 1,
  "temperature": 28.5,
  "humidity": 65.2,
  "soil_moisture": 52.3,
  "light_intensity": 45000,
  "timestamp": "2026-01-04T10:30:00.123456Z"
}
```

**Error Responses:**

**401 Unauthorized:**
```json
{
  "detail": "Not authenticated"
}
```

**422 Unprocessable Entity** - Validation error:
```json
{
  "detail": [
    {
      "loc": ["body", "temperature"],
      "msg": "ensure this value is less than or equal to 60",
      "type": "value_error.number.not_le"
    }
  ]
}
```

**Example cURL:**
```bash
curl -X POST http://localhost:8000/api/v1/sensors/readings \
  -H "Authorization: Bearer eyJhbGc..." \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 28.5,
    "humidity": 65.2,
    "soil_moisture": 52.3,
    "light_intensity": 45000
  }'
```

**Flutter Example:**
```dart
// services/sensor_service.dart
Future<SensorReading> submitReading({
  required double temperature,
  required double humidity,
  required double soilMoisture,
  required double lightIntensity,
}) async {
  final response = await http.post(
    Uri.parse('$baseUrl/api/v1/sensors/readings'),
    headers: {
      'Authorization': 'Bearer $token',
      'Content-Type': 'application/json',
    },
    body: json.encode({
      'temperature': temperature,
      'humidity': humidity,
      'soil_moisture': soilMoisture,
      'light_intensity': lightIntensity,
    }),
  );
  
  if (response.statusCode == 201) {
    return SensorReading.fromJson(json.decode(response.body));
  } else {
    throw Exception('Failed to submit reading');
  }
}
```

---

### 2.2 Get Sensor Readings

Get list of sensor readings for authenticated user.

**Endpoint:** `GET /api/v1/sensors/readings`

**Authentication:** Required

**Query Parameters:**
- `limit` (optional): Number of readings to return (default: 100, max: 500)
- `offset` (optional): Pagination offset (default: 0)
- `start_date` (optional): Filter from date (ISO 8601 format)
- `end_date` (optional): Filter to date (ISO 8601 format)

**Example URLs:**
```
GET /api/v1/sensors/readings
GET /api/v1/sensors/readings?limit=10&offset=0
GET /api/v1/sensors/readings?start_date=2026-01-01T00:00:00Z
GET /api/v1/sensors/readings?start_date=2026-01-01&end_date=2026-01-07
```

**Success Response (200 OK):**
```json
{
  "total": 168,
  "limit": 100,
  "offset": 0,
  "readings": [
    {
      "id": 168,
      "user_id": 1,
      "temperature": 27.8,
      "humidity": 68.5,
      "soil_moisture": 54.1,
      "light_intensity": 42000,
      "timestamp": "2026-01-04T14:30:00.123456Z"
    },
    {
      "id": 167,
      "user_id": 1,
      "temperature": 28.2,
      "humidity": 66.3,
      "soil_moisture": 53.8,
      "light_intensity": 48000,
      "timestamp": "2026-01-04T13:30:00.123456Z"
    }
  ]
}
```

**Error Responses:**

**401 Unauthorized:**
```json
{
  "detail": "Not authenticated"
}
```

**Example cURL:**
```bash
curl -X GET "http://localhost:8000/api/v1/sensors/readings?limit=10&offset=0" \
  -H "Authorization: Bearer eyJhbGc..."
```

**Flutter Example:**
```dart
// services/sensor_service.dart
Future<SensorReadingsResponse> getReadings({
  int limit = 100,
  int offset = 0,
  DateTime? startDate,
  DateTime? endDate,
}) async {
  var url = '$baseUrl/api/v1/sensors/readings?limit=$limit&offset=$offset';
  
  if (startDate != null) {
    url += '&start_date=${startDate.toIso8601String()}';
  }
  if (endDate != null) {
    url += '&end_date=${endDate.toIso8601String()}';
  }
  
  final response = await http.get(
    Uri.parse(url),
    headers: {'Authorization': 'Bearer $token'},
  );
  
  if (response.statusCode == 200) {
    return SensorReadingsResponse.fromJson(json.decode(response.body));
  } else {
    throw Exception('Failed to load readings');
  }
}
```

---

### 2.3 Get Latest Sensor Reading

Get the most recent sensor reading for authenticated user.

**Endpoint:** `GET /api/v1/sensors/readings/latest`

**Authentication:** Required

**Success Response (200 OK):**
```json
{
  "id": 168,
  "user_id": 1,
  "temperature": 27.8,
  "humidity": 68.5,
  "soil_moisture": 54.1,
  "light_intensity": 42000,
  "timestamp": "2026-01-04T14:30:00.123456Z"
}
```

**Error Responses:**

**404 Not Found** - No readings exist:
```json
{
  "detail": "No sensor readings found"
}
```

**Example cURL:**
```bash
curl -X GET http://localhost:8000/api/v1/sensors/readings/latest \
  -H "Authorization: Bearer eyJhbGc..."
```

---

### 2.4 Get Sensor Reading by ID

Get a specific sensor reading by ID.

**Endpoint:** `GET /api/v1/sensors/readings/{reading_id}`

**Authentication:** Required

**Path Parameters:**
- `reading_id`: Integer, ID of the sensor reading

**Success Response (200 OK):**
```json
{
  "id": 1,
  "user_id": 1,
  "temperature": 28.5,
  "humidity": 65.2,
  "soil_moisture": 52.3,
  "light_intensity": 45000,
  "timestamp": "2026-01-04T10:30:00.123456Z"
}
```

**Error Responses:**

**404 Not Found:**
```json
{
  "detail": "Sensor reading not found"
}
```

**403 Forbidden** - Reading belongs to another user:
```json
{
  "detail": "Not authorized to access this reading"
}
```

---

## 3. Pest Detection Endpoints

### 3.1 Detect Pest (Upload Image)

Upload an image for pest detection.

**Endpoint:** `POST /api/v1/pests/detect`

**Authentication:** Required

**Request Headers:**
```http
Authorization: Bearer eyJhbGc...
Content-Type: multipart/form-data
```

**Request Body (Form Data):**
```
image: <file> (JPEG, JPG, PNG only, max 10MB)
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "user_id": 1,
  "image_url": "/uploads/pest_20260104_103000_abc123.jpg",
  "pest_type": "Fall Armyworm",
  "confidence_score": 0.87,
  "severity_level": "high",
  "recommendations": "Apply recommended pesticide immediately. Monitor field daily. Consider biological control methods.",
  "detected_at": "2026-01-04T10:30:00.123456Z"
}
```

**Error Responses:**

**400 Bad Request** - Invalid file format:
```json
{
  "detail": "Invalid image format. Only JPG, JPEG, PNG allowed."
}
```

**400 Bad Request** - File too large:
```json
{
  "detail": "Image file too large. Maximum size is 10MB."
}
```

**422 Unprocessable Entity** - No file provided:
```json
{
  "detail": [
    {
      "loc": ["body", "image"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**Example cURL:**
```bash
curl -X POST http://localhost:8000/api/v1/pests/detect \
  -H "Authorization: Bearer eyJhbGc..." \
  -F "image=@/path/to/pest_image.jpg"
```

**Flutter Example:**
```dart
// services/pest_service.dart
Future<PestDetection> detectPest(File imageFile) async {
  var request = http.MultipartRequest(
    'POST',
    Uri.parse('$baseUrl/api/v1/pests/detect'),
  );
  
  request.headers['Authorization'] = 'Bearer $token';
  request.files.add(await http.MultipartFile.fromPath(
    'image',
    imageFile.path,
  ));
  
  var streamedResponse = await request.send();
  var response = await http.Response.fromStream(streamedResponse);
  
  if (response.statusCode == 200) {
    return PestDetection.fromJson(json.decode(response.body));
  } else {
    throw Exception('Failed to detect pest');
  }
}
```

---

### 3.2 Get Pest Detections

Get list of pest detections for authenticated user.

**Endpoint:** `GET /api/v1/pests/detections`

**Authentication:** Required

**Query Parameters:**
- `limit` (optional): Number of detections to return (default: 50, max: 200)
- `offset` (optional): Pagination offset (default: 0)
- `severity` (optional): Filter by severity level (low, medium, high)

**Example URLs:**
```
GET /api/v1/pests/detections
GET /api/v1/pests/detections?limit=10&offset=0
GET /api/v1/pests/detections?severity=high
```

**Success Response (200 OK):**
```json
{
  "total": 9,
  "limit": 50,
  "offset": 0,
  "detections": [
    {
      "id": 1,
      "user_id": 1,
      "image_url": "/uploads/pest_20260104_103000_abc123.jpg",
      "pest_type": "Fall Armyworm",
      "confidence_score": 0.87,
      "severity_level": "high",
      "recommendations": "Apply recommended pesticide immediately.",
      "detected_at": "2026-01-04T10:30:00.123456Z"
    },
    {
      "id": 2,
      "user_id": 1,
      "image_url": "/uploads/pest_20260103_152000_def456.jpg",
      "pest_type": "Aphids",
      "confidence_score": 0.85,
      "severity_level": "medium",
      "recommendations": "Use insecticidal soap or neem oil.",
      "detected_at": "2026-01-03T15:20:00.123456Z"
    }
  ]
}
```

**Error Responses:**

**401 Unauthorized:**
```json
{
  "detail": "Not authenticated"
}
```

**Example cURL:**
```bash
curl -X GET "http://localhost:8000/api/v1/pests/detections?limit=10" \
  -H "Authorization: Bearer eyJhbGc..."
```

---

### 3.3 Get Pest Detection by ID

Get a specific pest detection by ID.

**Endpoint:** `GET /api/v1/pests/detections/{detection_id}`

**Authentication:** Required

**Path Parameters:**
- `detection_id`: Integer, ID of the pest detection

**Success Response (200 OK):**
```json
{
  "id": 1,
  "user_id": 1,
  "image_url": "/uploads/pest_20260104_103000_abc123.jpg",
  "pest_type": "Fall Armyworm",
  "confidence_score": 0.87,
  "severity_level": "high",
  "detections_json": {
    "bounding_boxes": [
      {"x": 100, "y": 150, "width": 200, "height": 180}
    ],
    "all_predictions": {
      "Fall Armyworm": 0.87,
      "Aphids": 0.08,
      "Whitefly": 0.03,
      "Healthy": 0.02
    }
  },
  "recommendations": "Apply recommended pesticide immediately. Monitor field daily.",
  "detected_at": "2026-01-04T10:30:00.123456Z"
}
```

**Error Responses:**

**404 Not Found:**
```json
{
  "detail": "Pest detection not found"
}
```

**403 Forbidden:**
```json
{
  "detail": "Not authorized to access this detection"
}
```

---

## 4. Alerts Endpoints

### 4.1 Get Alerts

Get list of alerts for authenticated user.

**Endpoint:** `GET /api/v1/alerts`

**Authentication:** Required

**Query Parameters:**
- `limit` (optional): Number of alerts to return (default: 50, max: 200)
- `offset` (optional): Pagination offset (default: 0)
- `is_read` (optional): Filter by read status (true/false)
- `alert_type` (optional): Filter by type (weather, pest, environmental, system)
- `severity` (optional): Filter by severity (low, medium, high, critical)

**Example URLs:**
```
GET /api/v1/alerts
GET /api/v1/alerts?is_read=false
GET /api/v1/alerts?alert_type=weather&severity=high
GET /api/v1/alerts?is_read=false&severity=critical
```

**Success Response (200 OK):**
```json
{
  "total": 12,
  "unread_count": 8,
  "limit": 50,
  "offset": 0,
  "alerts": [
    {
      "id": 1,
      "user_id": 1,
      "alert_type": "weather",
      "severity": "high",
      "title": "Heavy Rain Warning",
      "message": "Heavy rain (65mm) expected tomorrow. Take precautions to protect your crops.",
      "recommendations": "Cover crops if possible. Prepare drainage systems. Secure loose equipment.",
      "is_read": false,
      "read_at": null,
      "expires_at": "2026-01-05T23:59:59Z",
      "alert_metadata": {
        "forecast_precipitation": 65.0,
        "forecast_date": "2026-01-05",
        "location": "Nairobi"
      },
      "created_at": "2026-01-04T08:00:00.123456Z",
      "updated_at": "2026-01-04T08:00:00.123456Z"
    },
    {
      "id": 2,
      "user_id": 1,
      "alert_type": "pest",
      "severity": "critical",
      "title": "Fall Armyworm Detected",
      "message": "Fall Armyworm detected in your field with 87% confidence.",
      "recommendations": "Apply recommended pesticide immediately. Monitor field daily.",
      "is_read": false,
      "read_at": null,
      "expires_at": null,
      "alert_metadata": {
        "pest_type": "Fall Armyworm",
        "confidence": 0.87,
        "detection_id": 1
      },
      "created_at": "2026-01-04T10:30:00.123456Z",
      "updated_at": "2026-01-04T10:30:00.123456Z"
    }
  ]
}
```

**Error Responses:**

**401 Unauthorized:**
```json
{
  "detail": "Not authenticated"
}
```

**Example cURL:**
```bash
curl -X GET "http://localhost:8000/api/v1/alerts?is_read=false" \
  -H "Authorization: Bearer eyJhbGc..."
```

**Flutter Example:**
```dart
// services/alert_service.dart
Future<AlertsResponse> getAlerts({
  int limit = 50,
  int offset = 0,
  bool? isRead,
  String? alertType,
  String? severity,
}) async {
  var url = '$baseUrl/api/v1/alerts?limit=$limit&offset=$offset';
  
  if (isRead != null) {
    url += '&is_read=$isRead';
  }
  if (alertType != null) {
    url += '&alert_type=$alertType';
  }
  if (severity != null) {
    url += '&severity=$severity';
  }
  
  final response = await http.get(
    Uri.parse(url),
    headers: {'Authorization': 'Bearer $token'},
  );
  
  if (response.statusCode == 200) {
    return AlertsResponse.fromJson(json.decode(response.body));
  } else {
    throw Exception('Failed to load alerts');
  }
}
```

---

### 4.2 Mark Alert as Read

Mark a specific alert as read.

**Endpoint:** `PUT /api/v1/alerts/{alert_id}/read`

**Authentication:** Required

**Path Parameters:**
- `alert_id`: Integer, ID of the alert

**Success Response (200 OK):**
```json
{
  "id": 1,
  "user_id": 1,
  "alert_type": "weather",
  "severity": "high",
  "title": "Heavy Rain Warning",
  "message": "Heavy rain (65mm) expected tomorrow.",
  "recommendations": "Cover crops if possible.",
  "is_read": true,
  "read_at": "2026-01-04T15:00:00.123456Z",
  "expires_at": "2026-01-05T23:59:59Z",
  "created_at": "2026-01-04T08:00:00.123456Z",
  "updated_at": "2026-01-04T15:00:00.123456Z"
}
```

**Error Responses:**

**404 Not Found:**
```json
{
  "detail": "Alert not found"
}
```

**403 Forbidden:**
```json
{
  "detail": "Not authorized to access this alert"
}
```

**Example cURL:**
```bash
curl -X PUT http://localhost:8000/api/v1/alerts/1/read \
  -H "Authorization: Bearer eyJhbGc..."
```

**Flutter Example:**
```dart
// services/alert_service.dart
Future<Alert> markAsRead(int alertId) async {
  final response = await http.put(
    Uri.parse('$baseUrl/api/v1/alerts/$alertId/read'),
    headers: {'Authorization': 'Bearer $token'},
  );
  
  if (response.statusCode == 200) {
    return Alert.fromJson(json.decode(response.body));
  } else {
    throw Exception('Failed to mark alert as read');
  }
}
```

---

### 4.3 Get Alert by ID

Get a specific alert by ID.

**Endpoint:** `GET /api/v1/alerts/{alert_id}`

**Authentication:** Required

**Path Parameters:**
- `alert_id`: Integer, ID of the alert

**Success Response (200 OK):**
```json
{
  "id": 1,
  "user_id": 1,
  "alert_type": "weather",
  "severity": "high",
  "title": "Heavy Rain Warning",
  "message": "Heavy rain (65mm) expected tomorrow. Take precautions to protect your crops.",
  "recommendations": "Cover crops if possible. Prepare drainage systems. Secure loose equipment.",
  "is_read": false,
  "read_at": null,
  "expires_at": "2026-01-05T23:59:59Z",
  "alert_metadata": {
    "forecast_precipitation": 65.0,
    "forecast_date": "2026-01-05",
    "location": "Nairobi"
  },
  "created_at": "2026-01-04T08:00:00.123456Z",
  "updated_at": "2026-01-04T08:00:00.123456Z"
}
```

**Error Responses:**

**404 Not Found:**
```json
{
  "detail": "Alert not found"
}
```

---

## 5. Weather Endpoints

### 5.1 Get Weather Forecast

Get weather forecast for user's location.

**Endpoint:** `GET /api/v1/weather/forecast`

**Authentication:** Required

**Query Parameters:**
- `days` (optional): Number of days to forecast (default: 7, max: 7)
- `lat` (optional): Latitude (if not provided, uses user's default location)
- `lon` (optional): Longitude (if not provided, uses user's default location)

**Example URLs:**
```
GET /api/v1/weather/forecast
GET /api/v1/weather/forecast?days=3
GET /api/v1/weather/forecast?lat=-1.286389&lon=36.817223
```

**Success Response (200 OK):**
```json
{
  "location": {
    "name": "Nairobi",
    "country": "Kenya",
    "lat": -1.286389,
    "lon": 36.817223
  },
  "current": {
    "temperature": 24.5,
    "feels_like": 23.8,
    "humidity": 65,
    "pressure": 1013,
    "wind_speed": 3.5,
    "wind_direction": 180,
    "description": "Partly cloudy",
    "icon": "02d",
    "timestamp": "2026-01-04T15:00:00Z"
  },
  "forecast": [
    {
      "date": "2026-01-05",
      "temp_min": 18.0,
      "temp_max": 26.5,
      "humidity": 60,
      "precipitation": 0,
      "precipitation_probability": 10,
      "wind_speed": 4.2,
      "description": "Sunny",
      "icon": "01d"
    },
    {
      "date": "2026-01-06",
      "temp_min": 19.0,
      "temp_max": 27.0,
      "humidity": 70,
      "precipitation": 15,
      "precipitation_probability": 80,
      "wind_speed": 5.5,
      "description": "Light rain",
      "icon": "10d"
    },
    {
      "date": "2026-01-07",
      "temp_min": 17.5,
      "temp_max": 25.0,
      "humidity": 75,
      "precipitation": 25,
      "precipitation_probability": 90,
      "wind_speed": 6.0,
      "description": "Moderate rain",
      "icon": "10d"
    }
  ]
}
```

**Error Responses:**

**400 Bad Request** - Invalid coordinates:
```json
{
  "detail": "Invalid latitude or longitude"
}
```

**503 Service Unavailable** - Weather API error:
```json
{
  "detail": "Weather service temporarily unavailable"
}
```

**Example cURL:**
```bash
curl -X GET "http://localhost:8000/api/v1/weather/forecast?days=7" \
  -H "Authorization: Bearer eyJhbGc..."
```

**Flutter Example:**
```dart
// services/weather_service.dart
Future<WeatherForecast> getForecast({int days = 7}) async {
  final response = await http.get(
    Uri.parse('$baseUrl/api/v1/weather/forecast?days=$days'),
    headers: {'Authorization': 'Bearer $token'},
  );
  
  if (response.statusCode == 200) {
    return WeatherForecast.fromJson(json.decode(response.body));
  } else {
    throw Exception('Failed to load weather forecast');
  }
}
```

---

### 5.2 Get Current Weather

Get current weather conditions.

**Endpoint:** `GET /api/v1/weather/current`

**Authentication:** Required

**Query Parameters:**
- `lat` (optional): Latitude
- `lon` (optional): Longitude

**Success Response (200 OK):**
```json
{
  "location": {
    "name": "Nairobi",
    "country": "Kenya",
    "lat": -1.286389,
    "lon": 36.817223
  },
  "temperature": 24.5,
  "feels_like": 23.8,
  "humidity": 65,
  "pressure": 1013,
  "wind_speed": 3.5,
  "wind_direction": 180,
  "description": "Partly cloudy",
  "icon": "02d",
  "timestamp": "2026-01-04T15:00:00Z"
}
```

---

## 📊 Data Models

### User

```json
{
  "id": 1,
  "username": "farmer1",
  "is_active": true,
  "created_at": "2026-01-04T10:30:00.123456Z",
  "updated_at": "2026-01-04T10:30:00.123456Z"
}
```

### SensorReading

```json
{
  "id": 1,
  "user_id": 1,
  "temperature": 28.5,
  "humidity": 65.2,
  "soil_moisture": 52.3,
  "light_intensity": 45000,
  "timestamp": "2026-01-04T10:30:00.123456Z"
}
```

**Field Descriptions:**
- `temperature`: Temperature in Celsius (-50 to 60)
- `humidity`: Relative humidity percentage (0 to 100)
- `soil_moisture`: Soil moisture percentage (0 to 100)
- `light_intensity`: Light intensity in lux (0 to 200000)

### PestDetection

```json
{
  "id": 1,
  "user_id": 1,
  "image_url": "/uploads/pest_20260104_103000_abc123.jpg",
  "pest_type": "Fall Armyworm",
  "confidence_score": 0.87,
  "severity_level": "high",
  "detections_json": {
    "bounding_boxes": [...],
    "all_predictions": {...}
  },
  "recommendations": "Apply recommended pesticide immediately.",
  "detected_at": "2026-01-04T10:30:00.123456Z"
}
```

**Field Descriptions:**
- `pest_type`: Name of detected pest
- `confidence_score`: ML model confidence (0.0 to 1.0)
- `severity_level`: Risk level (low, medium, high)
- `detections_json`: Additional ML model output (optional)
- `recommendations`: Treatment recommendations

**Pest Types:**
- Fall Armyworm
- Aphids
- Whitefly
- Healthy (No Pest)

**Severity Levels:**
- `low`: confidence < 0.70
- `medium`: 0.70 ≤ confidence < 0.85
- `high`: confidence ≥ 0.85

### Alert

```json
{
  "id": 1,
  "user_id": 1,
  "alert_type": "weather",
  "severity": "high",
  "title": "Heavy Rain Warning",
  "message": "Heavy rain (65mm) expected tomorrow.",
  "recommendations": "Cover crops if possible.",
  "is_read": false,
  "read_at": null,
  "expires_at": "2026-01-05T23:59:59Z",
  "alert_metadata": {...},
  "created_at": "2026-01-04T08:00:00.123456Z",
  "updated_at": "2026-01-04T08:00:00.123456Z"
}
```

**Alert Types:**
- `weather`: Weather-related alerts
- `pest`: Pest detection alerts
- `environmental`: Sensor anomaly alerts
- `system`: System notifications

**Severity Levels:**
- `low`: Informational
- `medium`: Attention needed
- `high`: Action recommended
- `critical`: Immediate action required

---

## 🧪 Testing

### Using Swagger UI

1. Start backend server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

2. Open browser:
   ```
   http://localhost:8000/docs
   ```

3. Test endpoints:
   - Click on endpoint
   - Click "Try it out"
   - Fill in parameters
   - Click "Execute"
   - View response

### Using Postman

1. Import collection:
   - File → Import
   - Select `docs/AgriSense.postman_collection.json`

2. Set environment:
   - Create environment "AgriSense Dev"
   - Add variable: `base_url` = `http://localhost:8000`
   - Add variable: `token` = (will be set after login)

3. Test flow:
   - Register user
   - Login (saves token automatically)
   - Test protected endpoints

### Using cURL

```bash
# 1. Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'

# 2. Login (save token)
TOKEN=$(curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}' \
  | jq -r '.access_token')

# 3. Get current user
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer $TOKEN"

# 4. Submit sensor reading
curl -X POST http://localhost:8000/api/v1/sensors/readings \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 28.5,
    "humidity": 65.2,
    "soil_moisture": 52.3,
    "light_intensity": 45000
  }'

# 5. Get sensor readings
curl -X GET http://localhost:8000/api/v1/sensors/readings \
  -H "Authorization: Bearer $TOKEN"
```

### Flutter Integration Testing

```dart
// test/integration/api_test.dart
void main() {
  group('API Integration Tests', () {
    late AuthService authService;
    late SensorService sensorService;
    String? token;

    setUp(() {
      authService = AuthService(baseUrl: 'http://localhost:8000');
      sensorService = SensorService(baseUrl: 'http://localhost:8000');
    });

    test('Register and login flow', () async {
      // Register
      final registerResponse = await authService.register(
        username: 'testuser',
        password: 'testpass123',
      );
      expect(registerResponse.username, 'testuser');

      // Login
      final loginResponse = await authService.login(
        username: 'testuser',
        password: 'testpass123',
      );
      expect(loginResponse.accessToken, isNotEmpty);
      token = loginResponse.accessToken;
    });

    test('Submit and retrieve sensor reading', () async {
      // Submit reading
      final reading = await sensorService.submitReading(
        token: token!,
        temperature: 28.5,
        humidity: 65.2,
        soilMoisture: 52.3,
        lightIntensity: 45000,
      );
      expect(reading.temperature, 28.5);

      // Get readings
      final readings = await sensorService.getReadings(token: token!);
      expect(readings.readings.length, greaterThan(0));
    });
  });
}
```

---

## 📝 Notes

### Date/Time Format

All timestamps use **ISO 8601 format** with UTC timezone:
```
2026-01-04T10:30:00.123456Z
```

### Pagination

List endpoints support pagination:
- `limit`: Number of items per page
- `offset`: Number of items to skip
- `total`: Total number of items available

Example:
```
Page 1: limit=20, offset=0   (items 1-20)
Page 2: limit=20, offset=20  (items 21-40)
Page 3: limit=20, offset=40  (items 41-60)
```

### Image Upload

- **Supported formats:** JPG, JPEG, PNG
- **Maximum size:** 10MB
- **Storage:** Images stored in `/uploads/` directory
- **URL format:** `/uploads/pest_YYYYMMDD_HHMMSS_randomid.jpg`

### Rate Limiting

(To be implemented in production)
- 100 requests per minute per user
- 1000 requests per hour per user

---

## 🔄 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-04 | Initial API contract created |

---

## 📞 Contact

**Backend Team:**
- Member 1 (Backend Lead): [email]
- Member 2 (Backend Dev): [email]

**Frontend Team:**
- Member 3 (Flutter Dev): [email]

**For API questions or changes:**
- Create GitHub issue with label `api-contract`
- Discuss in #integration Slack channel
- Update this document after agreement

---

**Last Updated:** January 4, 2026  
**Next Review:** After Phase 1 completion
