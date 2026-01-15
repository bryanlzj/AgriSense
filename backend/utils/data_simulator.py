"""
Data Simulator for AgriSense
============================

This module generates realistic sensor data for testing and development.
Fields aligned with Open-Meteo API parameters for ML processing.

Why We Need This:
-----------------
1. Testing without real hardware sensors
2. Generating historical data for development
3. Demonstrating the system in presentations
4. Simulating various weather conditions

What This Simulates (Open-Meteo aligned):
-----------------------------------------
- Temperature (20-35°C) - Air temperature at 2m height
- Relative Humidity (40-90%) - Relative humidity percentage
- Rain (0-50mm) - Rainfall amount
- Wind Speed (0-60 km/h) - Wind speed at 10m height
- Solar Radiation (0-1000 W/m²) - Shortwave radiation (GHI)
- Soil Temperature (20-35°C) - Soil temp at 0-7cm depth
- Soil Moisture (0.1-0.5 m³/m³) - Volumetric soil moisture
- Weather Code (WMO codes) - Weather condition classification

Author: AgriSense Team
Date: January 2025
"""

import random
from datetime import datetime, timedelta
from typing import Dict, Optional


class SensorDataSimulator:
    """
    Simulates realistic sensor data for agricultural monitoring.

    This class generates random but realistic values aligned with
    Open-Meteo API parameters for:
    - Temperature (affected by time of day)
    - Relative humidity (affected by temperature and time)
    - Rain (probabilistic, affected by weather conditions)
    - Wind speed (variable throughout day)
    - Solar radiation (based on time of day)
    - Soil temperature (more stable than air temp)
    - Soil moisture (gradual changes over time)
    - Weather code (WMO standard codes)

    Usage Example:
    -------------
    simulator = SensorDataSimulator()
    data = simulator.generate_reading()
    print(data)
    """

    # WMO Weather Codes for simulation (simplified for Malaysian agriculture)
    # Only includes: 0, 1, 2, 3, 51, 53, 55, 61, 63, 65
    WMO_CODES = {
        'clear': [0, 1],           # Clear sky, Mainly clear
        'cloudy': [2, 3],          # Partly cloudy, Overcast
        'drizzle': [51, 53, 55],   # Light, Moderate, Dense drizzle
        'rain': [61, 63, 65],      # Slight, Moderate, Heavy rain
    }

    def __init__(
        self,
        base_temperature: float = 27.5,
        base_humidity: float = 65.0,
        base_soil_moisture: float = 0.35
    ):
        """
        Initialize the simulator with base values.

        Args:
            base_temperature: Average temperature (°C)
            base_humidity: Average relative humidity (%)
            base_soil_moisture: Average soil moisture (m³/m³)

        Educational Note:
        ----------------
        Base values represent the "normal" conditions for Malaysian climate.
        Actual readings will vary around these base values.
        """
        self.base_temperature = base_temperature
        self.base_humidity = base_humidity
        self.base_soil_moisture = base_soil_moisture

        # Track soil moisture over time (it changes gradually)
        self.current_soil_moisture = base_soil_moisture

        # Current weather state (for consistency between readings)
        self.current_weather_state = 'cloudy'

    def generate_temperature(self, hour: Optional[int] = None) -> float:
        """
        Generate realistic temperature reading.

        Temperature varies throughout the day:
        - Coolest around 6 AM (sunrise)
        - Warmest around 2 PM (afternoon)
        - Gradual cooling in evening

        Args:
            hour: Hour of day (0-23). If None, uses current time.

        Returns:
            Temperature in Celsius (20-35°C range)
        """
        if hour is None:
            hour = datetime.now().hour

        # Calculate time-based variation
        # Coolest at 6 AM (hour 6), warmest at 2 PM (hour 14)
        time_variation = 5.0 * (1 - abs(((hour - 14) % 24) / 12.0 - 1))

        # Add random fluctuation (±2°C)
        random_variation = random.uniform(-2.0, 2.0)

        # Calculate final temperature
        temperature = self.base_temperature + time_variation + random_variation

        # Clamp to realistic range (20-35°C)
        temperature = max(20.0, min(35.0, temperature))

        return round(temperature, 1)

    def generate_relative_humidity(self, temperature: float, hour: Optional[int] = None) -> float:
        """
        Generate realistic relative humidity reading.

        Humidity is inversely related to temperature:
        - Higher temperature → Lower humidity (evaporation)
        - Lower temperature → Higher humidity (condensation)
        - Higher in morning/evening (dew)

        Args:
            temperature: Current temperature (affects humidity)
            hour: Hour of day (0-23). If None, uses current time.

        Returns:
            Relative humidity percentage (40-90% range)
        """
        if hour is None:
            hour = datetime.now().hour

        # Temperature effect: Higher temp → Lower humidity
        temp_effect = (30.0 - temperature) * 1.5

        # Time effect: Higher humidity in morning (6-9 AM) and evening (6-9 PM)
        if 6 <= hour <= 9 or 18 <= hour <= 21:
            time_effect = 10.0
        else:
            time_effect = 0.0

        # Add random fluctuation (±5%)
        random_variation = random.uniform(-5.0, 5.0)

        # Calculate final humidity
        humidity = self.base_humidity + temp_effect + time_effect + random_variation

        # Clamp to realistic range (40-90%)
        humidity = max(40.0, min(90.0, humidity))

        return round(humidity, 1)

    def generate_rain(self) -> float:
        """
        Generate realistic rainfall reading.

        Rain is probabilistic based on weather state.

        Returns:
            Rainfall in mm (0-50 range)
        """
        # Probability of rain based on weather state
        if self.current_weather_state == 'rain':
            # Currently raining
            rain = random.uniform(0.5, 20.0)
        elif self.current_weather_state == 'drizzle':
            rain = random.uniform(0.1, 2.0)
        else:
            # No rain (clear or cloudy)
            rain = 0.0

        return round(rain, 1)

    def generate_wind_speed(self, hour: Optional[int] = None) -> float:
        """
        Generate realistic wind speed reading.

        Wind is generally stronger during daytime.

        Args:
            hour: Hour of day (0-23). If None, uses current time.

        Returns:
            Wind speed in km/h (0-60 range)
        """
        if hour is None:
            hour = datetime.now().hour

        # Base wind speed varies by time
        if 10 <= hour <= 16:
            base_wind = random.uniform(10.0, 25.0)  # Stronger during day
        else:
            base_wind = random.uniform(5.0, 15.0)  # Lighter at night

        # Add variation for rainy weather
        if self.current_weather_state == 'rain':
            base_wind += random.uniform(5.0, 15.0)

        # Clamp to realistic range
        wind_speed = max(0.0, min(50.0, base_wind))

        return round(wind_speed, 1)

    def generate_solar_radiation(self, hour: Optional[int] = None) -> float:
        """
        Generate realistic solar radiation (GHI) reading.

        Solar radiation follows the sun's path:
        - Zero at night
        - Peak around noon
        - Reduced by cloud cover

        Args:
            hour: Hour of day (0-23). If None, uses current time.

        Returns:
            Solar radiation in W/m² (0-1000 range)
        """
        if hour is None:
            hour = datetime.now().hour

        # Night time (6 PM - 6 AM): No solar radiation
        if hour >= 18 or hour < 6:
            return 0.0

        # Calculate solar angle factor (peak at noon)
        # This creates a bell curve peaking at hour 12
        solar_angle = 1 - abs((hour - 12) / 6.0)
        solar_angle = max(0, solar_angle)

        # Base radiation at peak
        max_radiation = 1000.0

        # Cloud cover reduction based on weather state
        cloud_factor = 1.0
        if self.current_weather_state == 'clear':
            cloud_factor = random.uniform(0.9, 1.0)
        elif self.current_weather_state == 'cloudy':
            cloud_factor = random.uniform(0.5, 0.8)
        elif self.current_weather_state == 'drizzle':
            cloud_factor = random.uniform(0.2, 0.4)
        elif self.current_weather_state == 'rain':
            cloud_factor = random.uniform(0.1, 0.3)

        # Calculate final radiation
        radiation = max_radiation * solar_angle * cloud_factor

        return round(radiation, 1)

    def generate_soil_temperature(self, air_temperature: float) -> float:
        """
        Generate realistic soil temperature reading.

        Soil temperature is more stable than air temperature,
        typically lagging and dampening air temp changes.

        Args:
            air_temperature: Current air temperature (affects soil temp)

        Returns:
            Soil temperature in Celsius (20-35°C range)
        """
        # Soil temp is damped version of air temp (less variation)
        # Typically 2-5°C lower than air temp during hot days
        soil_temp = air_temperature - random.uniform(1.0, 4.0)

        # Add small random variation
        soil_temp += random.uniform(-1.0, 1.0)

        # Clamp to realistic range
        soil_temp = max(20.0, min(35.0, soil_temp))

        return round(soil_temp, 1)

    def generate_soil_moisture(self, hours_since_last_reading: float = 1.0) -> float:
        """
        Generate realistic soil moisture reading.

        Soil moisture changes gradually over time:
        - Decreases slowly due to evaporation and plant uptake
        - Increases when it rains
        - Uses volumetric units (m³/m³)

        Args:
            hours_since_last_reading: Time since last reading (for gradual change)

        Returns:
            Volumetric soil moisture (0.1-0.5 m³/m³ range)
        """
        # Gradual decrease due to evaporation/plant uptake
        # Typical rate: 0.005-0.015 m³/m³ per hour during day
        evaporation_rate = random.uniform(0.005, 0.015) * hours_since_last_reading
        self.current_soil_moisture -= evaporation_rate

        # Increase if raining
        if self.current_weather_state == 'rain':
            rain_increase = random.uniform(0.02, 0.08)
            self.current_soil_moisture += rain_increase
        elif self.current_weather_state == 'drizzle':
            rain_increase = random.uniform(0.005, 0.02)
            self.current_soil_moisture += rain_increase

        # Clamp to realistic range (0.1-0.5 m³/m³)
        self.current_soil_moisture = max(0.1, min(0.5, self.current_soil_moisture))

        return round(self.current_soil_moisture, 4)

    def generate_weather_code(self) -> int:
        """
        Generate WMO weather code and update weather state.

        Weather states transition probabilistically.

        Returns:
            WMO weather interpretation code (0-99)
        """
        # Transition probabilities (simplified for Malaysian weather)
        transitions = {
            'clear': {'clear': 0.6, 'cloudy': 0.3, 'drizzle': 0.1},
            'cloudy': {'clear': 0.2, 'cloudy': 0.5, 'drizzle': 0.2, 'rain': 0.1},
            'drizzle': {'cloudy': 0.3, 'drizzle': 0.4, 'rain': 0.3},
            'rain': {'cloudy': 0.3, 'drizzle': 0.3, 'rain': 0.4},
        }

        # Get transition probabilities for current state
        probs = transitions.get(self.current_weather_state, transitions['cloudy'])

        # Random transition
        rand = random.random()
        cumulative = 0
        for state, prob in probs.items():
            cumulative += prob
            if rand <= cumulative:
                self.current_weather_state = state
                break

        # Select random code from current weather state
        codes = self.WMO_CODES.get(self.current_weather_state, [1])
        return random.choice(codes)

    def generate_reading(
        self,
        timestamp: Optional[datetime] = None,
        hours_since_last: float = 1.0
    ) -> Dict[str, any]:
        """
        Generate a complete sensor reading with all values.

        This is the main method you'll use to get simulated data.

        Args:
            timestamp: Time of reading. If None, uses current time.
            hours_since_last: Hours since last reading (for soil moisture)

        Returns:
            Dictionary with all sensor values aligned with Open-Meteo:
            {
                'temperature': 28.5,
                'relative_humidity': 65.2,
                'rain': 0.0,
                'wind_speed': 12.5,
                'solar_radiation': 650.0,
                'soil_temperature': 26.0,
                'soil_moisture': 0.35,
                'weather_code': 1,
                'timestamp': datetime(2025, 1, 16, 14, 30)
            }
        """
        if timestamp is None:
            timestamp = datetime.now()

        hour = timestamp.hour

        # Generate weather code first (affects other values)
        weather_code = self.generate_weather_code()

        # Generate all sensor values
        # Order matters: some values depend on others
        temperature = self.generate_temperature(hour)
        relative_humidity = self.generate_relative_humidity(temperature, hour)
        rain = self.generate_rain()
        wind_speed = self.generate_wind_speed(hour)
        solar_radiation = self.generate_solar_radiation(hour)
        soil_temperature = self.generate_soil_temperature(temperature)
        soil_moisture = self.generate_soil_moisture(hours_since_last)

        return {
            'temperature': temperature,
            'relative_humidity': relative_humidity,
            'rain': rain,
            'wind_speed': wind_speed,
            'solar_radiation': solar_radiation,
            'soil_temperature': soil_temperature,
            'soil_moisture': soil_moisture,
            'weather_code': weather_code,
            'timestamp': timestamp
        }

    def generate_historical_data(
        self,
        days: int = 7,
        readings_per_day: int = 24
    ) -> list[Dict[str, any]]:
        """
        Generate historical sensor data for testing.

        This is useful for:
        - Populating database with test data
        - Testing time-series analysis
        - Demonstrating trends in the UI

        Args:
            days: Number of days of historical data
            readings_per_day: How many readings per day (default: 24 = hourly)

        Returns:
            List of sensor readings, oldest first
        """
        readings = []

        # Calculate time interval between readings
        hours_between = 24.0 / readings_per_day

        # Start from N days ago
        start_time = datetime.now() - timedelta(days=days)

        # Reset soil moisture for historical generation
        self.current_soil_moisture = self.base_soil_moisture

        # Generate readings
        total_readings = days * readings_per_day
        for i in range(total_readings):
            timestamp = start_time + timedelta(hours=i * hours_between)
            reading = self.generate_reading(timestamp, hours_between)
            readings.append(reading)

        return readings


