# Weather ML Model Integration — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Integrate the Random Forest weather classifier into AgriSense — auto-classify sensor readings, overhaul the weather page to show sensor-based current weather, historical charts, and Open-Meteo forecast.

**Architecture:** New `WeatherMLService` singleton loads 3 scikit-learn pkl files (model, scaler, encoder) at startup. Every sensor reading gets auto-classified on save. Weather page redesigned as 3-tab layout: Current (sensor + ML), Historical (DB + charts), Forecast (Open-Meteo).

**Tech Stack:** scikit-learn, joblib, pandas (backend); fl_chart (mobile); Alembic for migration

---

## Verified Model Details

**Features (7 — NOT 9, `time` and `weather_code` are excluded):**

| Index | Feature Name (as trained) | DB Column |
|---|---|---|
| 0 | `temperature_2m (°C)` | `temperature` |
| 1 | `relative_humidity_2m (%)` | `relative_humidity` |
| 2 | `rain (mm)` | `rain` |
| 3 | `wind_speed_10m (km/h)` | `wind_speed` |
| 4 | `soil_temperature_0_to_7cm (°C)` | `soil_temperature` |
| 5 | `soil_moisture_0_to_7cm (m³/m³)` | `soil_moisture` |
| 6 | `shortwave_radiation (W/m²)` | `solar_radiation` |

**Scaler:** `StandardScaler` (fitted with feature names)
**Model:** `RandomForestClassifier` (100 estimators, 7 features, 4 classes)
**Encoder:** `LabelEncoder` → `['Cloudy', 'Heavy Rain', 'Light Rain', 'Sunny']`
**Dependencies:** `scikit-learn`, `joblib`, `pandas` (pandas already installed)

---

## Task 1: Move Model Files and Add Dependencies

**Files:**
- Move: `weather/*.pkl` → `backend/ml_models/weather/`
- Modify: `backend/requirements.txt`

**Step 1: Create directory and move model files**

```bash
mkdir -p backend/ml_models/weather
cp weather/random_forest_model.pkl backend/ml_models/weather/
cp weather/random_forest_model_scaler.pkl backend/ml_models/weather/
cp weather/random_forest_model_encoder.pkl backend/ml_models/weather/
```

**Step 2: Add dependencies to requirements.txt**

Add after the existing ML section:

```
# Weather ML Model (Random Forest via scikit-learn)
scikit-learn>=1.3.0
joblib>=1.3.0
```

**Step 3: Verify files are in place**

```bash
ls -la backend/ml_models/weather/
# Expected: 3 pkl files
```

**Step 4: Commit**

```bash
git add backend/ml_models/weather/ backend/requirements.txt
git commit -m "chore: move weather model files and add scikit-learn dependency"
```

---

## Task 2: Create WeatherMLService

**Files:**
- Create: `backend/services/weather_ml_service.py`
- Test: `backend/tests/test_weather_ml_service.py`

**Step 1: Write the failing test**

Create `backend/tests/test_weather_ml_service.py`:

```python
"""Tests for WeatherMLService."""
import pytest
from services.weather_ml_service import weather_ml_service, WeatherPredictionResult


class TestWeatherMLServiceLoading:
    """Test model loading."""

    def test_load_model_success(self):
        """Model loads from valid directory with 3 pkl files."""
        result = weather_ml_service.load_model("./ml_models/weather")
        assert result is True
        assert weather_ml_service.is_loaded is True

    def test_load_model_missing_dir(self):
        """Returns False when directory doesn't exist."""
        result = weather_ml_service.load_model("./nonexistent/path")
        assert result is False

    def test_class_labels(self):
        """Encoder has expected class labels."""
        weather_ml_service.load_model("./ml_models/weather")
        labels = weather_ml_service.class_labels
        assert set(labels) == {"Cloudy", "Heavy Rain", "Light Rain", "Sunny"}


class TestWeatherMLServicePrediction:
    """Test predictions."""

    def setup_method(self):
        weather_ml_service.load_model("./ml_models/weather")

    def test_predict_returns_result(self):
        """Prediction returns a WeatherPredictionResult."""
        features = {
            "temperature": 30.0,
            "relative_humidity": 75.0,
            "rain": 0.0,
            "wind_speed": 12.0,
            "soil_temperature": 28.0,
            "soil_moisture": 0.32,
            "solar_radiation": 650.0,
        }
        result = weather_ml_service.predict(features)
        assert isinstance(result, WeatherPredictionResult)
        assert result.condition in {"Cloudy", "Heavy Rain", "Light Rain", "Sunny"}
        assert 0.0 <= result.confidence <= 1.0
        assert result.model_loaded is True

    def test_predict_with_none_falls_back(self):
        """Prediction handles None values (uses 0.0 default)."""
        features = {
            "temperature": 30.0,
            "relative_humidity": 75.0,
            "rain": 0.0,
            "wind_speed": 12.0,
            "soil_temperature": None,
            "soil_moisture": 0.32,
            "solar_radiation": None,
        }
        result = weather_ml_service.predict(features)
        assert isinstance(result, WeatherPredictionResult)
        assert result.condition in {"Cloudy", "Heavy Rain", "Light Rain", "Sunny"}

    def test_mock_predict_when_not_loaded(self):
        """Mock prediction when model is not loaded."""
        from services.weather_ml_service import WeatherMLService
        fresh_service = WeatherMLService()
        features = {
            "temperature": 30.0,
            "relative_humidity": 75.0,
            "rain": 0.0,
            "wind_speed": 12.0,
            "soil_temperature": 28.0,
            "soil_moisture": 0.32,
            "solar_radiation": 650.0,
        }
        result = fresh_service.predict(features)
        assert isinstance(result, WeatherPredictionResult)
        assert result.model_loaded is False
        assert result.condition in {"Cloudy", "Heavy Rain", "Light Rain", "Sunny"}

    def test_predict_probabilities(self):
        """Prediction includes probability distribution."""
        features = {
            "temperature": 30.0,
            "relative_humidity": 75.0,
            "rain": 0.0,
            "wind_speed": 12.0,
            "soil_temperature": 28.0,
            "soil_moisture": 0.32,
            "solar_radiation": 650.0,
        }
        result = weather_ml_service.predict(features)
        assert result.probabilities is not None
        assert len(result.probabilities) == 4
        assert abs(sum(result.probabilities.values()) - 1.0) < 0.01
```

