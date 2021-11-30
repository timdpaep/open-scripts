#!/usr/bin/env python3
"""
The Pozyx ready to localize tutorial (c) Pozyx Labs
Please read the tutorial that accompanies this sketch:
https://www.pozyx.io/Documentation/Tutorials/ready_to_localize/Python
This tutorial requires at least the contents of the Pozyx Ready to Localize kit. It demonstrates the positioning capabilities
of the Pozyx device both locally and remotely. Follow the steps to correctly set up your environment in the link, change the
parameters and upload this sketch. Watch the coordinates change as you move your device around!
"""
from time import sleep, time
from math import ceil
from pypozyx import (PozyxConstants, Coordinates, POZYX_SUCCESS, PozyxRegisters, version,
                     DeviceCoordinates, PozyxSerial, get_first_pozyx_serial_port, SingleRegister)
from pypozyx.tools.version_check import perform_latest_version_check


class MultitagPositioning(object):
    """Continuously performs multitag positioning"""

    def __init__(self, pozyx, tag_ids, anchors, log_tag_ids,
                 calculate_latency, latency_tag,
                 latency_samples):
        self.pozyx = pozyx
        self.tag_ids = tag_ids
        self.anchors = anchors

        # logging
        self.log_tag_ids = log_tag_ids

        # latency
        self.time_before = time()
        self.calculate_latency = calculate_latency
        self.latency_tag = latency_tag
        self.latency_table = []
        self.latency_samples = latency_samples

    def setup(self):
        """Sets up the Pozyx for positioning by calibrating its anchor list."""
        print("------------POZYX MULTITAG POSITIONING V{} -------------".format(version))
        print("")
        if None in self.tag_ids:
            for device_id in self.tag_ids:
                self.pozyx.printDeviceInfo(device_id)
        else:
            for device_id in [None] + self.tag_ids:
                self.pozyx.printDeviceInfo(device_id)
        print("")
        print("------------POZYX MULTITAG POSITIONING V{} -------------".format(version))
        print("")

        self.setAnchorsManual(save_to_flash=False)
        self.printPublishAnchorConfiguration()

    def loop(self):
        """Performs positioning and prints the results."""
        for tag_id in self.tag_ids:
            position = Coordinates()
            status = self.pozyx.doPositioning(
                position, height=2500, remote_id=tag_id)
            if status == POZYX_SUCCESS:
                # if we need to calculate the latency
                if self.calculate_latency == True:
                    if tag_id == self.latency_tag and len(self.latency_table) >= self.latency_samples:
                        print("Latency for tag {} with {} samples is now {}ms.".format(
                            hex(self.latency_tag), self.latency_samples, ceil((sum(self.latency_table) / len(self.latency_table)) * 1000)))
                        self.latency_table = []
                    elif tag_id == self.latency_tag:
                        current_time = time()
                        self.latency_table.append(
                            current_time - self.time_before)
                        self.time_before = current_time
                # if we just want to publish the position
                else:
                    if len(self.log_tag_ids) == 0 or tag_id in self.log_tag_ids:
                        self.printPublishPosition(position, tag_id)
            else:
                self.printPublishErrorCode("positioning", tag_id)

    def printPublishPosition(self, position, network_id):
        """Prints the Pozyx's position and possibly sends it as a OSC packet"""
        if network_id is None:
            network_id = 0
        s = "POS ID: {}, x(mm): {}, y(mm): {}, z(mm): {}".format("0x%0.4x" % network_id,
                                                                 position.x, position.y, position.z)
        print(s)

    def setAnchorsManual(self, save_to_flash=False):
        """Adds the manually measured anchors to the Pozyx's device list one for one."""
        for tag_id in self.tag_ids:
            status = self.pozyx.clearDevices(tag_id)
            for anchor in self.anchors:
                status &= self.pozyx.addDevice(anchor, tag_id)
            if len(anchors) > 4:
                status &= self.pozyx.setSelectionOfAnchors(PozyxConstants.ANCHOR_SELECT_AUTO, len(anchors),
                                                           remote_id=tag_id)
            # enable these if you want to save the configuration to the devices.
            if save_to_flash:
                self.pozyx.saveAnchorIds(tag_id)
                self.pozyx.saveRegisters(
                    [PozyxRegisters.POSITIONING_NUMBER_OF_ANCHORS], tag_id)

            self.printPublishConfigurationResult(status, tag_id)

    def printPublishConfigurationResult(self, status, tag_id):
        """Prints the configuration explicit result, prints and publishes error if one occurs"""
        if tag_id is None:
            tag_id = 0
        if status == POZYX_SUCCESS:
            print("Configuration of tag %s: success" % tag_id)
        else:
            self.printPublishErrorCode("configuration", tag_id)

    def printPublishErrorCode(self, operation, network_id):
        """Prints the Pozyx's error and possibly sends it as a OSC packet"""
        error_code = SingleRegister()
        status = self.pozyx.getErrorCode(error_code, network_id)
        if network_id is None:
            network_id = 0
        if status == POZYX_SUCCESS:
            print("Error %s on ID %s, %s" %
                  (operation, "0x%0.4x" % network_id, self.pozyx.getErrorMessage(error_code)))
        else:
            # should only happen when not being able to communicate with a remote Pozyx.
            self.pozyx.getErrorCode(error_code)
            print("Error % s, local error code %s" %
                  (operation, str(error_code)))

    def printPublishAnchorConfiguration(self):
        for anchor in self.anchors:
            print("ANCHOR,0x%0.4x,%s" % (anchor.network_id, str(anchor.pos)))


if __name__ == "__main__":
    # Check for the latest PyPozyx version. Skip if this takes too long or is not needed by setting to False.
    check_pypozyx_version = True
    if check_pypozyx_version:
        perform_latest_version_check()

    # shortcut to not have to find out the port yourself.
    serial_port = get_first_pozyx_serial_port()
    if serial_port is None:
        print("No Pozyx connected. Check your USB cable or your driver!")
        quit()

    # IDs of the tags to position, add None to position the local tag as well.
    # tag_ids = [0x1000, 0x1001, 0x1002, 0x1003, 0x1004]
    tag_ids = [0x1000]

    # only show id in log
    log_tag_ids = [0x1000]

    # necessary data for calibration
    anchors = [DeviceCoordinates(0xa000, 1, Coordinates(0, 0, 2500)),
               DeviceCoordinates(0x6968, 1, Coordinates(0, 3100, 2500)),
               DeviceCoordinates(0x6945, 1, Coordinates(1900, 0, 2500)),
               DeviceCoordinates(0x696b, 1, Coordinates(1900, 3100, 2500))]

    # create a pozyx object
    pozyx = PozyxSerial(serial_port)

    # latency calculation
    calculate_latency = True
    latency_tag = 0x1000
    latency_samples = 50

    # create a new multitag object
    r = MultitagPositioning(pozyx, tag_ids, anchors, log_tag_ids,
                            calculate_latency, latency_tag, latency_samples)

    # setup the thingy
    r.setup()

    # check if we need to loop or not
    loop = True

    # do the logic
    if loop:
        while True:
            r.loop()
    else:
        r.loop()
