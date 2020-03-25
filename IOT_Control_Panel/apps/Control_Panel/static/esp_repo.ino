//endpoint sensor variables
int pinDHT11 = 2;
SimpleDHT11 dht11(pinDHT11);
//endpoint sensor variables>>

//endpoint sensor libraries
#include <SimpleDHT.h>
//endpoint sensor libraries>>

//endpoint code
#include <ESP8266WiFi.h>
#include <ESP8266mDNS.h>
#include <WiFiUdp.h>
#include <ESP8266WebServer.h>
#include <ArduinoOTA.h>

const char* ID = "0";
const char* ssid = "";
const char* password = "";
const char* OTA_SSID = "WillsLaptop";
const char* OTA_PASSWORD = "Password123";
const int ESP_BUILTIN_LED = 2;
byte temperature = 0;
byte highest = 0;
int after_ID = 0;
int pinDHT11 = 2;
IPAddress host(192,168,4,after_ID);
const char* node_before_ssid = "0";
ESP8266WebServer server(80);

void setup()
{
  server.on("/data/", HTTP_GET, handleData);
  server.on("/handleota/", HTTP_GET, handleOTA);
  server.on("/highest/", HTTP_GET, handleHighest);
  server.begin();
}

void loop()
{
  server.handleClient();
}

void makeReading()
{
  byte data[40] = {0};

  int err = SimpleDHTErrSuccess;
  if ((err = dht11.read(&temperature, &humidity, NULL)) != SimpleDHTErrSuccess) {
    delay(1000);
    return;
  }

  if((int)temperature > (int)highest){
      highest = temperature;
  }
}

void handleOTA()
{
  WiFi.mode(WIFI_STA);
  WiFi.begin(OTA_SSID, OTA_PASSWORD);
  while (WiFi.waitForConnectResult() != WL_CONNECTED) {
    Serial.println(".");
  }
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
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  pinMode(ESP_BUILTIN_LED, OUTPUT);
  digitalWrite(ESP_BUILTIN_LED, LOW);
  delay(100);
  digitalWrite(ESP_BUILTIN_LED, HIGH);
  delay(100);
  digitalWrite(ESP_BUILTIN_LED, LOW);
  delay(100);
  digitalWrite(ESP_BUILTIN_LED, HIGH);
  delay(100);
}

void handleData()
{
  makeReading()
  WiFiClient client;
  if (client.connect(host, 80))
  {
    String url = "/data/";
    url += "?sensor_reading=";
    url += temperature;
    url += "&first_node=1";
    client.print(String("GET ") + url + " HTTP/1.1\r\n" +
                "Host: " + ipToString(host) + "\r\n" +
                "Connection: close\r\n\r\n");
    unsigned long timeout = millis();
    while (client.available() == 0)
    {
        if (millis() - timeout > 5000)
        {
            Serial.println(">>> Client Timeout !");
            client.stop();
            return;
        }
    }
  }
}

void handleHighest()
{
  makeReading()
  WiFiClient client;
  if (client.connect(host, 80))
  {
    String url = "/data/";
    url += "?sensor_reading=";
    url += highest;
    url += "&first_node=1";
    client.print(String("GET ") + url + " HTTP/1.1\r\n" +
                "Host: " + ipToString(host) + "\r\n" +
                "Connection: close\r\n\r\n");
    unsigned long timeout = millis();
    while (client.available() == 0)
    {
      if (millis() - timeout > 5000)
      {
          Serial.println(">>> Client Timeout !");
          client.stop();
          return;
      }
    }
  }
}

String ipToString(const IPAddress& address){
  return String(address[0]) + "." + address[1] + "." + address[2] + "." + address[3];
}
//endpoint code>>

//relay code
#include <ESP8266mDNS.h>
#include <WiFiUdp.h>
#include <ESP8266WebServer.h>
#include <ArduinoOTA.h>
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

String node_before_ssid = "0";
String node_after_ssid = "0";
String node_before_id = "0";
String node_after_id = "0";
String ID = "0";
String AP_ssid = "Relay" + ID;
String ssid = "";
String password = "";
const int ESP_BUILTIN_LED = 2;
int temperature = 0;
const char* OTA_SSID = "WillsLaptop";
const char* OTA_PASSWORD = "Password123";
IPAddress local_IP(192,168,4,ID.toInt());
IPAddress node_before_IP(192,168,4,node_before_id.toInt());
IPAddress node_after_IP(192,168,4,node_after_id.toInt());
IPAddress subnet(255,255,255,0);

ESP8266WebServer server(80);

void setup()
{
  WiFi.mode(WIFI_AP_STA);
  WiFi.softAPConfig(local_IP, /*may not work -->*/WiFi.gatewayIP(), subnet);
  WiFi.softAP(AP_ssid);
  WiFi.begin(node_before_ssid);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
  }
  server.on("/data/", HTTP_GET, fSetData);
  server.on("/highest/", HTTP_GET, fSetHighest);
  server.on("/handleota/", HTTP_GET, handleOTA)
  server.begin();
}

void loop()
{
  server.handleClient();
}
void fSetData()
{
  handlePassOnRequest("data");
}

void fSetHighest()
{
  handlePassOnRequest("highest");
}

void handleOTA()
{
  WiFi.mode(WIFI_STA);
  WiFi.begin(OTA_SSID, OTA_PASSWORD);
  while (WiFi.waitForConnectResult() != WL_CONNECTED) {
    Serial.println(".");
  }
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
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  pinMode(ESP_BUILTIN_LED, OUTPUT);
  digitalWrite(ESP_BUILTIN_LED, LOW);
  delay(100);
  digitalWrite(ESP_BUILTIN_LED, HIGH);
  delay(100);
  digitalWrite(ESP_BUILTIN_LED, LOW);
  delay(100);
  digitalWrite(ESP_BUILTIN_LED, HIGH);
  delay(100);
}

