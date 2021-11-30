"""
A Python Script that will do positioning
Continuously calls the Pozyx positioning function and prints its position.
"""

import time
from math import ceil
from pypozyx import (POZYX_POS_ALG_UWB_ONLY, POZYX_3D, Coordinates, POZYX_SUCCESS, PozyxConstants, version,
                     DeviceCoordinates, PozyxSerial, get_first_pozyx_serial_port, SingleRegister, DeviceList, PozyxRegisters,
                     NetworkID)

class Position(object):
    def __init__(self, pozyx, algorithm=POZYX_POS_ALG_UWB_ONLY, dimension=POZYX_3D, height=1000, remote_id=None):
      self.pozyx = pozyx
      self.algorithm = algorithm
      self.dimension = dimension
      self.height = height
      self.remote_id = remote_id
      self.network_id = self.getNetworkId()

    def setup(self):
      self.getNetworkId()
      self.printDeviceInfo()

    def getNetworkId(self):
      network_id = NetworkID()
      self.pozyx.getNetworkId(network_id)
      return network_id.id

    def printDeviceInfo(self):
      firmware = SingleRegister()
      status = self.pozyx.getFirmwareVersion(firmware)
      print("This is device 0x%0.4x" % self.network_id)
      if status != POZYX_SUCCESS:
          print("\t- Error: Couldn't retrieve device information")
          return
      print("Firmware version: %i.%i" % (firmware.value >> 4, firmware.value % 0x10))

    def loop(self):
      """Performs positioning and displays/exports the results."""
      position = Coordinates()
      time_before = time.time()
      status = self.pozyx.doPositioning(
          position, self.dimension, self.height, self.algorithm, remote_id=self.remote_id)
      latency = ceil((time.time() - time_before) * 1000)
      if status == POZYX_SUCCESS:
        self.printPublishPosition(position, latency)
      else:
          print("Something went wrong in positioning...")

    def printPublishPosition(self, position, latency):
      """Prints the Pozyx's position in mm"""
      print("POS ID {}: x: {pos.x}, y: {pos.y}, z: {pos.z}, lat: {latency}ms".format(
          "0x%0.4x" % self.network_id, pos=position, latency=latency))

if __name__ == "__main__":
    # shortcut to not have to find out the port yourself
    serial_port = get_first_pozyx_serial_port()
    if serial_port is None:
        print("No Pozyx connected. Check your USB cable or your driver!")
        quit()

    # positioning algorithm to use, other is PozyxConstants.POSITIONING_ALGORITHM_TRACKING
    algorithm = PozyxConstants.POSITIONING_ALGORITHM_UWB_ONLY

    # positioning dimension. Others are PozyxConstants.DIMENSION_2D, PozyxConstants.DIMENSION_2_5D
    dimension = PozyxConstants.DIMENSION_3D

    # height of device, required in 2.5D positioning
    height = 2500

    # create a new pozyx object
    pozyx = PozyxSerial(serial_port)

    r = Position(pozyx, algorithm, dimension, height)
    r.setup()
    while True:
      r.loop()