
// -----------------------
// General OSC Logic
// -----------------------

/**
 * Sends an OSC message to a specific address
 * Include host IP, msg type and state to send
 */
void sendMessage(IPAddress to, OSCMessage& msg, int state) {
  // Add state to message
  msg.add(state);
  
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
      inmsg.dispatch("/servermessage", handleReceive);
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
void handleReceive(OSCMessage &msg) {
  // Get state from message
  int state = msg.getInt(0);

  // TODO : Handle state received
  Serial.println(state);
}