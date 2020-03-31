#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <ArduinoOTA.h>
#include <ESP8266mDNS.h>
#include <WiFiUdp.h>
#include <ESP8266WiFiMulti.h>
#include "ESPAsyncWebServer.h"

const char* node_before_ssid = "Gateway_1";
int nodeBeforeID = 1;
bool switchwifi = false;
bool switched = false;
const char* ServerSSID = "SKY3164B";
const char* ServerPass = "WMBNTRNCDS";
IPAddress subnet(255, 255, 255, 0);
IPAddress GatewayIP(192, 168, 137, 101);
String serverNameTemp = "http://192.168.137.1/temp";
String backwardsTest = "http://192.168.138.101/temp";
String ID = "2";
String AP_ssid = "Relay_" + ID;
String temperature;
unsigned long previousMillis = 0;
const long interval = 5000;
IPAddress local_IP(192, 168, 137, + ID.toInt());
IPAddress AP_IP(192, 168, 138, 2);
IPAddress GatewayIPAP(192, 168, 139, 2);
IPAddress Server_Gateway(192,168,0,1);
IPAddress Server_IP(192,168,0,100);
AsyncWebServer server(80);

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);
  Serial.println();
  WiFi.softAP(AP_ssid);
  WiFi.mode(WIFI_AP_STA);
  WiFi.begin(node_before_ssid);
  while ((WiFi.status() != WL_CONNECTED)) {
    delay(500);
    Serial.print(".");
  }
  WiFi.config(local_IP, GatewayIP, subnet);
  Serial.println("");
  Serial.println("Connected to WiFi");
  Serial.print("Local IP address: ");
  Serial.println(WiFi.localIP());
  WiFi.softAPConfig(AP_IP, GatewayIPAP, subnet);
  Serial.print("AP IP address: ");
  Serial.println(WiFi.softAPIP());
  server.on("/temp", HTTP_GET, [](AsyncWebServerRequest * request) {
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
}

void flash(String temperature)
{
  if (temperature != "--")
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

  if (currentMillis - previousMillis >= interval) {
    if ((WiFi.status() == WL_CONNECTED))
    {
      //temperature = httpGETRequest(serverNameTemp);
      //Serial.println(temperature);
      //flash(temperature);
      //Serial.println("-------------------------------------------------");
      temperature = httpGETRequest(backwardsTest);
      Serial.println(temperature);
      flash(temperature);
      Serial.println("-------------------------------------------------");
      Serial.print("Local IP address: ");
      Serial.println(WiFi.localIP());
      Serial.println("-------------------------------------------------");
      Serial.print("AP IP address: ");
      Serial.println(WiFi.softAPIP());
      Serial.println("-------------------------------------------------");
      // save the last HTTP GET Request
      previousMillis = currentMillis;
    }
    //else {
    //  Serial.println("WiFi Disconnected");
    //}
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

void SwitchStaConn()
{
  WiFi.disconnect();
  WiFi.config(Server_IP, Server_Gateway, subnet);
  WiFi.begin(ServerSSID, ServerPass);
  while ((WiFi.status() != WL_CONNECTED)) {
    delay(500);
    Serial.print(".");
  }
  WiFi.config(Server_IP, Server_Gateway, subnet);
  Serial.print("Local IP address: ");
  Serial.println(WiFi.localIP());
}

String httpGETRequest(String serverName) {
  WiFiClient client;
  HTTPClient http;

  http.begin(client, serverName);

  int httpResponseCode = http.GET();

  String payload = "--";

  if (httpResponseCode > 0) {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    payload = http.getString();
  }
  else {
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
  }
  http.end();

  return payload;
}