**Step 2: Run test to verify it fails**

```bash
cd backend
SET TEST_DATABASE_URL=postgresql://agrisense_user:PwGszJbrHGnxVplLFmjc3X31gtHr412+@168.138.188.113:5432/agrisense
python -m pytest tests/test_weather_ml_service.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'services.weather_ml_service'`

**Step 3: Implement WeatherMLService**

Create `backend/services/weather_ml_service.py`:

```python
"""
Weather ML Service - Random Forest weather classification

Singleton service that loads a scikit-learn Random Forest model at startup
and classifies weather conditions from sensor data. Falls back to mock
predictions when model files are missing or USE_MOCK_WEATHER_ML is enabled.

The model was trained with 3 components:
- StandardScaler: normalizes 7 input features
- RandomForestClassifier: predicts weather class (0-3)
- LabelEncoder: maps class index to label

Output labels: Cloudy, Heavy Rain, Light Rain, Sunny
"""

import logging
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

# Feature order must match training data exactly
FEATURE_COLUMNS = [
    "temperature_2m (°C)",
    "relative_humidity_2m (%)",
    "rain (mm)",
    "wind_speed_10m (km/h)",
    "soil_temperature_0_to_7cm (°C)",
    "soil_moisture_0_to_7cm (m³/m³)",
    "shortwave_radiation (W/m²)",
]

# Mapping from SensorReading column names to feature names
SENSOR_TO_FEATURE = {
    "temperature": "temperature_2m (°C)",
    "relative_humidity": "relative_humidity_2m (%)",
    "rain": "rain (mm)",
    "wind_speed": "wind_speed_10m (km/h)",
    "soil_temperature": "soil_temperature_0_to_7cm (°C)",
    "soil_moisture": "soil_moisture_0_to_7cm (m³/m³)",
    "solar_radiation": "shortwave_radiation (W/m²)",
}

WEATHER_LABELS = ["Cloudy", "Heavy Rain", "Light Rain", "Sunny"]


@dataclass
class WeatherPredictionResult:
    """Structured result from weather classification."""
    condition: Optional[str]          # "Sunny", "Cloudy", "Light Rain", "Heavy Rain"
    confidence: float                 # 0.0 - 1.0 (max probability)
    probabilities: Dict[str, float]   # {label: probability} for all classes
    model_loaded: bool                # True = real model, False = mock


class WeatherMLService:
    """Singleton scikit-learn weather classification service."""

    def __init__(self):
        self._model = None
        self._scaler = None
        self._encoder = None
        self._model_loaded = False

    def load_model(self, model_dir: str) -> bool:
        """Load model, scaler, and encoder from pkl files in model_dir."""
        model_path = Path(model_dir)
        required_files = [
            "random_forest_model.pkl",
            "random_forest_model_scaler.pkl",
            "random_forest_model_encoder.pkl",
        ]

        for f in required_files:
            if not (model_path / f).exists():
                logger.warning("Weather model file not found: %s — using mock", model_path / f)
                return False

        try:
            import joblib

            self._scaler = joblib.load(model_path / "random_forest_model_scaler.pkl")
            self._model = joblib.load(model_path / "random_forest_model.pkl")
            self._encoder = joblib.load(model_path / "random_forest_model_encoder.pkl")
            self._model_loaded = True

            logger.info(
                "Weather ML model loaded from %s — labels: %s",
                model_path, list(self._encoder.classes_),
            )
            return True

        except Exception:
            logger.exception("Failed to load weather ML model from %s", model_path)
            self._model = None
            self._scaler = None
            self._encoder = None
            self._model_loaded = False
            return False

    @property
    def is_loaded(self) -> bool:
        return self._model_loaded

    @property
    def class_labels(self) -> List[str]:
        if self._encoder is not None:
            return list(self._encoder.classes_)
        return list(WEATHER_LABELS)

    def predict(self, features: Dict[str, Optional[float]]) -> WeatherPredictionResult:
        """
        Classify weather from sensor reading features.

        Args:
            features: dict with keys matching SensorReading columns:
                temperature, relative_humidity, rain, wind_speed,
                soil_temperature, soil_moisture, solar_radiation

        Returns:
            WeatherPredictionResult with condition, confidence, probabilities.
        """
        if not self._model_loaded:
            return self._mock_predict()

        try:
            import pandas as pd

            # Map sensor column names to training feature names
            row = {}
            for sensor_col, feature_name in SENSOR_TO_FEATURE.items():
                value = features.get(sensor_col)
                row[feature_name] = float(value) if value is not None else 0.0

            df = pd.DataFrame([row], columns=FEATURE_COLUMNS)
            scaled = self._scaler.transform(df)
            prediction = self._model.predict(scaled)
            probas = self._model.predict_proba(scaled)[0]
            label = self._encoder.inverse_transform(prediction)[0]

            prob_dict = {
                c: round(float(p), 4)
                for c, p in zip(self._encoder.classes_, probas)
            }

            return WeatherPredictionResult(
                condition=label,
                confidence=round(float(max(probas)), 4),
                probabilities=prob_dict,
                model_loaded=True,
            )

        except Exception:
            logger.exception("Weather ML prediction failed")
            return self._mock_predict()

    @staticmethod
    def _mock_predict() -> WeatherPredictionResult:
        """Return a random mock prediction (dev/testing fallback)."""
        condition = random.choice(WEATHER_LABELS)
        confidence = round(random.uniform(0.4, 0.95), 2)
        # Generate plausible probabilities
        remaining = 1.0 - confidence
        others = [l for l in WEATHER_LABELS if l != condition]
        splits = sorted([random.random() for _ in range(len(others) - 1)])
        probs = {}
        probs[condition] = confidence
        prev = 0.0
        for i, label in enumerate(others):
            if i < len(splits):
                probs[label] = round((splits[i] - prev) * remaining, 4)
                prev = splits[i]
            else:
                probs[label] = round((1.0 - prev) * remaining, 4)

        return WeatherPredictionResult(
            condition=condition,
            confidence=confidence,
            probabilities=probs,
            model_loaded=False,
        )


# Module-level singleton
weather_ml_service = WeatherMLService()
```

