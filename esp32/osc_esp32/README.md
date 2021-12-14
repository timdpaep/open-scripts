# 1141-OSC-ESP-Message-Boilerplate
Boilerplate for sending and receiving OSC messages via WiFi on an ESP32.
Arduino automatically imports all .ino files in alphabetical order, so make sure to not have circular dependencies. Put all global variables in the variables.h file.

## To do when installing:
In Variables: 
- Change outIp to dashboard IP
- Change msg("Client-XX") to own client assigned number
- Change ssid to the network both devices are connected to
- Change password
- receivePort port ESP listens to, does not need to change, has to be same as in dashboard
- outPort has to be port dashboard listens to. Consult with dashboard maker which port this is.
- Configure pin assignments and custom variables

In main file:
- Check if the correct wifi library is imported for your board
- Set pin modes in setup
- Start writing your program in loop
- Make sure to avoid unconditional delay() functions in the loop function to make sure ESP remains able to listen to incoming messages

## When running for the first time
Open Serial monitor and take note of your ESP's IP Address to put in the dashboard

## When using
Always send a message in this format:
sendMessage(outIp, msg, ###);
Replace the ### with your desired state. outIp and msg are variables you always need