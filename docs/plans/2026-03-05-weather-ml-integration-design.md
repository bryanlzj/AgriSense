# Weather ML Model Integration — Design Document

> **Date:** 2026-03-05
> **Status:** Approved
> **Scope:** Integrate Random Forest weather classifier into AgriSense, overhaul weather page

---

## Context

A teammate trained a Random Forest classifier that predicts weather conditions from sensor data. The model consists of 3 pkl files that work together:

- `random_forest_model.pkl` — trained Random Forest model
- `random_forest_model_scaler.pkl` — feature scaler (normalizes inputs)
- `random_forest_model_encoder.pkl` — label encoder (maps numeric output → label)

**Output labels:** `Cloudy`, `Heavy Rain`, `Light Rain`, `Sunny`

**Input features (9):**
| Feature | Source (DB column) |
|---|---|
| `time` | `timestamp` |
| `temperature_2m` | `temperature` |
| `relative_humidity_2m` | `relative_humidity` |
| `rain` | `rain` |
| `wind_speed_10m` | `wind_speed` |
| `soil_temperature_0_to_7cm` | `soil_temperature` |
| `soil_moisture_0_to_7cm` | `soil_moisture` |
| `shortwave_radiation` | `solar_radiation` |
| `weather_code` | `weather_code` |

All input features already exist in the `sensor_readings` table.

### What the model CAN and CANNOT do

- **CAN:** Classify current weather from sensor readings → Sunny/Cloudy/Light Rain/Heavy Rain
- **CAN:** Classify historical sensor readings (same process, past data)
- **CANNOT:** Forecast future weather (it's a classifier, not a time-series forecaster — needs future inputs it can't produce)

### Decision: Weather Page Sections

| Section | Data Source | ML Model Role |
|---|---|---|
| **Current** | Latest sensor reading | ML classifies condition — replaces Open-Meteo |
| **Historical** | Past sensor readings from DB | ML classifications stored per reading |
| **Forecast** | Open-Meteo API (kept as-is) | Not applicable — needs a different model type |

---

## Section 1: Backend — Weather ML Service

**New file:** `backend/services/weather_ml_service.py`

Singleton pattern (same as `PestMLService`):

```python
class WeatherMLService:
    def __init__(self):
        self._model = None
        self._scaler = None
        self._encoder = None
        self._model_loaded = False

    def load_model(self, model_dir: str) -> bool:
        """Load model, scaler, encoder from pkl files."""
        # Uses joblib or pickle to load all 3 files
        # Returns True on success, False on failure

    @property
    def is_loaded(self) -> bool: ...

    def predict(self, features: dict) -> WeatherPredictionResult:
        """
        Takes sensor reading features dict →
        scale with scaler → predict with model → decode with encoder →
        returns WeatherPredictionResult(condition="Sunny", confidence=0.87)
        """
        # If model not loaded → mock fallback

# Module-level singleton
weather_ml_service = WeatherMLService()
```

**WeatherPredictionResult dataclass:**
```python
@dataclass
class WeatherPredictionResult:
    condition: Optional[str]     # "Sunny", "Cloudy", "Light Rain", "Heavy Rain"
    confidence: float            # 0.0 - 1.0 (from predict_proba)
    model_loaded: bool           # True = real model, False = mock
```

**Model files location:** Move from `weather/` to `backend/ml_models/weather/`:
```
backend/ml_models/
├── pest_model.pt
└── weather/
    ├── random_forest_model.pkl
    ├── random_forest_model_scaler.pkl
    └── random_forest_model_encoder.pkl
```

**Config additions (`config.py`):**
```python
use_mock_weather_ml: bool = Field(default=False, env="USE_MOCK_WEATHER_ML")
weather_model_path: str = Field(default="./ml_models/weather", env="WEATHER_MODEL_PATH")
```

**Startup (`main.py` lifespan):** Load weather ML model alongside pest model.

---

## Section 2: Database — Schema Change

**Add column to `sensor_readings` table:**
```python
weather_condition = Column(String(20), nullable=True)
# Stores: "Sunny", "Cloudy", "Light Rain", "Heavy Rain", or NULL
```

**Alembic migration:** `alembic revision --autogenerate -m "Add weather_condition to sensor_readings"`

- Existing rows get `NULL`
- Can backfill historically later if needed

