import paho.mqtt.client as mqtt
import json
import ssl

# Secure Configuration (Port 8883)
MQTT_BROKER = "broker.emqx.io"
MQTT_PORT = 8883
MQTT_TOPIC = "agrisense/fyp/peng/data/unique_99"

def on_message(client, userdata, message):
    try:
        payload = message.payload.decode("utf-8")
        print(f"[DEBUG] Raw Payload Received: {payload}")
        data = json.loads(payload)
        print(f"[DEBUG] Parsed JSON: {data}")

        print("\n--- [ SECURE DATA RECEIVED ] ---")
        print(f"Env Temp:   {data['temp_env']}°C")
        print(f"Humidity:   {data['humidity']}%")
        print(f"Soil Moist: {data['soil_moist']}%")
        print(f"Soil Temp:  {data['soil_temp']}°C")
        print(f"Solar Rad:  {data['solar']} W/m²")
        print(f"Wind Speed: {data['wind_speed']} km/h")
        print(f"Rainfall:   {data['rain_mm']} mm")
        print(f"Raining:    {'YES 🌧️' if data.get('raining', False) else 'No'}")
        print("---------------------------------")
    except Exception as e:
        print(f"❌ Error parsing data: {e}")
        print(f"[DEBUG] Exception details: {type(e).__name__}")

def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        print(f"✅ Securely connected to {MQTT_BROKER}!")
        client.subscribe(MQTT_TOPIC)
        print(f"📡 Subscribed to: {MQTT_TOPIC}")
    else:
        print(f"❌ Connection failed with code {rc}")

# Setup Client with SSL enabled
client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.tls_set(cert_reqs=ssl.CERT_NONE) # Enable SSL, bypass cert validation for testing
client.on_message = on_message
client.on_connect = on_connect

print(f"Connecting Securely to {MQTT_BROKER} on Port {MQTT_PORT}...")
try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()
except Exception as e:
    print(f"FATAL ERROR: {e}")
    print("\n[HINT] Your network is even blocking encrypted traffic. Use a Mobile Hotspot.")
    exit()
