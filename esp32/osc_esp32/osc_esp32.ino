#include <SLIPEncodedSerial.h>
#include <OSCData.h>
#include <OSCBundle.h>
#include <OSCBoards.h>
#include <OSCTiming.h>
#include <OSCMessage.h>
#include <OSCMatch.h>
#include <SLIPEncodedUSBSerial.h>

#include "Arduino.h"
#include <ESP8266WiFi.h> // This depends on board architecture, ESP32 needs something else
#include <WiFiUdp.h>
#include <SPI.h>
#include <OSCMessage.h>

// -----------------------
// Internals
// -----------------------

WiFiUDP udp;                            // Wifi UDP instance
IPAddress ip;                           // The ESP's IP

// -----------------------
// Network Stuff
// -----------------------

char ssid[] = "";             // your network SSID (name)
char pass[] = "";               // your network password
const unsigned int receivePort = 8888;  // Local port to listen (if listening for some data)
const unsigned int outPort = 9999;      // Port to send to

// -----------------------
// General Program Logic
// -----------------------

/**
 * Sends an OSC message to a specific address
 */
void sendMessage(IPAddress to, OSCMessage msg) {
  // Sending over udp, begin the packet header
  udp.beginPacket(to, outPort);

  // Send the message, the bytes to the SLIP stream
  msg.send(udp);

  // Mark the end of the OSC packet
  udp.endPacket();

  // Free space occupied by message
  msg.empty();
}

/**
 * Receiving the messages from a specific address
 */
void receiveMessage() {
  // Creates the internal
  OSCMessage inmsg;

  // Parse the UDP package
  int size = udp.parsePacket();

  // Did we receive something?
  if (size > 0) {
    while (size--) {
      inmsg.fill(udp.read());
    }
    if (!inmsg.hasError()) {
      inmsg.dispatch("/hello", sayHello);
      // @TODO dispatch other functions
    }
  }
}

// ------------------------------
// Dispatched Logic from receiver
// ------------------------------

/**
 * A demo function to know if the receiver is working
 */
void sayHello(OSCMessage &msg) {
  Serial.print("Hello World!");
}

// ------------------------------
// Setup the program
// ------------------------------

/**
 * Setting up the project
 */
void setup() {
  // Start Serial at a specific Baudrate
  Serial.begin(115200);

  // Prints an empty line
  Serial.println();

  // For iPhone hotspots...SETS TO STATION MODE!
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
// Go looping
// ------------------------------

void loop() {
  /**
   * This is a Sending Example
   */

  /*
  // Sending to? Your computer?
  IPAddress outIp(172, 20, 10, 7);

  // Create an OSCMessage
  OSCMessage msg("/address");
  msg.add("Hello");

  // Send a message
  sendMessage(outIp, msg);

  // Sending every second
  delay(1000);
  */

  /**
   * This wil receive OSC
   */

  // Checks if we received a message
  receiveMessage();

  // Sets delay.. wait
  delay(16);
}
