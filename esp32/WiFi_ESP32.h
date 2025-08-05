
#include <WiFi.h>
#include <HTTPClient.h>
#include <NetworkClient.h>
#include <WiFiAP.h>
#include <ArduinoJson.h>

const char *ssid = "ESP32WIFI";        // Change this to your WiFi SSID
const char *password = "TrapRapSuck12456";  // Change this to your WiFi password

const char *host = "http://192.168.4.2:5000/track";

struct AltAz{
  float alt;
  float az;
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
float getMagDec() {
  float magDec;
  HTTPClient http;
  http.begin(host);  // URL of local API
  int httpCode = http.GET();

  if (httpCode == 200) {
    String payload = http.getString();

    StaticJsonDocument<200> doc;
    DeserializationError error = deserializeJson(doc, payload);

    if (!error) {
      
      magDec = doc["magnetic_dec"];
      Serial.printf("Magnetic Dec:  %.2f\n", magDec);
    } else {
      Serial.println("Failed to parse JSON");
    }
  } else {
    Serial.printf("HTTP GET failed, code: %d\n", httpCode);
  }

  http.end();
  return magDec;

}

AltAz getStartAltAz() {
  float temp, hum;
  HTTPClient http;
  http.begin(host);  // URL of local API
  int httpCode = http.GET();

  if (httpCode == 200) {
    String payload = http.getString();

    StaticJsonDocument<200> doc;
    DeserializationError error = deserializeJson(doc, payload);

    if (!error) {
      temp = doc["polaris_alt"];
      hum = doc["polaris_az"];
      Serial.printf("Altitude: %.2f, Azimuth:  %.2f\n", temp, hum);
    } else {
      Serial.println("Failed to parse JSON");
    }
  } else {
    Serial.printf("HTTP GET failed, code: %d\n", httpCode);
  }

  http.end();
  return {temp, hum};

}

AltAz getAltAz() {
  float temp, hum;
  HTTPClient http;
  http.begin(host);  // URL of local API
  int httpCode = http.GET();

  if (httpCode == 200) {
    String payload = http.getString();

    StaticJsonDocument<200> doc;
    DeserializationError error = deserializeJson(doc, payload);

    if (!error) {
      temp = doc["altitude_deg"];
      hum = doc["azimuth_deg"];
      //Serial.printf("Altitude: %.2f, Azimuth:  %.2f\n", temp, hum);
    } else {
      Serial.println("Failed to parse JSON");
    }
  } else {
    Serial.printf("HTTP GET failed, code: %d\n", httpCode);
  }

  http.end();
  return {temp, hum};

}
