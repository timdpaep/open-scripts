// -----------------------
// Internals
// -----------------------

WiFiUDP udp;             // Wifi UDP instance
IPAddress ip;           // The ESP's IP
IPAddress outIp(xxx, xx, xx, x); //IP Address to send to (DASHBOARD IP)
OSCMessage msg("/Client-XX"); // OSC Address, replace XX by your Client ID

// -----------------------
// Network Stuff
// -----------------------

char ssid[] = "xxxx";                       // your network SSID (name)
char pass[] = "xxxx";                       // your network password
const unsigned int receivePort = 8888;  // Local port to listen (Same as port in dashboard)
const unsigned int outPort = 57111;      // Port to send to DO NOT CHANGE

// -----------------------
// Pin Assignments
// -----------------------

// -----------------------
// Variables
// -----------------------