# Convenience function for quick testing
def generate_sample_reading() -> Dict[str, any]:
    """
    Quick function to generate a single sample reading.

    Usage:
    -----
    from utils.data_simulator import generate_sample_reading

    reading = generate_sample_reading()
    print(reading)
    """
    simulator = SensorDataSimulator()
    return simulator.generate_reading()


# Example usage (for testing this module)
if __name__ == "__main__":
    print("AgriSense Data Simulator - Test Run")
    print("=" * 60)

    # Create simulator
    simulator = SensorDataSimulator()

    # Generate current reading
    print("\n1. Current Reading (Open-Meteo aligned fields):")
    current = simulator.generate_reading()
    print(f"   Temperature: {current['temperature']}°C")
    print(f"   Relative Humidity: {current['relative_humidity']}%")
    print(f"   Rain: {current['rain']} mm")
    print(f"   Wind Speed: {current['wind_speed']} km/h")
    print(f"   Solar Radiation: {current['solar_radiation']} W/m²")
    print(f"   Soil Temperature: {current['soil_temperature']}°C")
    print(f"   Soil Moisture: {current['soil_moisture']} m³/m³")
    print(f"   Weather Code: {current['weather_code']}")
    print(f"   Timestamp: {current['timestamp']}")

    # Generate readings at different times of day
    print("\n2. Readings Throughout the Day:")
    for hour in [6, 12, 18, 0]:
        time = datetime.now().replace(hour=hour, minute=0, second=0)
        reading = simulator.generate_reading(timestamp=time)
        print(f"   {hour:02d}:00 - Temp: {reading['temperature']}°C, "
              f"Solar: {reading['solar_radiation']} W/m², "
              f"Rain: {reading['rain']} mm")

    # Generate historical data
    print("\n3. Historical Data (Last 3 Days):")
    historical = simulator.generate_historical_data(days=3, readings_per_day=4)
    print(f"   Generated {len(historical)} readings")
    print(f"   First reading: {historical[0]['timestamp']}")
    print(f"   Last reading: {historical[-1]['timestamp']}")

    print("\n" + "=" * 60)
    print("Test complete! Simulator is working correctly.")
