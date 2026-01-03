"""
Data Simulator for AgriSense
============================

This module generates realistic sensor data for testing and development.

Why We Need This:
-----------------
1. Testing without real hardware sensors
2. Generating historical data for development
3. Demonstrating the system in presentations
4. Simulating various weather conditions

What This Simulates:
-------------------
- Temperature (20-35°C) - Typical agricultural range
- Humidity (40-90%) - Common humidity levels
- Soil Moisture (20-80%) - From dry to well-watered
- Light Intensity (0-100000 lux) - From night to bright sun

Educational Notes:
-----------------
- Real sensors would provide actual readings from hardware
- This simulator uses random values within realistic ranges
- In production, you'd replace this with actual sensor readings
- The ranges are based on typical agricultural conditions

Author: AgriSense Team
Date: January 2025
"""

import random
from datetime import datetime, timedelta
from typing import Dict, Optional


class SensorDataSimulator:
    """
    Simulates realistic sensor data for agricultural monitoring.
    
    This class generates random but realistic values for:
    - Temperature (affected by time of day)
    - Humidity (affected by temperature and time)
    - Soil moisture (gradual changes over time)
    - Light intensity (based on time of day)
    
    Usage Example:
    -------------
    simulator = SensorDataSimulator()
    data = simulator.generate_reading()
    print(data)
    # Output: {'temperature': 28.5, 'humidity': 65.2, ...}
    """
    
    def __init__(
        self,
        base_temperature: float = 27.5,
        base_humidity: float = 65.0,
        base_soil_moisture: float = 50.0
    ):
        """
        Initialize the simulator with base values.
        
        Args:
            base_temperature: Average temperature (°C)
            base_humidity: Average humidity (%)
            base_soil_moisture: Average soil moisture (%)
            
        Educational Note:
        ----------------
        Base values represent the "normal" conditions for your location.
        Actual readings will vary around these base values.
        """
        self.base_temperature = base_temperature
        self.base_humidity = base_humidity
        self.base_soil_moisture = base_soil_moisture
        
        # Track soil moisture over time (it changes gradually)
        self.current_soil_moisture = base_soil_moisture
    
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
            
        Educational Note:
        ----------------
        Real temperature follows a sinusoidal pattern throughout the day.
        We simulate this by adjusting based on the hour.
        """
        if hour is None:
            hour = datetime.now().hour
        
        # Calculate time-based variation (sinusoidal pattern)
        # Coolest at 6 AM (hour 6), warmest at 2 PM (hour 14)
        time_offset = (hour - 6) / 24.0 * 2 * 3.14159  # Convert to radians
        time_variation = 5.0 * (1 - abs(((hour - 14) % 24) / 12.0 - 1))
        
        # Add random fluctuation (±2°C)
        random_variation = random.uniform(-2.0, 2.0)
        
        # Calculate final temperature
        temperature = self.base_temperature + time_variation + random_variation
        
        # Clamp to realistic range (20-35°C)
        temperature = max(20.0, min(35.0, temperature))
        
        # Round to 1 decimal place (sensor precision)
        return round(temperature, 1)
    
    def generate_humidity(self, temperature: float, hour: Optional[int] = None) -> float:
        """
        Generate realistic humidity reading.
        
        Humidity is inversely related to temperature:
        - Higher temperature → Lower humidity (evaporation)
        - Lower temperature → Higher humidity (condensation)
        - Higher in morning/evening (dew)
        
        Args:
            temperature: Current temperature (affects humidity)
            hour: Hour of day (0-23). If None, uses current time.
            
        Returns:
            Humidity percentage (40-90% range)
            
        Educational Note:
        ----------------
        Relative humidity is the amount of water vapor in air relative
        to the maximum it can hold at that temperature.
        Warm air holds more water, so humidity drops as temp rises.
        """
        if hour is None:
            hour = datetime.now().hour
        
        # Temperature effect: Higher temp → Lower humidity
        temp_effect = (30.0 - temperature) * 1.5
        
        # Time effect: Higher humidity in morning (6-9 AM) and evening (6-9 PM)
        if 6 <= hour <= 9 or 18 <= hour <= 21:
            time_effect = 10.0  # Morning/evening dew
        else:
            time_effect = 0.0
        
        # Add random fluctuation (±5%)
        random_variation = random.uniform(-5.0, 5.0)
        
        # Calculate final humidity
        humidity = self.base_humidity + temp_effect + time_effect + random_variation
        
        # Clamp to realistic range (40-90%)
        humidity = max(40.0, min(90.0, humidity))
        
        # Round to 1 decimal place
        return round(humidity, 1)
    
    def generate_soil_moisture(self, hours_since_last_reading: float = 1.0) -> float:
        """
        Generate realistic soil moisture reading.
        
        Soil moisture changes gradually over time:
        - Decreases slowly due to evaporation and plant uptake
        - Increases suddenly when it rains (simulated randomly)
        - Changes much slower than temperature/humidity
        
        Args:
            hours_since_last_reading: Time since last reading (for gradual change)
            
        Returns:
            Soil moisture percentage (20-80% range)
            
        Educational Note:
        ----------------
        Soil moisture is measured as volumetric water content (VWC).
        - 20-30%: Dry soil (irrigation needed)
        - 40-60%: Optimal for most crops
        - 70-80%: Very wet (risk of root rot)
        """
        # Gradual decrease due to evaporation/plant uptake
        # Typical rate: 1-2% per hour during day
        evaporation_rate = random.uniform(0.5, 1.5) * hours_since_last_reading
        self.current_soil_moisture -= evaporation_rate
        
        # Random chance of "rain" (10% chance per reading)
        if random.random() < 0.1:
            rain_increase = random.uniform(10.0, 25.0)
            self.current_soil_moisture += rain_increase
        
        # Clamp to realistic range (20-80%)
        self.current_soil_moisture = max(20.0, min(80.0, self.current_soil_moisture))
        
        # Round to 1 decimal place
        return round(self.current_soil_moisture, 1)
    
    def generate_light_intensity(self, hour: Optional[int] = None) -> int:
        """
        Generate realistic light intensity reading.
        
        Light intensity varies dramatically throughout the day:
        - Night (6 PM - 6 AM): 0-100 lux (moonlight)
        - Dawn/Dusk (5-7 AM, 5-7 PM): 1000-10000 lux
        - Day (8 AM - 5 PM): 30000-100000 lux (full sun)
        
        Args:
            hour: Hour of day (0-23). If None, uses current time.
            
        Returns:
            Light intensity in lux (0-100000 range)
            
        Educational Note:
        ----------------
        Lux is a measure of light intensity (lumens per square meter).
        - 0-50 lux: Dark night
        - 400 lux: Sunrise/sunset
        - 1000 lux: Overcast day
        - 10000-25000 lux: Full daylight
        - 32000-100000 lux: Direct sunlight
        
        Plants need different light levels:
        - Low light plants: 1000-2500 lux
        - Medium light: 2500-10000 lux
        - High light (full sun): 10000+ lux
        """
        if hour is None:
            hour = datetime.now().hour
        
        # Night time (6 PM - 6 AM): Very low light
        if hour >= 18 or hour < 6:
            return random.randint(0, 100)
        
        # Dawn (6-7 AM) or Dusk (5-6 PM): Increasing/decreasing light
        elif hour == 6 or hour == 17:
            return random.randint(1000, 10000)
        
        # Early morning (7-8 AM) or Late afternoon (4-5 PM)
        elif hour == 7 or hour == 16:
            return random.randint(10000, 30000)
        
        # Full daylight (8 AM - 4 PM): High light
        else:
            # Add cloud cover variation (some days are cloudier)
            cloud_factor = random.uniform(0.5, 1.0)  # 50-100% of max light
            max_light = 100000
            return int(max_light * cloud_factor)
    
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
            Dictionary with all sensor values:
            {
                'temperature': 28.5,
                'humidity': 65.2,
                'soil_moisture': 52.3,
                'light_intensity': 45000,
                'timestamp': datetime(2025, 1, 16, 14, 30)
            }
            
        Usage Example:
        -------------
        simulator = SensorDataSimulator()
        
        # Generate current reading
        reading = simulator.generate_reading()
        
        # Generate reading for specific time
        past_time = datetime.now() - timedelta(hours=3)
        reading = simulator.generate_reading(timestamp=past_time)
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        hour = timestamp.hour
        
        # Generate all sensor values
        # Order matters: humidity depends on temperature
        temperature = self.generate_temperature(hour)
        humidity = self.generate_humidity(temperature, hour)
        soil_moisture = self.generate_soil_moisture(hours_since_last)
        light_intensity = self.generate_light_intensity(hour)
        
        return {
            'temperature': temperature,
            'humidity': humidity,
            'soil_moisture': soil_moisture,
            'light_intensity': light_intensity,
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
            
        Usage Example:
        -------------
        simulator = SensorDataSimulator()
        
        # Generate 7 days of hourly data
        historical_data = simulator.generate_historical_data(days=7)
        
        # Insert into database
        for reading in historical_data:
            db_reading = SensorReading(
                user_id=1,
                temperature=reading['temperature'],
                humidity=reading['humidity'],
                soil_moisture=reading['soil_moisture'],
                light_intensity=reading['light_intensity'],
                timestamp=reading['timestamp']
            )
            db.add(db_reading)
        db.commit()
        """
        readings = []
        
        # Calculate time interval between readings
        hours_between = 24.0 / readings_per_day
        
        # Start from N days ago
        start_time = datetime.now() - timedelta(days=days)
        
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
    print("=" * 50)
    
    # Create simulator
    simulator = SensorDataSimulator()
    
    # Generate current reading
    print("\n1. Current Reading:")
    current = simulator.generate_reading()
    print(f"   Temperature: {current['temperature']}°C")
    print(f"   Humidity: {current['humidity']}%")
    print(f"   Soil Moisture: {current['soil_moisture']}%")
    print(f"   Light Intensity: {current['light_intensity']} lux")
    print(f"   Timestamp: {current['timestamp']}")
    
    # Generate readings at different times of day
    print("\n2. Readings Throughout the Day:")
    for hour in [6, 12, 18, 0]:  # 6 AM, Noon, 6 PM, Midnight
        time = datetime.now().replace(hour=hour, minute=0, second=0)
        reading = simulator.generate_reading(timestamp=time)
        print(f"   {hour:02d}:00 - Temp: {reading['temperature']}°C, "
              f"Light: {reading['light_intensity']} lux")
    
    # Generate historical data
    print("\n3. Historical Data (Last 3 Days):")
    historical = simulator.generate_historical_data(days=3, readings_per_day=4)
    print(f"   Generated {len(historical)} readings")
    print(f"   First reading: {historical[0]['timestamp']}")
    print(f"   Last reading: {historical[-1]['timestamp']}")
    
    print("\n" + "=" * 50)
    print("Test complete! Simulator is working correctly.")
