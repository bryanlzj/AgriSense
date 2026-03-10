#include <WiFi.h>
#include <WiFiClientSecure.h>
#include "PubSubClient.h"
#include <ArduinoJson.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <DHT.h>

// WiFi Configuration (Wokwi uses these credentials)
const char* ssid = "Wokwi-GUEST";
const char* password = "";

// MQTT Configuration
const char* mqtt_server = "broker.emqx.io";
const int mqtt_port = 8883; // Secure Port
const char* mqtt_topic = "agrisense/fyp/peng/data/unique_99";

// Hardware Pins
#define DHTPIN 23
#define DHTTYPE DHT22
#define SOIL_PIN 34
#define SOLAR_PIN 32
#define RAIN_PIN 18
#define ONE_WIRE_BUS 17
#define WIND_PIN 25 // Changed from 35 to 25 because 35 has no internal pull-up

// Sensor Objects
DHT dht(DHTPIN, DHTTYPE);
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature soilTempSensor(&oneWire);
WiFiClientSecure espClient;
PubSubClient client(espClient);

// Rain and Wind Pulse Counting
volatile int rainCount = 0;
volatile int windCount = 0;

const float mmPerTip = 0.2794;
const float windFactor = 2.4;

void IRAM_ATTR countRain() {
  rainCount++;
}

void IRAM_ATTR countWind() {
  windCount++;
}

void setup_wifi() {
  delay(10);
  Serial.print("\nConnecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    String clientId = "ESP32Client-" + String(random(0xffff), HEX);
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  setup_wifi();
  
  // Secure connection setup
  espClient.setInsecure(); // Skip certificate validation for testing
  client.setServer(mqtt_server, mqtt_port);

  dht.begin();
  soilTempSensor.begin();
  pinMode(SOIL_PIN, INPUT);
  pinMode(SOLAR_PIN, INPUT);
  pinMode(RAIN_PIN, INPUT_PULLUP);
  pinMode(WIND_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(RAIN_PIN), countRain, FALLING);
  attachInterrupt(digitalPinToInterrupt(WIND_PIN), countWind, FALLING);

  Serial.println("▸ AgriSense IoT Demo (SECURE) Starting...");
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  int soilRaw = analogRead(SOIL_PIN);
  int soilPercent = map(soilRaw, 0, 4095, 100, 0);
  soilTempSensor.requestTemperatures();
  float soilTemp = soilTempSensor.getTempCByIndex(0);
  float windSpeed = windCount * windFactor;
  float rainMM = rainCount * mmPerTip;
  bool isRaining = digitalRead(RAIN_PIN) == LOW;
  int solarRaw = analogRead(SOLAR_PIN);
  float solarRadiation = map(solarRaw, 0, 4095, 0, 1200);

  StaticJsonDocument<256> doc;
  doc["temp_env"] = isnan(temperature) ? 0 : temperature;
  doc["humidity"] = isnan(humidity) ? 0 : humidity;
  doc["soil_moist"] = soilPercent;
  doc["soil_temp"] = soilTemp;
  doc["solar"] = solarRadiation;
  doc["wind_speed"] = windSpeed;
  doc["raining"] = isRaining;
  doc["rain_mm"] = rainMM;

  char buffer[256];
  serializeJson(doc, buffer);
  Serial.print("Publishing Securely: ");
  Serial.println(buffer);
  client.publish(mqtt_topic, buffer);
  
  windCount = 0; // Reset wind pulse counter
  delay(5000);
}
