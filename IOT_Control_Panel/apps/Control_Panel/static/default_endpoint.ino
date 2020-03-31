#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include "ESPAsyncWebServer.h"
#include <ESP8266WiFiMulti.h>
#include <ArduinoOTA.h>
#include <ESP8266mDNS.h>
#include <WiFiUdp.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#define ONE_WIRE_BUS 4

ESP8266WiFiMulti WiFiMulti;
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
bool switchwifi = false;
bool switched = false;
const char* ServerSSID = "SKY3164B";
const char* ServerPass = "WMBNTRNCDS";
const char* node_before_ssid = "Relay_2";
String ID = "3";
String AP_ssid = "Relay" + ID;
const char* serverNameTemp = "http://192.168.138.2/temp";
String temperature;
IPAddress local_IP(192,168,138,101);
IPAddress subnet(255,255,255,0);
IPAddress GatewayIP(192,168,139,2);
IPAddress Server_Gateway(192,168,0,1);
//IPAddress AP_IP(192,168,138,2);
unsigned long previousMillis = 0;
const long interval = 5000;
AsyncWebServer server(80);
//byte temperature = 0;
float humidity = 0;
float temp = 0;

void setup() {
  Serial.begin(115200);
  Serial.println();
  WiFi.mode(WIFI_STA);
  //pinMode(DHTPIN, INPUT);
  //dht.begin();
  WiFi.begin(node_before_ssid);
  while((WiFi.status() != WL_CONNECTED)) {
    delay(500);
    Serial.print(".");
  }
  WiFi.config(local_IP, GatewayIP, subnet);
  Serial.println("");
  Serial.println("Connected to WiFi");
  Serial.print("Local IP address: ");
  Serial.println(WiFi.localIP());
  server.on("/temp", HTTP_GET, [](AsyncWebServerRequest *request){
  Serial.print("temp str : ");
  Serial.println(temperature.c_str());
    request->send_P(200, "text/plain", temperature.c_str());
  });
  server.on("/ota", HTTP_GET, [](AsyncWebServerRequest*request)
  {
    request->send_P(200, "text/plain", temperature.c_str());
    switchwifi=true;
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
  server.begin();
  server.begin();
}

void makeReading()
{
  Serial.print("Requesting temperatures...");
  sensors.requestTemperatures(); // Send the command to get temperatures
  Serial.println("DONE");
  temperature = sensors.getTempCByIndex(0);
  if(temperature.toInt() < -50)
  {
    ESP.restart();
  }
}

void flash(String temperature)
{
  if(temperature != "--")
  {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(500);
    digitalWrite(LED_BUILTIN, LOW);
    delay(500);
    digitalWrite(LED_BUILTIN, HIGH);
  }
}

void loop() {
  unsigned long currentMillis = millis();
  if(currentMillis - previousMillis >= interval) {
    // Check WiFi connection status
    if ((WiFiMulti.run() == WL_CONNECTED)) {
      Serial.println(WiFi.localIP());
      makeReading();
      Serial.println(temperature);
      flash(temperature);
      // save the last HTTP GET Request
      previousMillis = currentMillis;
    }
    else {
      Serial.println("WiFi Disconnected");
    }
  }
  if(switchwifi==true)
  {
    if(switched==false)
    {
      SwitchStaConn();
      switched = true;
    }

  }
  ArduinoOTA.handle();
}

String httpGETRequest(const char* serverName) {
  WiFiClient client;
  HTTPClient http;

  // Your IP address with path or Domain name with URL path
  http.begin(client, serverName);

  // Send HTTP POST request
  int httpResponseCode = http.GET();

  String payload = "--";

  if (httpResponseCode>0) {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    payload = http.getString();
  }
  else {
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
  }
  // Free resources
  http.end();

  return payload;
}