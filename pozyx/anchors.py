"""
A Python Script that will setup the anchors on a tag
"""
from time import time

from pypozyx import (PozyxConstants, Coordinates, POZYX_SUCCESS, PozyxRegisters, version, DeviceList,
                     DeviceCoordinates, PozyxSerial, get_first_pozyx_serial_port, SingleRegister, NetworkID)

from pypozyx.tools.version_check import perform_latest_version_check


class Anchors(object):

    def __init__(self, pozyx, anchors, remote_id=None):
        self.pozyx = pozyx
        self.anchors = anchors
        self.remote_id = remote_id

    def setup(self):
        print("Device Information")
        print("-------------------------------")
        self.printDeviceInfo()
        print("")
        print("Current Anchor Information")
        print("-------------------------------")
        self.printAnchorInfo()
        print("")
        print("New Anchor Information")
        print("-------------------------------")
        self.printPublishAnchorConfiguration()
        self.setAnchorsManual()
        print("")
        print("New Anchor IDs on device")
        print("-------------------------------")
        self.printAnchorInfo()

    def printAnchorInfo(self):
        list_size = SingleRegister()
        self.pozyx.getNumberOfAnchors(list_size)
        anchor_list = DeviceList(list_size=list_size[0])
        self.pozyx.getPositioningAnchorIds(anchor_list)
        print("Anchor", anchor_list)

    def printDeviceInfo(self):
        firmware = SingleRegister()
        status = self.pozyx.getFirmwareVersion(firmware)
        network_id = NetworkID()
        self.pozyx.getNetworkId(network_id)
        print("This is device 0x%0.4x" % network_id.id)
        if status != POZYX_SUCCESS:
            print("\t- Error: Couldn't retrieve device information")
            return
        print("Firmware version: %i.%i" %
              (firmware.value >> 4, firmware.value % 0x10))

    def printPublishAnchorConfiguration(self):
        for anchor in self.anchors:
            print("ANCHOR 0x%0.4x,%s" % (anchor.network_id, str(anchor.pos)))

    def setAnchorsManual(self):
        status = self.pozyx.configureAnchors(self.anchors)
        status = self.pozyx.clearDevices(self.remote_id)
        for anchor in self.anchors:
            status &= self.pozyx.addDevice(anchor, remote_id=self.remote_id)
        if len(self.anchors) > 4:
            status &= self.pozyx.setSelectionOfAnchors(PozyxConstants.ANCHOR_SELECT_AUTO, len(self.anchors),
                                                       remote_id=self.remote_id)
        self.pozyx.saveAnchorIds(remote_id=self.remote_id)
        self.pozyx.saveRegisters(
            [PozyxRegisters.POSITIONING_NUMBER_OF_ANCHORS], remote_id=self.remote_id)
        return status


if __name__ == "__main__":
    # shortcut to not have to find out the port yourself.
    serial_port = get_first_pozyx_serial_port()
    if serial_port is None:
        print("No Pozyx connected. Check your USB cable or your driver!")
        quit()

    # necessary data for calibration
    anchors = [DeviceCoordinates(0xa000, 1, Coordinates(0, 0, 2500)),
               DeviceCoordinates(0x6968, 1, Coordinates(0, 3100, 2500)),
               DeviceCoordinates(0x6945, 1, Coordinates(1900, 0, 2500)),
               DeviceCoordinates(0x696b, 1, Coordinates(1900, 3100, 2500))]

    # create a new pozyx object
    pozyx = PozyxSerial(serial_port)

    # create a new anchor object
    anchors = Anchors(pozyx, anchors)

    # setup the anchors
    anchors.setup()
