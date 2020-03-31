#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <ArduinoOTA.h>
#include <ESP8266mDNS.h>
#include <WiFiUdp.h>
#include <ESP8266WiFiMulti.h>
#include "ESPAsyncWebServer.h"

const char* ssid = "Default";
const char* ServerSSID = "SKY3164B";
const char* ServerPass = "WMBNTRNCDS";
String ID = "1";
bool ServerRequest = false;
IPAddress Server_local_IP(192,168,137,101);
IPAddress subnet(255,255,255,0);
IPAddress Server_Gateway(192,168,0,1);
unsigned long previousMillis = 0;
const long interval = 5000;
const char* serverTest = "http://192.168.0.13:8000/test/";
char char_array[32];

// Create AsyncWebServer object on port 80
AsyncWebServer server(80);

void setup(){
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);
  Serial.println();
  WiFi.mode(WIFI_STA);
  WiFi.begin(ServerSSID, ServerPass);
  while((WiFi.status() != WL_CONNECTED)) {
    delay(500);
    Serial.print(".");
  }
  WiFi.config(Server_local_IP, Server_Gateway, subnet);
  Serial.print("Local IP address: ");
  Serial.println(WiFi.localIP());
  server.on("/ota", HTTP_GET, [](AsyncWebServerRequest*request)
  {
    request->send_P(200, "text/html", temperature.c_str());
  });
  ArduinoOTA.setHostname("IOTESP8266");
  ArduinoOTA.onStart([]() {
    Serial.println("Start");
  });
  ArduinoOTA.onEnd([]() {
    Serial.println("\nEnd");
  });
  ArduinoOTA.onProgress([](unsigned int progress, unsigned int total) {
    Serial.printf("Progress: %u%%\r", (progress / (total / 100)));
  });
  ArduinoOTA.onError([](ota_error_t error) {
    Serial.printf("Error[%u]: ", error);
    if (error == OTA_AUTH_ERROR) Serial.println("Auth Failed");
    else if (error == OTA_BEGIN_ERROR) Serial.println("Begin Failed");
    else if (error == OTA_CONNECT_ERROR) Serial.println("Connect Failed");
    else if (error == OTA_RECEIVE_ERROR) Serial.println("Receive Failed");
    else if (error == OTA_END_ERROR) Serial.println("End Failed");
  });
  ArduinoOTA.begin();
  Serial.println("Ready");
  server.begin();
}

void loop(){
  ArduinoOTA.handle();
}