void handlePassOnRequest(String reqType)
{
  if(!server.args())
  {
    WiFi.disconnect(true);
    WiFi.begin(node_after_ssid);
    WiFiClient client;
    if (client.connect(node_after_IP, 80))
    {
      String url = "/" + reqType + "/";
      client.print(String("GET ") + url + " HTTP/1.1\r\n" +
                "Host: " + ipToString(node_after_IP) + "\r\n" +
                "Connection: close\r\n\r\n");
      unsigned long timeout = millis();
      while (client.available() == 0)
      {
        if (millis() - timeout > 5000)
        {
          Serial.println(">>> Client Timeout !");
          client.stop();
          return;
        }
      }
    }
    WiFi.disconnect(true);
    WiFi.begin(node_before_ssid);
  }
  else
  {
    handlePassBack();
  }
}

void handlePassBack()
{
  if (server.hasArg("sensor_reading"))
  {
    int readingInt = server.arg("sensor_reading").toInt();
    WiFiClient client;
    if (client.connect(node_before_IP, 80))
    {
      String url = "/data/";
      url += "?sensor_reading=";
      url += readingInt;
      client.print(String("GET ") + url + " HTTP/1.1\r\n" +
                "Host: " + ipToString(node_before_IP) + "\r\n" +
                "Connection: close\r\n\r\n");
      unsigned long timeout = millis();
      while (client.available() == 0)
      {
        if (millis() - timeout > 5000)
        {
          Serial.println(">>> Client Timeout !");
          client.stop();
          return;
        }
      }
    }
  }
}

String ipToString(const IPAddress& address){
  return String(address[0]) + "." + address[1] + "." + address[2] + "." + address[3];
}
//relay code>>

//gateway code
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>

String node_after_ssid = "0";
String node_after_id = "0";
String ID = "0";
String AP_ssid = "ESP12" + ID;
String ssid = "";
String password = "";
String OTA_SSID = "WillsLaptop";
String OTA_PASSWORD = "Password123";
IPAddress severIP(127,0,0,1);
IPAddress local_IP(192,168,4,ID.toInt());
IPAddress node_after_IP(192,168,4,node_after_id.toInt());
IPAddress subnet(255,255,255,0);

ESP8266WebServer server(80);

void setup()
{
  WiFi.mode(WIFI_AP_STA);
  WiFi.softAPConfig(local_IP, /*may not work -->*/WiFi.gatewayIP(), subnet);
  WiFi.softAP(AP_ssid);
  WiFi.begin(OTA_SSID, OTA_PASSWORD);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
  }
  server.on("/data/", HTTP_GET, fSetData);
  server.on("/highest/", HTTP_GET, fSetHighest);
  server.on("/handleota/", HTTP_GET, handleOTA)
  server.begin();
}

void loop()
{
  server.handleClient();
}
void fSetData()
{
  handlePassOnRequest("data");
}

void fSetHighest()
{
  handlePassOnRequest("highest");
}

void handleOTA()
{
  //OTA code goes here
  WiFi.mode(WIFI_AP);
  WiFi.softAP(AP_ssid);
  while (WiFi.waitForConnectResult() != WL_CONNECTED) {
    Serial.println(".");
  }
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
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  pinMode(ESP_BUILTIN_LED, OUTPUT);
  digitalWrite(ESP_BUILTIN_LED, LOW);
  delay(100);
  digitalWrite(ESP_BUILTIN_LED, HIGH);
  delay(100);
  digitalWrite(ESP_BUILTIN_LED, LOW);
  delay(100);
  digitalWrite(ESP_BUILTIN_LED, HIGH);
  delay(100);
}

void handlePassOnRequest(String reqType)
{
  if(!server.args())
  {
    WiFi.disconnect(true);
    WiFi.begin(node_after_ssid);
    WiFiClient client;
    if (client.connect(node_after_IP, 80))
    {
      String url = "/" + reqType + "/";
      client.print(String("GET ") + url + " HTTP/1.1\r\n" +
                "Host: " + ipToString(node_after_IP) + "\r\n" +
                "Connection: close\r\n\r\n");
      unsigned long timeout = millis();
      while (client.available() == 0)
      {
        if (millis() - timeout > 5000)
        {
          Serial.println(">>> Client Timeout !");
          client.stop();
          return;
        }
      }
    }
    WiFi.disconnect(true);
    WiFi.begin(OTA_SSID, OTA_PASSWORD);
  }
  else
  {
    handlePassBack();
  }
}

void handlePassBack()
{
  if (server.hasArg("sensor_reading"))
  {
    int readingInt = server.arg("sensor_reading").toInt();
    WiFiClient client;
    if (client.connect(severIP, 80))
    {
      String url = "/data/";
      url += "?sensor_reading=";
      url += readingInt;
      client.print(String("GET ") + url + " HTTP/1.1\r\n" +
                "Host: " + ipToString(severIP) + "\r\n" +
                "Connection: close\r\n\r\n");
      unsigned long timeout = millis();
      while (client.available() == 0)
      {
        if (millis() - timeout > 5000)
        {
          Serial.println(">>> Client Timeout !");
          client.stop();
          return;
        }
      }
    }
  }
}

String ipToString(const IPAddress& address){
  return String(address[0]) + "." + address[1] + "." + address[2] + "." + address[3];
}
//gateway code>>
