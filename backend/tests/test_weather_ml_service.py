"""Tests for WeatherMLService."""

import os
from pathlib import Path

import pytest

from services.weather_ml_service import (
    FEATURE_COLUMNS,
    WeatherMLService,
    WeatherPredictionResult,
)

# Resolve the weather model directory relative to this file
MODEL_DIR = str(Path(__file__).resolve().parent.parent / "ml_models" / "weather")


class TestWeatherModelLoading:
    """Tests for model loading behaviour."""

    def test_load_model_success(self):
        """Model loads successfully from the real pkl files."""
        svc = WeatherMLService()
        result = svc.load_model(MODEL_DIR)
        assert result is True
        assert svc.is_loaded is True

    def test_load_model_missing_directory(self):
        """Returns False when directory does not exist."""
        svc = WeatherMLService()
        result = svc.load_model("/nonexistent/path/to/models")
        assert result is False
        assert svc.is_loaded is False

    def test_load_model_missing_file(self, tmp_path):
        """Returns False when a required pkl file is missing."""
        svc = WeatherMLService()
        result = svc.load_model(str(tmp_path))  # empty dir
        assert result is False
        assert svc.is_loaded is False

    def test_not_loaded_initially(self):
        """Service starts in unloaded state."""
        svc = WeatherMLService()
        assert svc.is_loaded is False


class TestClassLabels:
    """Tests for the class_labels property."""

    def test_class_labels_after_load(self):
        svc = WeatherMLService()
        svc.load_model(MODEL_DIR)
        labels = svc.class_labels
        assert isinstance(labels, list)
        assert len(labels) == 4
        assert set(labels) == {"Cloudy", "Heavy Rain", "Light Rain", "Sunny"}

    def test_class_labels_before_load(self):
        svc = WeatherMLService()
        assert svc.class_labels == []


class TestPrediction:
    """Tests for the predict method with real model."""

    @pytest.fixture(autouse=True)
    def _load_model(self):
        self.svc = WeatherMLService()
        loaded = self.svc.load_model(MODEL_DIR)
        if not loaded:
            pytest.skip("Weather model files not available")

    def _sample_features(self) -> dict:
        return {
            "temperature": 30.0,
            "relative_humidity": 75.0,
            "rain": 0.0,
            "wind_speed": 12.0,
            "soil_temperature": 28.0,
            "soil_moisture": 0.3,
            "solar_radiation": 450.0,
        }

    def test_predict_returns_valid_result(self):
        result = self.svc.predict(self._sample_features())
        assert isinstance(result, WeatherPredictionResult)
        assert result.model_loaded is True
        assert result.condition in {"Cloudy", "Heavy Rain", "Light Rain", "Sunny"}
        assert 0.0 <= result.confidence <= 1.0

    def test_predict_probabilities_sum_to_one(self):
        result = self.svc.predict(self._sample_features())
        total = sum(result.probabilities.values())
        assert abs(total - 1.0) < 1e-3, f"Probabilities sum to {total}, expected ~1.0"

    def test_predict_probabilities_keys_match_labels(self):
        result = self.svc.predict(self._sample_features())
        assert set(result.probabilities.keys()) == set(self.svc.class_labels)

    def test_predict_with_none_values(self):
        """None feature values should be treated as 0.0 and not crash."""
        features = {
            "temperature": None,
            "relative_humidity": None,
            "rain": None,
            "wind_speed": None,
            "soil_temperature": None,
            "soil_moisture": None,
            "solar_radiation": None,
        }
        result = self.svc.predict(features)
        assert isinstance(result, WeatherPredictionResult)
        assert result.model_loaded is True
        assert result.condition in {"Cloudy", "Heavy Rain", "Light Rain", "Sunny"}

    def test_predict_with_partial_none_values(self):
        """Mix of real and None values should work fine."""
        features = {
            "temperature": 25.0,
            "relative_humidity": None,
            "rain": 5.0,
            "wind_speed": None,
            "soil_temperature": 22.0,
            "soil_moisture": 0.4,
            "solar_radiation": None,
        }
        result = self.svc.predict(features)
        assert isinstance(result, WeatherPredictionResult)
        assert result.model_loaded is True

    def test_predict_with_empty_dict(self):
        """Empty features dict should default all to 0.0."""
        result = self.svc.predict({})
        assert isinstance(result, WeatherPredictionResult)
        assert result.model_loaded is True


class TestMockPrediction:
    """Tests for mock fallback when model is not loaded."""

    def test_mock_predict_when_not_loaded(self):
        svc = WeatherMLService()
        result = svc.predict({"temperature": 25.0})
        assert isinstance(result, WeatherPredictionResult)
        assert result.model_loaded is False
        assert result.condition in {"Sunny", "Cloudy", "Light Rain", "Heavy Rain"}
        assert 0.0 <= result.confidence <= 1.0

    def test_mock_predict_probabilities_sum_to_one(self):
        svc = WeatherMLService()
        result = svc.predict({})
        total = sum(result.probabilities.values())
        assert abs(total - 1.0) < 0.02, f"Mock probabilities sum to {total}, expected ~1.0"

    def test_mock_predict_static_method(self):
        result = WeatherMLService._mock_predict()
        assert isinstance(result, WeatherPredictionResult)
        assert result.model_loaded is False


class TestFeatureColumns:
    """Verify the feature column constants are correct."""

    def test_feature_columns_count(self):
        assert len(FEATURE_COLUMNS) == 7

    def test_feature_columns_content(self):
        expected = [
            "temperature_2m (°C)",
            "relative_humidity_2m (%)",
            "rain (mm)",
            "wind_speed_10m (km/h)",
            "soil_temperature_0_to_7cm (°C)",
            "soil_moisture_0_to_7cm (m³/m³)",
            "shortwave_radiation (W/m²)",
        ]
        assert FEATURE_COLUMNS == expected
