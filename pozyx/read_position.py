#!/usr/bin/env python3
"""
A script that will read the positioning data on the tag
"""

from pypozyx import (PozyxSerial, get_first_pozyx_serial_port, PositioningData, SingleRegister,
                     PozyxConstants, POZYX_SUCCESS, Coordinates)


def get_position(pozyx):
    position = Coordinates()
    position_data = PositioningData(0b1)
    status = pozyx.getPositioningData(position_data)
    if status == POZYX_SUCCESS:
        position.load_bytes(position_data.byte_data)
        printPublishPosition(position)


def doPositioning(pozyx):
    position = Coordinates()
    return pozyx.doPositioning(
        position, PozyxConstants.DIMENSION_3D, 2500, PozyxConstants.POSITIONING_ALGORITHM_UWB_ONLY, remote_id=None)


def printPublishPosition(position):
    print("x: {pos.x}, y: {pos.y}, z: {pos.z}".format(pos=position))


if __name__ == '__main__':
    serial_port = get_first_pozyx_serial_port()
    if serial_port is None:
        print("No Pozyx connected. Check your USB cable or your driver!")
        quit()

    pozyx = PozyxSerial(serial_port)

    # change to remote ID for troubleshooting that device
    remote_id = None

    # do positioning if needed
    position = False

    # see what we need to do
    if position is True and doPositioning(pozyx) == POZYX_SUCCESS:
        get_position(pozyx)
    else:
        get_position(pozyx)
