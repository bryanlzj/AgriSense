#include <Arduino.h>
#line 1 "C:\\Users\\weike\\Arduino&Wokwi\\Wokwi Simulator\\sketch\\sketch.ino"
#include <WiFi.h>
#include "PubSubClient.h"
#include <ArduinoJson.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <DHT.h>

// WiFi Configuration (Wokwi uses these credentials)
const char* ssid = "Wokwi-GUEST";
const char* password = "";

// MQTT Configuration
const char* mqtt_server = "test.mosquitto.org";
const char* mqtt_topic = "agrisense/sensor_data";

// Hardware Pins
#define DHTPIN 23
#define DHTTYPE DHT22
#define SOIL_PIN 34
#define SOLAR_PIN 32
#define RAIN_PIN 18
#define ONE_WIRE_BUS 17
#define WIND_PIN 35

// Sensor Objects
DHT dht(DHTPIN, DHTTYPE);
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature soilTempSensor(&oneWire);
WiFiClient espClient;
PubSubClient client(espClient);

// Rain and Wind Pulse Counting
volatile int rainCount = 0;
volatile int windCount = 0;

// Constants
const float mmPerTip = 0.2794;
const float windFactor = 2.4;

#line 48 "C:\\Users\\weike\\Arduino&Wokwi\\Wokwi Simulator\\sketch\\sketch.ino"
void setup_wifi();
#line 67 "C:\\Users\\weike\\Arduino&Wokwi\\Wokwi Simulator\\sketch\\sketch.ino"
void reconnect();
#line 85 "C:\\Users\\weike\\Arduino&Wokwi\\Wokwi Simulator\\sketch\\sketch.ino"
void setup();
#line 104 "C:\\Users\\weike\\Arduino&Wokwi\\Wokwi Simulator\\sketch\\sketch.ino"
void loop();
#line 40 "C:\\Users\\weike\\Arduino&Wokwi\\Wokwi Simulator\\sketch\\sketch.ino"
void IRAM_ATTR countRain() {
  rainCount++;
}

void IRAM_ATTR countWind() {
  windCount++;
}

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP32Client-";
    clientId += String(random(0xffff), HEX);
    
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
  client.setServer(mqtt_server, 1883);

  dht.begin();
  soilTempSensor.begin();

  pinMode(SOIL_PIN, INPUT);
  pinMode(SOLAR_PIN, INPUT);
  pinMode(RAIN_PIN, INPUT_PULLUP);
  pinMode(WIND_PIN, INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(RAIN_PIN), countRain, FALLING);
  attachInterrupt(digitalPinToInterrupt(WIND_PIN), countWind, FALLING);

  Serial.println("▸ AgriSense IoT Demo (Connected) Starting...");
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // Read Sensors
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

  // Create JSON Data
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

  // Publish Data
  Serial.print("Publishing to MQTT: ");
  Serial.println(buffer);
  
  if (client.publish(mqtt_topic, buffer)) {
    Serial.println("Success!");
  } else {
    Serial.println("Failed to publish.");
  }

  // Reset wind count
  windCount = 0;

  delay(5000); // Send data every 5 seconds
}

