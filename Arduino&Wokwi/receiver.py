import paho.mqtt.client as mqtt
import json
import ssl
import requests

# ── MQTT Configuration ──
MQTT_BROKER = "broker.emqx.io"
MQTT_PORT = 8883
MQTT_TOPIC = "agrisense/fyp/peng/data/unique_99"

# ── Backend API Configuration ──
API_BASE_URL = "https://agrisense.bryanlzj.work"
API_SENSOR_ENDPOINT = f"{API_BASE_URL}/api/v1/sensor/"

# Paste your JWT token here (login to the app first, then copy the token)
AUTH_TOKEN = "YOUR_TOKEN_HERE"


def map_wokwi_to_backend(data):
    """Map Wokwi sensor fields to backend API schema."""
    return {
        "temperature": data.get("temp_env", 0),
        "relative_humidity": data.get("humidity", 0),
        "rain": data.get("rain_mm", 0),
        "wind_speed": data.get("wind_speed", 0),
        "solar_radiation": data.get("solar", None),
        "soil_temperature": data.get("soil_temp", None),
        "soil_moisture": data.get("soil_moist", 0) / 100.0,  # Convert % to volumetric (0-1.0)
    }


def send_to_backend(sensor_data):
    """POST sensor data to the AgriSense backend API."""
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json",
    }
    try:
        response = requests.post(API_SENSOR_ENDPOINT, json=sensor_data, headers=headers)
        if response.status_code == 200 or response.status_code == 201:
            print(f"  -> Sent to backend successfully!")
        else:
            print(f"  -> Backend error {response.status_code}: {response.text}")
    except requests.exceptions.ConnectionError:
        print(f"  -> Could not connect to backend at {API_BASE_URL}")
    except Exception as e:
        print(f"  -> Failed to send: {e}")


def on_message(client, userdata, message):
    try:
        payload = message.payload.decode("utf-8")
        data = json.loads(payload)

        # Display received data
        print("\n--- [ WOKWI DATA RECEIVED ] ---")
        print(f"  Env Temp:   {data['temp_env']}°C")
        print(f"  Humidity:   {data['humidity']}%")
        print(f"  Soil Moist: {data['soil_moist']}%")
        print(f"  Soil Temp:  {data['soil_temp']}°C")
        print(f"  Solar Rad:  {data['solar']} W/m²")
        print(f"  Wind Speed: {data['wind_speed']} km/h")
        print(f"  Rainfall:   {data['rain_mm']} mm")
        print(f"  Raining:    {'YES' if data.get('raining', False) else 'No'}")
        print("---------------------------------")

        # Map and forward to backend
        sensor_data = map_wokwi_to_backend(data)
        print(f"  Mapped payload: {json.dumps(sensor_data, indent=2)}")
        send_to_backend(sensor_data)

    except Exception as e:
        print(f"Error parsing data: {e}")


def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        print(f"Connected to {MQTT_BROKER} (secure)")
        client.subscribe(MQTT_TOPIC)
        print(f"Subscribed to: {MQTT_TOPIC}")
        print("Waiting for Wokwi data...\n")
    else:
        print(f"Connection failed with code {rc}")


# Setup MQTT client with TLS
client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.tls_set(cert_reqs=ssl.CERT_NONE)
client.on_message = on_message
client.on_connect = on_connect

print("=" * 40)
print("  AgriSense IoT Bridge")
print("  Wokwi -> MQTT -> Backend API")
print("=" * 40)
print(f"Broker:   {MQTT_BROKER}:{MQTT_PORT}")
print(f"Topic:    {MQTT_TOPIC}")
print(f"Backend:  {API_SENSOR_ENDPOINT}")
print()

try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()
except Exception as e:
    print(f"FATAL ERROR: {e}")
    print("\n[HINT] Your network may be blocking encrypted traffic. Try a Mobile Hotspot.")
    exit()