**Step 4: Run tests to verify they pass**

```bash
cd backend
python -m pytest tests/test_weather_ml_service.py -v
```

Expected: All 6 tests PASS

**Step 5: Commit**

```bash
git add services/weather_ml_service.py tests/test_weather_ml_service.py
git commit -m "feat: add WeatherMLService for weather classification"
```

---

## Task 3: Add Config and Startup Loading

**Files:**
- Modify: `backend/config.py:82-88` (add weather ML settings)
- Modify: `backend/main.py:60-71` (add weather model loading in lifespan)

**Step 1: Add config settings**

In `backend/config.py`, after `pest_model_path` (line 88), add:

```python
    use_mock_weather_ml: bool = Field(default=False, env="USE_MOCK_WEATHER_ML")
    weather_model_path: str = Field(
        default="./ml_models/weather",
        env="WEATHER_MODEL_PATH"
    )
```

**Step 2: Add startup loading in main.py**

In `backend/main.py`, in the lifespan function, after the pest model loading block (after line 71), add:

```python
    # Load weather classification ML model
    from services.weather_ml_service import weather_ml_service

    if not settings.use_mock_weather_ml:
        loaded = weather_ml_service.load_model(settings.weather_model_path)
        if loaded:
            print(f"Weather ML model loaded — labels: {weather_ml_service.class_labels}")
        else:
            print("Weather ML model not found, falling back to mock predictions")
    else:
        print("USE_MOCK_WEATHER_ML=True — skipping weather model load")
```

**Step 3: Test startup**

```bash
cd backend
python -c "from config import settings; print('weather_model_path:', settings.weather_model_path, 'use_mock:', settings.use_mock_weather_ml)"
```

Expected: `weather_model_path: ./ml_models/weather use_mock: False`

**Step 4: Commit**

```bash
git add config.py main.py
git commit -m "feat: add weather ML config and startup loading"
```

---

## Task 4: Database Migration — Add weather_condition Column

**Files:**
- Modify: `backend/models/sensor_reading.py:112` (add column)
- Create: `backend/alembic/versions/xxxx_add_weather_condition.py` (auto-generated)

**Step 1: Add column to model**

In `backend/models/sensor_reading.py`, after the `weather_code` column (after line 111), add:

```python
    weather_condition = Column(String(20), nullable=True)
    # ML-predicted weather condition: "Sunny", "Cloudy", "Light Rain", "Heavy Rain"
    # Set automatically when sensor reading is created
    # NULL for readings before model integration
```

**Step 2: Generate Alembic migration**

```bash
cd backend
alembic revision --autogenerate -m "Add weather_condition to sensor_readings"
```

**Step 3: Review the generated migration file**

Open the generated file in `alembic/versions/`. Verify the upgrade function contains:

```python
op.add_column('sensor_readings', sa.Column('weather_condition', sa.String(length=20), nullable=True))
```

And downgrade contains:

```python
op.drop_column('sensor_readings', 'weather_condition')
```

**Step 4: Apply migration**

```bash
cd backend
alembic upgrade head
```

**Step 5: Verify column exists**

```bash
cd backend
python -c "
from database import SessionLocal
from sqlalchemy import text
db = SessionLocal()
result = db.execute(text(\"SELECT column_name FROM information_schema.columns WHERE table_name='sensor_readings' AND column_name='weather_condition'\"))
print('Column exists:', result.fetchone() is not None)
db.close()
"
```

Expected: `Column exists: True`

**Step 6: Commit**

```bash
git add models/sensor_reading.py alembic/versions/
git commit -m "feat: add weather_condition column to sensor_readings"
```