**Auto-classify on save:** When the background job (scheduler) creates a sensor reading, immediately run `weather_ml_service.predict()` and set the `weather_condition` field before committing.

---

## Section 3: Backend — API Endpoints

### Modified: `GET /api/v1/weather/current`

**Before:** Fetches from Open-Meteo API
**After:** Returns latest sensor reading + ML classification from DB

**Response shape:**
```json
{
  "source": "sensor",
  "weather_condition": "Sunny",
  "confidence": 0.87,
  "temperature": 31.2,
  "relative_humidity": 72.5,
  "rain": 0.0,
  "wind_speed": 12.3,
  "soil_temperature": 28.5,
  "soil_moisture": 0.32,
  "solar_radiation": 650.0,
  "weather_code": 1,
  "timestamp": "2026-03-05T14:30:00Z",
  "model_loaded": true
}
```

**Fallback:** If no sensor reading exists, return error with message "No sensor data available".

### New: `GET /api/v1/weather/historical`

**Query params:**
- `period`: `24h` | `7d` | `custom` (default: `24h`)
- `start_date`: ISO datetime (required if period=custom)
- `end_date`: ISO datetime (required if period=custom)

**Response shape:**
```json
{
  "period": "24h",
  "start": "2026-03-04T14:30:00Z",
  "end": "2026-03-05T14:30:00Z",
  "readings_count": 48,
  "readings": [
    {
      "timestamp": "2026-03-04T14:30:00Z",
      "temperature": 30.5,
      "relative_humidity": 75.0,
      "rain": 0.0,
      "wind_speed": 10.2,
      "soil_temperature": 27.8,
      "soil_moisture": 0.31,
      "solar_radiation": 580.0,
      "weather_condition": "Sunny"
    }
  ],
  "summary": {
    "avg_temperature": 29.3,
    "max_temperature": 33.1,
    "min_temperature": 25.8,
    "avg_humidity": 73.2,
    "total_rain": 5.2,
    "dominant_condition": "Cloudy",
    "condition_breakdown": {
      "Sunny": 12,
      "Cloudy": 20,
      "Light Rain": 10,
      "Heavy Rain": 6
    }
  }
}
```

**Constraints:** Max 30 days for custom range. Data shaped for direct chart consumption.

### Unchanged: `GET /api/v1/weather/forecast`

Stays Open-Meteo powered. No changes.

### Unchanged: `GET /api/v1/weather/summary`

Will be updated to combine sensor-based current + Open-Meteo forecast.

---

## Section 4: Mobile — Weather Page Redesign

### Three-tab layout using `TabBar`/`TabBarView`:

**Tab 1 — Current**
- Large weather condition icon + label (ML classification)
- Grid of 6 sensor metrics:
  - Temperature, Humidity, Wind Speed
  - Rainfall, Soil Temperature, Soil Moisture
- "Last updated: X minutes ago"
- Source: "Sensor Data + AI Classification"

**Tab 2 — Historical**
- Period picker: segmented control (24h | 7d | Custom)
- Custom: date range picker dialog
- Line charts using `fl_chart` package:
  - Temperature over time (°C)
  - Humidity over time (%)
  - Rainfall over time (mm)
- Weather condition timeline (colored dots along x-axis)
- Summary card: avg temp, total rain, dominant condition

**Tab 3 — Forecast**
- Existing Open-Meteo forecast UI (24-hour horizontal scroll)
- Weather alerts and agricultural recommendations
- Labeled as "Forecast (Open-Meteo)"

### New Flutter dependency:
- `fl_chart` package for line charts

### Mobile service changes:
- `WeatherService.getCurrentWeather()` → hits modified `/weather/current` (sensor-based)
- `WeatherService.getHistorical()` → new method hitting `/weather/historical`
- `WeatherService.getForecast()` → unchanged (Open-Meteo)

---

## Section 5: Error Handling

| Scenario | Behavior |
|---|---|
| No sensor data | Show "No sensor data available" message with icon |
| ML model not loaded | Store `weather_condition = NULL`, show sensor data without classification label |
| Historical range empty | Show "No data for this period" |
| Historical range > 30 days | API returns 400 error |
| Open-Meteo down (forecast) | Existing fallback to mock data |

---

## Out of Scope

- Forecasting model (needs time-series model, not this classifier)
- IoT sensor hardware integration
- Backfilling historical `weather_condition` for existing rows
- Push notifications for weather changes
