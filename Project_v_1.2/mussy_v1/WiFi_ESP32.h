
#include <WiFi.h>
#include <HTTPClient.h>
#include <NetworkClient.h>
#include <WiFiAP.h>
#include <ArduinoJson.h>

const char *ssid = "ESP32WIFI";        // Change this to your WiFi SSID
const char *password = "TrapRapSuck12456";  // Change this to your WiFi password

const char *host = "http://192.168.4.2:5000/track";
const char *host_cal = "http://192.168.4.2:5000/calibrate";

struct AltAz{
  float alt;
  float az;
};
struct startAltAz{
  float alt;
  float az;
  String command;
  String speed;
};

void setupWiFi() {
  Serial.println();
  Serial.println("Configuring access point...");

  // You can remove the password parameter if you want the AP to be open.
  // a valid password must have more than 7 characters
  if (!WiFi.softAP(ssid, password)) {
    log_e("Soft AP creation failed.");
    while (1);
  }
  IPAddress myIP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(myIP);

  Serial.println("Server started");
}
bool clientConnected(){
  HTTPClient http;
  http.begin(host);
  int httpCode = http.GET();
  if (httpCode != -1){
    return 1;
  }
  return 0;
}


startAltAz getStartAltAz() {
  float alt, az;
  String command;
  String speed;
  HTTPClient http;
  http.begin(host_cal);  // URL of local API
  int httpCode = http.GET();

  if (httpCode == 200) {
    String payload = http.getString();

    StaticJsonDocument<200> doc;
    DeserializationError error = deserializeJson(doc, payload);

    if (!error) {
      alt = doc["alt"];
      az = doc["az"];
      command = doc["command"].as<String>();
      speed = doc["speed"].as<String>();
      Serial.printf("Altitude: %.2f, Azimuth:  %.2f, Command: %.2f, Speed: %.2f\n", alt, az, command, speed);
    } else {
      Serial.println("Failed to parse JSON");
    }
  } else {
    Serial.printf("HTTP GET failed, code: %d\n", httpCode);
  }

  http.end();
  return {alt, az, command, speed};

}

AltAz getAltAz() {
  float alt, az;
  HTTPClient http;
  http.begin(host);  // URL of local API
  int httpCode = http.GET();

  if (httpCode == 200) {
    String payload = http.getString();

    StaticJsonDocument<200> doc;
    DeserializationError error = deserializeJson(doc, payload);

    if (!error) {
      alt = doc["altitude_deg"];
      az = doc["azimuth_deg"];
      //Serial.printf("Altitude: %.2f, Azimuth:  %.2f\n", temp, hum);
    } else {
      Serial.println("Failed to parse JSON");
    }
  } else {
    Serial.printf("HTTP GET failed, code: %d\n", httpCode);
  }

  http.end();
  return {alt, az};

}