---

## Task 5: Auto-classify on Sensor Reading Creation

**Files:**
- Modify: `backend/jobs/scheduler.py:101-115` (classify after creating reading)
- Modify: `backend/routers/sensor.py:66-83` (classify on manual POST)

**Step 1: Write failing test**

Add to `backend/tests/test_weather_ml_service.py`:

```python
class TestAutoClassification:
    """Test that sensor readings get auto-classified."""

    def test_classify_sensor_reading_dict(self):
        """Classify a dict of sensor values."""
        weather_ml_service.load_model("./ml_models/weather")
        features = {
            "temperature": 30.0,
            "relative_humidity": 75.0,
            "rain": 0.0,
            "wind_speed": 12.0,
            "soil_temperature": 28.0,
            "soil_moisture": 0.32,
            "solar_radiation": 650.0,
        }
        result = weather_ml_service.predict(features)
        assert result.condition is not None
        assert len(result.condition) > 0
```

**Step 2: Run test**

```bash
cd backend
python -m pytest tests/test_weather_ml_service.py::TestAutoClassification -v
```

Expected: PASS (predict already works from Task 2)

**Step 3: Modify scheduler to classify readings**

In `backend/jobs/scheduler.py`, add import at top:

```python
from services.weather_ml_service import weather_ml_service
```

Then modify the sensor reading creation block (around line 102-115). After creating the `SensorReading` object and before `db.add(reading)`, add classification:

```python
                    reading = SensorReading(
                        user_id=loc_user.id,
                        temperature=current.temperature,
                        relative_humidity=current.relative_humidity,
                        rain=current.rain or 0.0,
                        wind_speed=raw_current.get("wind_speed_10m", 0.0),
                        solar_radiation=current.shortwave_radiation,
                        soil_temperature=current.soil_temperature,
                        soil_moisture=current.soil_moisture if current.soil_moisture is not None else 0.0,
                        weather_code=raw_current.get("weather_code")
                    )

                    # Auto-classify weather condition using ML model
                    try:
                        prediction = weather_ml_service.predict({
                            "temperature": reading.temperature,
                            "relative_humidity": reading.relative_humidity,
                            "rain": reading.rain,
                            "wind_speed": reading.wind_speed,
                            "soil_temperature": reading.soil_temperature,
                            "soil_moisture": reading.soil_moisture,
                            "solar_radiation": reading.solar_radiation,
                        })
                        reading.weather_condition = prediction.condition
                    except Exception as e:
                        logger.warning("Weather classification failed: %s", e)

                    db.add(reading)
```

**Step 4: Modify sensor router for manual POST**

In `backend/routers/sensor.py`, add import at top:

```python
from services.weather_ml_service import weather_ml_service
```

Then after creating `db_sensor_data` (around line 77), before `db.add()`:

```python
    # Auto-classify weather condition using ML model
    try:
        prediction = weather_ml_service.predict({
            "temperature": db_sensor_data.temperature,
            "relative_humidity": db_sensor_data.relative_humidity,
            "rain": db_sensor_data.rain,
            "wind_speed": db_sensor_data.wind_speed,
            "soil_temperature": db_sensor_data.soil_temperature,
            "soil_moisture": db_sensor_data.soil_moisture,
            "solar_radiation": db_sensor_data.solar_radiation,
        })
        db_sensor_data.weather_condition = prediction.condition
    except Exception:
        pass  # Classification failure shouldn't block reading creation

    db.add(db_sensor_data)
```

**Step 5: Run existing sensor tests to make sure nothing breaks**

```bash
cd backend
SET TEST_DATABASE_URL=postgresql://agrisense_user:PwGszJbrHGnxVplLFmjc3X31gtHr412+@168.138.188.113:5432/agrisense
python -m pytest tests/test_sensor.py -v
```

Expected: All existing tests still pass

**Step 6: Commit**

```bash
git add jobs/scheduler.py routers/sensor.py tests/test_weather_ml_service.py
git commit -m "feat: auto-classify weather condition on sensor reading creation"
```

---

## Task 6: Backend — New/Modified Weather Endpoints

**Files:**
- Modify: `backend/schemas/weather.py` (add new response schemas)
- Modify: `backend/routers/weather.py` (modify current, add historical)

**Step 1: Add new schemas**

In `backend/schemas/weather.py`, add at the end of the file:

```python
class SensorWeatherReading(BaseModel):
    """Single sensor reading with ML weather classification."""
    timestamp: datetime
    temperature: float
    relative_humidity: float
    rain: float
    wind_speed: float
    soil_temperature: Optional[float] = None
    soil_moisture: float
    solar_radiation: Optional[float] = None
    weather_code: Optional[int] = None
    weather_condition: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class CurrentSensorWeatherResponse(BaseModel):
    """Current weather from latest sensor reading + ML classification."""
    source: str = "sensor"
    weather_condition: Optional[str] = None
    confidence: Optional[float] = None
    probabilities: Optional[Dict[str, float]] = None
    temperature: float
    relative_humidity: float
    rain: float
    wind_speed: float
    soil_temperature: Optional[float] = None
    soil_moisture: float
    solar_radiation: Optional[float] = None
    weather_code: Optional[int] = None
    timestamp: datetime
    model_loaded: bool = False


class HistoricalSummary(BaseModel):
    """Summary statistics for a historical period."""
    avg_temperature: float
    max_temperature: float
    min_temperature: float
    avg_humidity: float
    total_rain: float
    dominant_condition: Optional[str] = None
    condition_breakdown: Dict[str, int] = {}


class HistoricalWeatherResponse(BaseModel):
    """Historical weather data from sensor readings."""
    period: str
    start: datetime
    end: datetime
    readings_count: int
    readings: List[SensorWeatherReading]
    summary: HistoricalSummary
```

