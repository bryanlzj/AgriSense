"""
Export historical weather data from Open-Meteo API for ML model training/testing.

This script fetches raw weather data and exports it to CSV format with:
- Input features: temperature, humidity, pressure, wind, cloud cover, etc.
- Output label: weather_code (WMO code)

Usage:
    python scripts/export_weather_data.py
    python scripts/export_weather_data.py --days 60 --output my_data.csv
    python scripts/export_weather_data.py --lat 3.1390 --lon 101.6869 --days 30
"""

import httpx
import csv
import argparse
from datetime import datetime, timedelta
from pathlib import Path


# Open-Meteo Historical API endpoint
HISTORICAL_API_URL = "https://archive-api.open-meteo.com/v1/archive"

# Default location: Kuala Lumpur, Malaysia
DEFAULT_LAT = 3.1390
DEFAULT_LON = 101.6869


def fetch_historical_weather(
    latitude: float,
    longitude: float,
    start_date: str,
    end_date: str
) -> dict:
    """
    Fetch historical weather data from Open-Meteo Archive API.

    Args:
        latitude: Location latitude
        longitude: Location longitude
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)

    Returns:
        dict: Raw API response with hourly weather data
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation",
            "rain",
            "weather_code",
            "surface_pressure",
            "wind_speed_10m",
            "wind_direction_10m",
            "cloud_cover"
        ],
        "timezone": "auto"
    }

    print(f"Fetching data from {start_date} to {end_date}...")

    with httpx.Client(timeout=60.0) as client:
        response = client.get(HISTORICAL_API_URL, params=params)
        response.raise_for_status()
        return response.json()


def export_to_csv(data: dict, output_path: str) -> int:
    """
    Export weather data to CSV file.

    Args:
        data: Raw API response from Open-Meteo
        output_path: Path to output CSV file

    Returns:
        int: Number of rows exported
    """
    hourly = data.get("hourly", {})

    if not hourly:
        print("No hourly data found in response")
        return 0

    # Get all arrays
    times = hourly.get("time", [])
    temperature = hourly.get("temperature_2m", [])
    humidity = hourly.get("relative_humidity_2m", [])
    apparent_temp = hourly.get("apparent_temperature", [])
    precipitation = hourly.get("precipitation", [])
    rain = hourly.get("rain", [])
    weather_code = hourly.get("weather_code", [])
    pressure = hourly.get("surface_pressure", [])
    wind_speed = hourly.get("wind_speed_10m", [])
    wind_direction = hourly.get("wind_direction_10m", [])
    cloud_cover = hourly.get("cloud_cover", [])

    # CSV headers
    headers = [
        "timestamp",
        "temperature_2m",
        "relative_humidity_2m",
        "apparent_temperature",
        "precipitation",
        "rain",
        "surface_pressure",
        "wind_speed_10m",
        "wind_direction_10m",
        "cloud_cover",
        "weather_code"  # Label (output)
    ]

    rows_written = 0

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for i in range(len(times)):
            # Skip rows with missing weather_code (the label)
            if i >= len(weather_code) or weather_code[i] is None:
                continue

            row = [
                times[i] if i < len(times) else "",
                temperature[i] if i < len(temperature) else "",
                humidity[i] if i < len(humidity) else "",
                apparent_temp[i] if i < len(apparent_temp) else "",
                precipitation[i] if i < len(precipitation) else "",
                rain[i] if i < len(rain) else "",
                pressure[i] if i < len(pressure) else "",
                wind_speed[i] if i < len(wind_speed) else "",
                wind_direction[i] if i < len(wind_direction) else "",
                cloud_cover[i] if i < len(cloud_cover) else "",
                weather_code[i]  # Label
            ]
            writer.writerow(row)
            rows_written += 1

    return rows_written


def main():
    parser = argparse.ArgumentParser(
        description="Export historical weather data from Open-Meteo for ML training"
    )
    parser.add_argument(
        "--lat", type=float, default=DEFAULT_LAT,
        help=f"Latitude (default: {DEFAULT_LAT} - Kuala Lumpur)"
    )
    parser.add_argument(
        "--lon", type=float, default=DEFAULT_LON,
        help=f"Longitude (default: {DEFAULT_LON} - Kuala Lumpur)"
    )
    parser.add_argument(
        "--days", type=int, default=30,
        help="Number of days of historical data (default: 30)"
    )
    parser.add_argument(
        "--output", type=str, default="weather_data.csv",
        help="Output CSV filename (default: weather_data.csv)"
    )

    args = parser.parse_args()

    # Calculate date range (historical data, so end date is yesterday)
    end_date = datetime.now() - timedelta(days=1)
    start_date = end_date - timedelta(days=args.days)

    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")

    print(f"Location: ({args.lat}, {args.lon})")
    print(f"Date range: {start_str} to {end_str}")
    print(f"Output file: {args.output}")
    print()

    try:
        # Fetch data
        data = fetch_historical_weather(
            latitude=args.lat,
            longitude=args.lon,
            start_date=start_str,
            end_date=end_str
        )

        # Export to CSV
        rows = export_to_csv(data, args.output)

        print(f"\nExported {rows} rows to {args.output}")
        print(f"(~{rows} hourly observations over {args.days} days)")

        # Print sample of weather codes found
        hourly = data.get("hourly", {})
        codes = hourly.get("weather_code", [])
        unique_codes = set(c for c in codes if c is not None)
        print(f"\nWeather codes found in data: {sorted(unique_codes)}")

    except httpx.HTTPError as e:
        print(f"Error fetching data: {e}")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
