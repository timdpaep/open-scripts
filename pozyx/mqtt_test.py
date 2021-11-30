"""
A Python Script that will do positioning
Continuously calls the Pozyx positioning function and prints its position.
"""

import paho.mqtt.client as paho
from time import sleep
import json


class Position:
    def __init__(self, x, y, z, lat):
        self.x = x
        self.y = y
        self.z = z
        self.lat = lat


class MqttTest(object):
    def __init__(self, broker, port):
        self.broker = broker
        self.port = port
        self.client = paho.Client('mqtt_test')
        self.client.connect(broker, port)
        self.client.on_connect = self.on_connect

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

    def sendTestMessage(self, message):
        self.client.publish("mqtt_test/hello", message)

    def sendTestObject(self, object):
        self.client.publish("mqtt_test/hello", json.dumps(object))


if __name__ == "__main__":
    # create a new test
    mqtt_test = MqttTest("localhost", 1883)

    # loop and send 5 mqtt messages
    for i in range(5):
        # mqtt_test.sendTestMessage(f"Message {i+1}")
        position = Position(10, 20, 30, 40)
        mqtt_test.sendTestObject(position.__dict__)
        sleep(1)