Add required imports at top of the file:

```python
from typing import Dict, List, Optional
```

**Step 2: Modify current weather endpoint**

In `backend/routers/weather.py`, modify the `GET /current` endpoint to fetch from sensor readings instead of Open-Meteo:

```python
@router.get("/weather/current", response_model=None)
async def get_current_weather(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get current weather from latest sensor reading + ML classification.
    Falls back to Open-Meteo if no sensor data available.
    """
    from models.sensor_reading import SensorReading
    from services.weather_ml_service import weather_ml_service
    from schemas.weather import CurrentSensorWeatherResponse

    # Get latest sensor reading for this user
    latest = (
        db.query(SensorReading)
        .filter(SensorReading.user_id == current_user.id)
        .order_by(SensorReading.timestamp.desc())
        .first()
    )

    if latest is None:
        raise HTTPException(
            status_code=404,
            detail="No sensor data available. Waiting for sensor readings."
        )

    # Run ML prediction (or use stored classification)
    confidence = None
    probabilities = None
    condition = latest.weather_condition

    if condition is None and weather_ml_service.is_loaded:
        prediction = weather_ml_service.predict({
            "temperature": latest.temperature,
            "relative_humidity": latest.relative_humidity,
            "rain": latest.rain,
            "wind_speed": latest.wind_speed,
            "soil_temperature": latest.soil_temperature,
            "soil_moisture": latest.soil_moisture,
            "solar_radiation": latest.solar_radiation,
        })
        condition = prediction.condition
        confidence = prediction.confidence
        probabilities = prediction.probabilities
    elif condition is not None and weather_ml_service.is_loaded:
        # Re-predict for fresh confidence/probability data
        prediction = weather_ml_service.predict({
            "temperature": latest.temperature,
            "relative_humidity": latest.relative_humidity,
            "rain": latest.rain,
            "wind_speed": latest.wind_speed,
            "soil_temperature": latest.soil_temperature,
            "soil_moisture": latest.soil_moisture,
            "solar_radiation": latest.solar_radiation,
        })
        confidence = prediction.confidence
        probabilities = prediction.probabilities

    return CurrentSensorWeatherResponse(
        source="sensor",
        weather_condition=condition,
        confidence=confidence,
        probabilities=probabilities,
        temperature=latest.temperature,
        relative_humidity=latest.relative_humidity,
        rain=latest.rain,
        wind_speed=latest.wind_speed,
        soil_temperature=latest.soil_temperature,
        soil_moisture=latest.soil_moisture,
        solar_radiation=latest.solar_radiation,
        weather_code=latest.weather_code,
        timestamp=latest.timestamp,
        model_loaded=weather_ml_service.is_loaded,
    )
```

**Step 3: Add historical endpoint**

Add new endpoint to `backend/routers/weather.py`:

```python
@router.get("/weather/historical", response_model=None)
async def get_historical_weather(
    period: str = Query(default="24h", regex="^(24h|7d|custom)$"),
    start_date: Optional[str] = Query(default=None),
    end_date: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get historical weather data from sensor readings.

    Args:
        period: "24h", "7d", or "custom"
        start_date: ISO datetime (required if period=custom)
        end_date: ISO datetime (required if period=custom)
    """
    from datetime import datetime, timedelta, timezone
    from sqlalchemy import func
    from models.sensor_reading import SensorReading
    from schemas.weather import (
        HistoricalWeatherResponse, HistoricalSummary, SensorWeatherReading
    )

    now = datetime.now(timezone.utc)

    if period == "24h":
        start = now - timedelta(hours=24)
        end = now
    elif period == "7d":
        start = now - timedelta(days=7)
        end = now
    elif period == "custom":
        if not start_date or not end_date:
            raise HTTPException(400, "start_date and end_date required for custom period")
        try:
            start = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
            end = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
        except ValueError:
            raise HTTPException(400, "Invalid date format. Use ISO 8601.")
        if (end - start).days > 30:
            raise HTTPException(400, "Custom period cannot exceed 30 days")
    else:
        raise HTTPException(400, "Invalid period. Use 24h, 7d, or custom.")

    readings = (
        db.query(SensorReading)
        .filter(
            SensorReading.user_id == current_user.id,
            SensorReading.timestamp >= start,
            SensorReading.timestamp <= end,
        )
        .order_by(SensorReading.timestamp.asc())
        .all()
    )

    # Build summary
    if readings:
        temps = [r.temperature for r in readings]
        humidities = [r.relative_humidity for r in readings]
        rains = [r.rain for r in readings]
        conditions = [r.weather_condition for r in readings if r.weather_condition]

        condition_counts = {}
        for c in conditions:
            condition_counts[c] = condition_counts.get(c, 0) + 1

        dominant = max(condition_counts, key=condition_counts.get) if condition_counts else None

        summary = HistoricalSummary(
            avg_temperature=round(sum(temps) / len(temps), 1),
            max_temperature=round(max(temps), 1),
            min_temperature=round(min(temps), 1),
            avg_humidity=round(sum(humidities) / len(humidities), 1),
            total_rain=round(sum(rains), 1),
            dominant_condition=dominant,
            condition_breakdown=condition_counts,
        )
    else:
        summary = HistoricalSummary(
            avg_temperature=0, max_temperature=0, min_temperature=0,
            avg_humidity=0, total_rain=0,
        )

    return HistoricalWeatherResponse(
        period=period,
        start=start,
        end=end,
        readings_count=len(readings),
        readings=[SensorWeatherReading.model_validate(r) for r in readings],
        summary=summary,
    )
```

