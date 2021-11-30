#!/usr/bin/env python3
"""
A script that will read the positioning data on the tag
"""
from time import sleep, time
from math import ceil
from pypozyx import (PozyxSerial, get_first_pozyx_serial_port, PositioningData, SingleRegister,
                     PozyxConstants, POZYX_SUCCESS, Coordinates)


class CurrentPosition:
    def __init__(self, pozyx):
        self.pozyx = pozyx
        self.time_before = time()
        self.x = 0
        self.y = 0
        self.z = 0
        self.latency = 0

    def setup(self):
        self.get_position()

    def get_position(self):
        position = Coordinates()
        position_data = PositioningData(0b1)
        status = self.pozyx.getPositioningData(position_data)
        if status == POZYX_SUCCESS:
            position.load_bytes(position_data.byte_data)
            if self.x != position.x or self.y != position.y or self.z != position.z:
                self.x = position.x
                self.y = position.y
                self.z = position.z
                self.latency = ceil((time() - self.time_before) * 1000)
                self.printPublishPosition(position, self.latency)
                self.time_before = time()

    def printPublishPosition(self, position, latency):
        print("x: {pos.x}, y: {pos.y}, z: {pos.z}, latency: {lat}ms".format(
            pos=position, lat=latency))


if __name__ == '__main__':
    serial_port = get_first_pozyx_serial_port()
    if serial_port is None:
        print("No Pozyx connected. Check your USB cable or your driver!")
        quit()

    # get the pozyx
    pozyx = PozyxSerial(serial_port)

    # change to remote ID for troubleshooting that device
    remote_id = None

    # do positioning if needed
    position = False

    # create current position object
    current_position = CurrentPosition(pozyx)

    # get position
    current_position.setup()

    # start the loop
    while True:
        current_position.get_position()
