"""
Weather ML Service - RandomForest-based weather condition prediction

Singleton service that loads a scikit-learn RandomForestClassifier at startup
and provides inference for weather prediction endpoints. Falls back to mock
predictions when the model files are missing or fail to load.

The model expects 7 features (StandardScaler → RandomForest → LabelEncoder decode):
  temperature_2m, relative_humidity_2m, rain, wind_speed_10m,
  soil_temperature_0_to_7cm, soil_moisture_0_to_7cm, shortwave_radiation
"""

import logging
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

# Mapping from sensor reading column names → training feature names
_FEATURE_MAP = {
    "temperature": "temperature_2m (°C)",
    "relative_humidity": "relative_humidity_2m (%)",
    "rain": "rain (mm)",
    "wind_speed": "wind_speed_10m (km/h)",
    "soil_temperature": "soil_temperature_0_to_7cm (°C)",
    "soil_moisture": "soil_moisture_0_to_7cm (m³/m³)",
    "solar_radiation": "shortwave_radiation (W/m²)",
}

# Ordered list of training feature names (must match scaler column order)
FEATURE_COLUMNS = list(_FEATURE_MAP.values())


@dataclass
class WeatherPredictionResult:
    """Structured result from weather inference."""
    condition: str                          # Predicted weather condition label
    confidence: float                       # Probability of predicted class (0.0–1.0)
    probabilities: Dict[str, float] = field(default_factory=dict)  # class → prob
    model_loaded: bool = False              # True = real model, False = mock


class WeatherMLService:
    """Singleton scikit-learn weather prediction service."""

    def __init__(self):
        self._model = None
        self._scaler = None
        self._encoder = None
        self._model_loaded = False

    # ------------------------------------------------------------------
    # Model lifecycle
    # ------------------------------------------------------------------

    def load_model(self, model_dir: str) -> bool:
        """Load the 3 pkl files (model, scaler, encoder) from *model_dir*. Returns True on success."""
        dirpath = Path(model_dir)
        if not dirpath.is_dir():
            logger.warning("Weather model directory not found at %s - using mock predictions", dirpath)
            return False

        model_path = dirpath / "random_forest_model.pkl"
        scaler_path = dirpath / "random_forest_model_scaler.pkl"
        encoder_path = dirpath / "random_forest_model_encoder.pkl"

        for p in (model_path, scaler_path, encoder_path):
            if not p.exists():
                logger.warning("Weather model file missing: %s - using mock predictions", p)
                return False

        try:
            import joblib

            self._model = joblib.load(str(model_path))
            self._scaler = joblib.load(str(scaler_path))
            self._encoder = joblib.load(str(encoder_path))
            self._model_loaded = True

            logger.info(
                "Weather ML model loaded from %s - classes: %s",
                dirpath,
                list(self._encoder.classes_),
            )
            return True
        except Exception:
            logger.exception("Failed to load weather ML model from %s", dirpath)
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
        """Return the list of class labels the model can predict."""
        if self._encoder is not None:
            return list(self._encoder.classes_)
        return []

    # ------------------------------------------------------------------
    # Inference
    # ------------------------------------------------------------------

    def predict(self, features: Dict[str, Optional[float]]) -> WeatherPredictionResult:
        """
        Predict weather condition from sensor features.

        Args:
            features: Dict with sensor column names as keys:
                temperature, relative_humidity, rain, wind_speed,
                soil_temperature, soil_moisture, solar_radiation.
                None values are replaced with 0.0.

        Returns:
            WeatherPredictionResult with condition, confidence, and per-class probabilities.
        """
        if not self._model_loaded or self._model is None:
            return self._mock_predict()

        try:
            # Build feature vector in training column order, defaulting None → 0.0
            values = []
            for sensor_col, train_col in _FEATURE_MAP.items():
                val = features.get(sensor_col)
                values.append(float(val) if val is not None else 0.0)

            # Use DataFrame so scaler sees correct column names (avoids sklearn warnings)
            df = pd.DataFrame([values], columns=FEATURE_COLUMNS)

            scaled = self._scaler.transform(df)
            proba = self._model.predict_proba(scaled)[0]
            pred_idx = int(np.argmax(proba))
            pred_label = self._encoder.inverse_transform([pred_idx])[0]

            probabilities = {
                label: round(float(p), 4)
                for label, p in zip(self._encoder.classes_, proba)
            }

            return WeatherPredictionResult(
                condition=pred_label,
                confidence=round(float(proba[pred_idx]), 4),
                probabilities=probabilities,
                model_loaded=True,
            )

        except Exception:
            logger.exception("Weather ML inference failed")
            return self._mock_predict()

    # ------------------------------------------------------------------
    # Mock fallback
    # ------------------------------------------------------------------

    @staticmethod
    def _mock_predict() -> WeatherPredictionResult:
        """Return a random mock prediction (dev/testing fallback)."""
        conditions = ["Sunny", "Cloudy", "Light Rain", "Heavy Rain"]
        condition = random.choice(conditions)
        confidence = round(random.uniform(0.4, 0.95), 2)

        # Build mock probabilities that sum to 1.0
        remaining = round(1.0 - confidence, 4)
        others = [c for c in conditions if c != condition]
        splits = sorted([random.random() for _ in range(len(others) - 1)])
        fractions = (
            [splits[0]]
            + [splits[i + 1] - splits[i] for i in range(len(splits) - 1)]
            + [1.0 - splits[-1]]
        )
        probabilities = {condition: confidence}
        for c, f in zip(others, fractions):
            probabilities[c] = round(remaining * f, 4)

        return WeatherPredictionResult(
            condition=condition,
            confidence=confidence,
            probabilities=probabilities,
            model_loaded=False,
        )


# Module-level singleton
weather_ml_service = WeatherMLService()