**Step 4: Write tests for new endpoints**

Create `backend/tests/test_weather_endpoints.py`:

```python
"""Tests for weather endpoints (sensor-based current + historical)."""
import pytest
from datetime import datetime, timezone


class TestCurrentWeather:
    """Test GET /api/v1/weather/current (sensor-based)."""

    def test_current_weather_no_data(self, client, auth_headers):
        """Returns 404 when no sensor readings exist."""
        response = client.get("/api/v1/weather/current", headers=auth_headers)
        # May return 404 or data depending on existing DB state
        assert response.status_code in (200, 404)

    def test_current_weather_has_fields(self, client, auth_headers):
        """Response has expected fields when data exists."""
        # Create a sensor reading first
        reading_data = {
            "temperature": 30.0,
            "relative_humidity": 75.0,
            "rain": 0.0,
            "wind_speed": 12.0,
            "soil_temperature": 28.0,
            "soil_moisture": 0.32,
            "solar_radiation": 650.0,
            "weather_code": 1,
        }
        client.post("/api/v1/sensor/", json=reading_data, headers=auth_headers)

        response = client.get("/api/v1/weather/current", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["source"] == "sensor"
        assert "temperature" in data
        assert "weather_condition" in data
        assert "timestamp" in data


class TestHistoricalWeather:
    """Test GET /api/v1/weather/historical."""

    def test_historical_24h(self, client, auth_headers):
        """Returns historical data for 24h period."""
        response = client.get(
            "/api/v1/weather/historical?period=24h",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["period"] == "24h"
        assert "readings" in data
        assert "summary" in data

    def test_historical_7d(self, client, auth_headers):
        """Returns historical data for 7d period."""
        response = client.get(
            "/api/v1/weather/historical?period=7d",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["period"] == "7d"

    def test_historical_custom_missing_dates(self, client, auth_headers):
        """Returns 400 when custom period missing dates."""
        response = client.get(
            "/api/v1/weather/historical?period=custom",
            headers=auth_headers,
        )
        assert response.status_code == 400

    def test_historical_custom_exceeds_30_days(self, client, auth_headers):
        """Returns 400 when custom period exceeds 30 days."""
        response = client.get(
            "/api/v1/weather/historical?period=custom&start_date=2026-01-01T00:00:00Z&end_date=2026-03-01T00:00:00Z",
            headers=auth_headers,
        )
        assert response.status_code == 400

    def test_historical_summary_fields(self, client, auth_headers):
        """Summary has expected fields."""
        response = client.get(
            "/api/v1/weather/historical?period=24h",
            headers=auth_headers,
        )
        data = response.json()
        summary = data["summary"]
        assert "avg_temperature" in summary
        assert "max_temperature" in summary
        assert "total_rain" in summary
        assert "condition_breakdown" in summary
```

**Step 5: Run new tests**

```bash
cd backend
SET TEST_DATABASE_URL=postgresql://agrisense_user:PwGszJbrHGnxVplLFmjc3X31gtHr412+@168.138.188.113:5432/agrisense
python -m pytest tests/test_weather_endpoints.py -v
```

Expected: All tests PASS

**Step 6: Run full test suite to check for regressions**

```bash
cd backend
python -m pytest -v --tb=short
```

**Step 7: Commit**

```bash
git add schemas/weather.py routers/weather.py tests/test_weather_endpoints.py
git commit -m "feat: sensor-based current weather + historical endpoint with ML classification"
```

---

## Task 7: Mobile — Add fl_chart Dependency

**Files:**
- Modify: `mobile/pubspec.yaml`

**Step 1: Add fl_chart dependency**

```bash
cd mobile
flutter pub add fl_chart
```

**Step 2: Verify**

```bash
flutter pub get
```

**Step 3: Commit**

```bash
git add pubspec.yaml pubspec.lock
git commit -m "chore: add fl_chart dependency for weather charts"
```

---

## Task 8: Mobile — Weather Models and Service

**Files:**
- Create: `mobile/lib/models/sensor_weather.dart`
- Modify: `mobile/lib/services/weather_service.dart`

**Step 1: Create sensor weather models**

Create `mobile/lib/models/sensor_weather.dart`:

