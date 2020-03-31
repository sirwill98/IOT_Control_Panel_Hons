#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <ArduinoOTA.h>
#include <ESP8266mDNS.h>
#include <WiFiUdp.h>
#include <ESP8266WiFiMulti.h>
#include "ESPAsyncWebServer.h"

// Set your access point network credentials
const char* ssid = "Gateway_1";
const char* ServerSSID = "SKY3164B";
const char* ServerPass = "WMBNTRNCDS";
const char* OTASSID = "WillsLaptop";
const char* OTAPass = "Password123";
String ID = "1";
String nodeIP =  String(ID + 100);
bool ServerRequest = false;
IPAddress local_IP(192,168,137,ID.toInt());
IPAddress Server_local_IP(192,168,137,101);
IPAddress subnet(255,255,255,0);
IPAddress GatewayIP(192,168,139,1);
IPAddress Server_Gateway(192,168,0,1);
unsigned long previousMillis = 0;
String temperature;
bool serverRegister = false;
const long interval = 5000;
const char* serverNameTemp = "http://192.168.137.2/temp";
const char* serverTest = "http://192.168.0.13:8000/test/";
char char_array[32];

// Create AsyncWebServer object on port 80
AsyncWebServer server(80);

void setup(){
  // Serial port for debugging purposes
  char_array[0] = 0;
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);
  Serial.println();
  WiFi.mode(WIFI_AP_STA);
  // Setting the ESP as an access point
  Serial.print("Setting AP (Access Point)…");
  // Remove the password parameter, if you want the AP (Access Point) to be open
  WiFi.softAP(ssid);
  //WiFi.begin(node_after_ssid);
  WiFi.softAPConfig(local_IP, GatewayIP, subnet);
  delay(50);
  IPAddress IP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(IP);
  WiFi.begin(ServerSSID, ServerPass);
  while((WiFi.status() != WL_CONNECTED)) {
    delay(500);
    Serial.print(".");
  }
  WiFi.config(Server_local_IP, Server_Gateway, subnet);
  Serial.print("Local IP address: ");
  Serial.println(WiFi.localIP());
  server.on("/temp", HTTP_GET, [](AsyncWebServerRequest *request){
    if(!ServerRequest)
    {
      request->send_P(200, "text/html", temperature.c_str());
      //request->send_P(200, "text/html", "<html><body><h1>it work</h1></body></html>");
      //ServerRequest = true;
    }
    else
    {
      request->send_P(200, "text/plain", "bums");
      Serial.println(char_array);
      Serial.print(" ::: this is the array");
    }
  });
  server.on("/ota", HTTP_GET, [](AsyncWebServerRequest*request)
  {
    int paramsNr = request->params();
    for(int i=0;i<paramsNr;i++)
    {
      AsyncWebParameter* p = request->getParam(i);
      if(p->name() == "ID" & p->value() == ID)
      {
        Serial.print("Param name: ");
        Serial.println(p->name());
        Serial.print("Param value: ");
        Serial.println(p->value());
      }
    }
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
  temperature = httpGETRequest(serverNameTemp);
  Serial.println(WiFi.softAPIP());
  if(temperature != "--")
  {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(500);
    digitalWrite(LED_BUILTIN, LOW);
    delay(500);
    digitalWrite(LED_BUILTIN, HIGH);
    Serial.println(temperature);
  }
  Serial.println("-------------------------------------------------");
  Serial.println(WiFi.localIP());
  Serial.println("-------------------------------------------------");
  if(!serverRegister)
  {
    String getserver = httpGETRequest(serverTest);
    serverRegister = true;
    Serial.println("-------------------------------------------------");
    Serial.println(getserver);
  }
  delay(2000);
  ArduinoOTA.handle();
}

const char* strtochar(String str)
{
  int len = str.length();
  char charbuf[len];
  str.toCharArray(charbuf, len);
  return charbuf;
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