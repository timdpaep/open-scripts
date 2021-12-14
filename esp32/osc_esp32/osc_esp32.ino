#include <SLIPEncodedSerial.h>
#include <OSCData.h>
#include <OSCBundle.h>
#include <OSCBoards.h>
#include <OSCTiming.h>
#include <OSCMessage.h>
#include <OSCMatch.h>
#include <SLIPEncodedUSBSerial.h>

#include "Arduino.h"
// #include <ESP8266WiFi.h> // Wifi library for ESP8266
// #include <WiFi.h> // Wifi library for the ESP32
#include <WiFiUdp.h>
#include <SPI.h>
#include <OSCMessage.h>

// -----------------------
// Variables
// -----------------------

#include "variables.h"

// -----------------------
// Setup
// -----------------------

void setup() {
  // Start Serial at a specific Baudrate
  Serial.begin(115200);

  // TODO: Set pin modes
  

  // Connecting to WiFi

  // Set Station mode ESP32
  WiFi.mode(WIFI_STA);

  // Begin WiFi looking
  WiFi.begin(ssid, pass);

  // Start connecting and wait
  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println();

  // When we are connected
  Serial.print("Connected, IP address: ");
  ip = WiFi.localIP();
  Serial.println(ip);

  // Begin with UDP
  udp.begin(receivePort);
}

// ------------------------------
// Program loop
// ------------------------------

void loop() {
  //@TODO your code

  // Checks if we received a message
  receiveMessage();
}