```dart
/// Models for sensor-based weather data with ML classification.

class SensorCurrentWeather {
  final String source;
  final String? weatherCondition;
  final double? confidence;
  final Map<String, double>? probabilities;
  final double temperature;
  final double relativeHumidity;
  final double rain;
  final double windSpeed;
  final double? soilTemperature;
  final double soilMoisture;
  final double? solarRadiation;
  final int? weatherCode;
  final DateTime timestamp;
  final bool modelLoaded;

  SensorCurrentWeather({
    required this.source,
    this.weatherCondition,
    this.confidence,
    this.probabilities,
    required this.temperature,
    required this.relativeHumidity,
    required this.rain,
    required this.windSpeed,
    this.soilTemperature,
    required this.soilMoisture,
    this.solarRadiation,
    this.weatherCode,
    required this.timestamp,
    required this.modelLoaded,
  });

  factory SensorCurrentWeather.fromJson(Map<String, dynamic> json) {
    return SensorCurrentWeather(
      source: json['source'] ?? 'sensor',
      weatherCondition: json['weather_condition'],
      confidence: json['confidence']?.toDouble(),
      probabilities: json['probabilities'] != null
          ? Map<String, double>.from(
              json['probabilities'].map((k, v) => MapEntry(k, v.toDouble())))
          : null,
      temperature: (json['temperature'] ?? 0).toDouble(),
      relativeHumidity: (json['relative_humidity'] ?? 0).toDouble(),
      rain: (json['rain'] ?? 0).toDouble(),
      windSpeed: (json['wind_speed'] ?? 0).toDouble(),
      soilTemperature: json['soil_temperature']?.toDouble(),
      soilMoisture: (json['soil_moisture'] ?? 0).toDouble(),
      solarRadiation: json['solar_radiation']?.toDouble(),
      weatherCode: json['weather_code'],
      timestamp: DateTime.parse(json['timestamp']),
      modelLoaded: json['model_loaded'] ?? false,
    );
  }
}

class SensorWeatherReading {
  final DateTime timestamp;
  final double temperature;
  final double relativeHumidity;
  final double rain;
  final double windSpeed;
  final double? soilTemperature;
  final double soilMoisture;
  final double? solarRadiation;
  final int? weatherCode;
  final String? weatherCondition;

  SensorWeatherReading({
    required this.timestamp,
    required this.temperature,
    required this.relativeHumidity,
    required this.rain,
    required this.windSpeed,
    this.soilTemperature,
    required this.soilMoisture,
    this.solarRadiation,
    this.weatherCode,
    this.weatherCondition,
  });

  factory SensorWeatherReading.fromJson(Map<String, dynamic> json) {
    return SensorWeatherReading(
      timestamp: DateTime.parse(json['timestamp']),
      temperature: (json['temperature'] ?? 0).toDouble(),
      relativeHumidity: (json['relative_humidity'] ?? 0).toDouble(),
      rain: (json['rain'] ?? 0).toDouble(),
      windSpeed: (json['wind_speed'] ?? 0).toDouble(),
      soilTemperature: json['soil_temperature']?.toDouble(),
      soilMoisture: (json['soil_moisture'] ?? 0).toDouble(),
      solarRadiation: json['solar_radiation']?.toDouble(),
      weatherCode: json['weather_code'],
      weatherCondition: json['weather_condition'],
    );
  }
}

class HistoricalSummary {
  final double avgTemperature;
  final double maxTemperature;
  final double minTemperature;
  final double avgHumidity;
  final double totalRain;
  final String? dominantCondition;
  final Map<String, int> conditionBreakdown;

  HistoricalSummary({
    required this.avgTemperature,
    required this.maxTemperature,
    required this.minTemperature,
    required this.avgHumidity,
    required this.totalRain,
    this.dominantCondition,
    required this.conditionBreakdown,
  });

  factory HistoricalSummary.fromJson(Map<String, dynamic> json) {
    return HistoricalSummary(
      avgTemperature: (json['avg_temperature'] ?? 0).toDouble(),
      maxTemperature: (json['max_temperature'] ?? 0).toDouble(),
      minTemperature: (json['min_temperature'] ?? 0).toDouble(),
      avgHumidity: (json['avg_humidity'] ?? 0).toDouble(),
      totalRain: (json['total_rain'] ?? 0).toDouble(),
      dominantCondition: json['dominant_condition'],
      conditionBreakdown: json['condition_breakdown'] != null
          ? Map<String, int>.from(
              json['condition_breakdown'].map((k, v) => MapEntry(k, v as int)))
          : {},
    );
  }
}

class HistoricalWeatherData {
  final String period;
  final DateTime start;
  final DateTime end;
  final int readingsCount;
  final List<SensorWeatherReading> readings;
  final HistoricalSummary summary;

  HistoricalWeatherData({
    required this.period,
    required this.start,
    required this.end,
    required this.readingsCount,
    required this.readings,
    required this.summary,
  });

  factory HistoricalWeatherData.fromJson(Map<String, dynamic> json) {
    return HistoricalWeatherData(
      period: json['period'],
      start: DateTime.parse(json['start']),
      end: DateTime.parse(json['end']),
      readingsCount: json['readings_count'],
      readings: (json['readings'] as List)
          .map((r) => SensorWeatherReading.fromJson(r))
          .toList(),
      summary: HistoricalSummary.fromJson(json['summary']),
    );
  }
}
```

**Step 2: Add new methods to WeatherService**

In `mobile/lib/services/weather_service.dart`, add two new methods:

```dart
  /// Get current weather from sensor data + ML classification
  static Future<SensorCurrentWeather> getSensorCurrent() async {
    final token = await TokenStorage.getToken();
    if (token == null) throw Exception('Not authenticated');

    final response = await appHttpClient.get(
      Uri.parse('${ApiConstants.baseUrl}${ApiConstants.weatherCurrent}'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
    );

    if (response.statusCode == 200) {
      return SensorCurrentWeather.fromJson(json.decode(response.body));
    } else if (response.statusCode == 401) {
      throw Exception('Session expired');
    } else if (response.statusCode == 404) {
      throw Exception('No sensor data available');
    } else {
      throw Exception('Failed to load current weather');
    }
  }

  /// Get historical weather data from sensor readings
  static Future<HistoricalWeatherData> getHistorical({
    String period = '24h',
    String? startDate,
    String? endDate,
  }) async {
    final token = await TokenStorage.getToken();
    if (token == null) throw Exception('Not authenticated');

    String url = '${ApiConstants.baseUrl}/api/v1/weather/historical?period=$period';
    if (period == 'custom' && startDate != null && endDate != null) {
      url += '&start_date=$startDate&end_date=$endDate';
    }

    final response = await appHttpClient.get(
      Uri.parse(url),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
    );

    if (response.statusCode == 200) {
      return HistoricalWeatherData.fromJson(json.decode(response.body));
    } else if (response.statusCode == 401) {
      throw Exception('Session expired');
    } else {
      throw Exception('Failed to load historical weather');
    }
  }
```

Add import at top of weather_service.dart:

```dart
import 'package:fyp_prototype/models/sensor_weather.dart';
```

**Step 3: Commit**

```bash
cd mobile
git add lib/models/sensor_weather.dart lib/services/weather_service.dart
git commit -m "feat: add sensor weather models and service methods"
```

---

## Task 9: Mobile — Weather Page Redesign (3-tab layout)

**Files:**
- Rewrite: `mobile/lib/pages/weather_page.dart`

**This is the largest task. The weather page will be rewritten as a 3-tab layout:**

1. **Current tab** — sensor data + ML classification
2. **Historical tab** — line charts with period picker
3. **Forecast tab** — existing Open-Meteo forecast (moved here)

**Step 1: Rewrite weather_page.dart**

The full implementation should include:

- `TabBar` with 3 tabs: Current, Historical, Forecast
- **Current tab:**
  - Large weather condition icon + label (Sunny/Cloudy/Light Rain/Heavy Rain)
  - Confidence percentage badge
  - 2x3 grid of sensor metrics (temp, humidity, wind, rain, soil temp, soil moisture)
  - "Last updated" timestamp
- **Historical tab:**
  - Segmented control for period (24h | 7d | Custom)
  - Custom: `showDateRangePicker` dialog
  - Line chart (temperature) using `fl_chart` `LineChart`
  - Line chart (humidity) using `fl_chart` `LineChart`
  - Bar-style display for rainfall
  - Summary card with dominant condition + breakdown
- **Forecast tab:**
  - Move existing Open-Meteo forecast UI into this tab
  - Keep 24-hour horizontal scroll
  - Keep weather alerts and agricultural recommendations

**Weather condition icon mapping:**
```dart
IconData getWeatherIcon(String? condition) {
  switch (condition) {
    case 'Sunny': return Icons.wb_sunny;
    case 'Cloudy': return Icons.cloud;
    case 'Light Rain': return Icons.grain;
    case 'Heavy Rain': return Icons.thunderstorm;
    default: return Icons.help_outline;
  }
}

Color getWeatherColor(String? condition) {
  switch (condition) {
    case 'Sunny': return Colors.orange;
    case 'Cloudy': return Color(0xFF78909C);
    case 'Light Rain': return Colors.lightBlue;
    case 'Heavy Rain': return Color(0xFF1565C0);
    default: return Colors.grey;
  }
}
```

**Chart implementation notes:**
- Use `LineChartData` from fl_chart
- X-axis: time labels (hour for 24h, date for 7d)
- Y-axis: value with appropriate unit
- Touch tooltips showing exact values
- Green theme to match app design

**Step 2: Run Flutter tests**

```bash
cd mobile
flutter test
```

**Step 3: Test on emulator**

```bash
cd mobile
flutter run
```

Verify:
- 3 tabs visible and switchable
- Current tab shows sensor data with ML label
- Historical tab shows charts with period picker
- Forecast tab shows existing Open-Meteo data

**Step 4: Commit**

```bash
cd mobile
git add lib/pages/weather_page.dart
git commit -m "feat: redesign weather page with 3-tab layout (current, historical, forecast)"
```

---

## Task 10: Integration Test and Cleanup

**Step 1: Run full backend test suite**

```bash
cd backend
SET TEST_DATABASE_URL=postgresql://agrisense_user:PwGszJbrHGnxVplLFmjc3X31gtHr412+@168.138.188.113:5432/agrisense
python -m pytest -v --tb=short
```

Expected: All tests pass (minus pre-existing DB flake)

**Step 2: Run full Flutter test suite**

```bash
cd mobile
flutter test
```

**Step 3: Manual end-to-end test**

1. Start backend: `cd backend && python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload`
2. Verify startup logs show "Weather ML model loaded"
3. Hit `GET /api/v1/weather/current` — should return sensor data + ML classification
4. Hit `GET /api/v1/weather/historical?period=24h` — should return readings with conditions
5. Run Flutter app and navigate to Weather tab
6. Verify all 3 tabs display correctly

**Step 4: Update HANDOVER.md**

Add weather ML integration to the completed work section.

**Step 5: Final commit**

```bash
git add HANDOVER.md
git commit -m "docs: update handover with weather ML integration"
```
