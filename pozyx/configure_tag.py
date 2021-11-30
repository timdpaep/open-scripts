"""
Configures a tag with UWB settings
"""

from pypozyx import (AlgorithmData, Data, PozyxSerial, FilterData,
                     SingleRegister, PozyxConstants, DeviceList, Coordinates,
                     get_first_pozyx_serial_port, PozyxConstants, POZYX_SUCCESS,
                     DeviceCoordinates, UWBSettings, PozyxRegisters)
from pypozyx.structures.generic import dataCheck


class ConfigureTag:
    def __init__(self, tags, pozyx, uwb_settings, filter,
                 filter_strength, positioning_algorithm,
                 dimension, update_interval, anchor_selection_mode,
                 ranging_protocol, sensor_mode, anchor_list,
                 save_to_flash=True):
        """"""
        self.pozyx = pozyx
        self.tags = tags

        # positioning
        self.uwb_settings = uwb_settings
        self.filter = filter
        self.filter_strength = filter_strength
        self.positioning_algorithm = positioning_algorithm
        self.dimension = dimension
        self.update_interval = update_interval
        self.ranging_protocol = ranging_protocol
        self.sensor_mode = sensor_mode

        # anchors
        self.number_of_anchors = self.get_number_of_anchors()
        self.anchor_selection_mode = anchor_selection_mode
        self.anchor_list = anchor_list
        self.save_to_flash = save_to_flash

        # do configuration
        self.configure()

    def configure(self):
        # print("")
        # print("Old Configuration")
        # print("-----------------------------------")
        # self.printConfiguration()
        print("")
        for tag in self.tags:
            if tag is None:
                print("Configuring local tag")
            else:
                print("Configuring tag %s" % hex(tag))
            self.change_uwb_settings(tag)
            self.change_filter(tag)
            self.change_algorithm(tag)
            self.change_update_interval(tag)
            self.change_anchor_selection_mode(tag)
            self.change_range_protocol(tag)
            self.change_sensor_mode(tag)
            self.set_anchors(tag)
            if self.save_to_flash:
                print('Saving registers...')
                self.save_registers(tag)
        print("")
        # print("New Configuration")
        # print("-----------------------------------")
        # self.printConfiguration()
        # print("")

    # Number of anchors
    def get_number_of_anchors(self):
        number_of_anchors = SingleRegister()
        pozyx.getNumberOfAnchors(number_of_anchors)
        return number_of_anchors[0]

    # UWB Settings

    def change_uwb_settings(self, remote_id=None):
        return self.pozyx.setUWBSettings(
            self.uwb_settings, remote_id, False)

    # Filter

    def change_filter(self, remote_id=None):
        self.pozyx.setPositionFilter(
            self.filter, self.filter_strength, remote_id)

    # Algorithm

    def change_algorithm(self, remote_id=None):
        self.pozyx.setPositionAlgorithm(
            self.positioning_algorithm, self.dimension, remote_id)

    # Update Interval
    def change_update_interval(self, remote_id=None):
        ms = SingleRegister(self.update_interval, size=2)
        self.pozyx.setWrite(PozyxRegisters.POSITIONING_INTERVAL, ms, remote_id)

    # Anchor Selection Mode
    def change_anchor_selection_mode(self, remote_id=None):
        self.pozyx.setSelectionOfAnchors(
            self.anchor_selection_mode, self.number_of_anchors, remote_id)

    # Change the ranging protocol
    def change_range_protocol(self, remote_id=None):
        ranging_protocol_register = SingleRegister(self.ranging_protocol)
        self.pozyx.setWrite(PozyxRegisters.RANGING_PROTOCOL,
                            ranging_protocol_register, remote_id)

    # Change the sensor mode
    def change_sensor_mode(self, remote_id=None):
        self.pozyx.setSensorMode(self.sensor_mode, remote_id)

    # Sets the anchors
    def set_anchors(self, remote_id=None):
        self.pozyx.clearDevices(remote_id)
        for anchor in self.anchor_list:
            if not dataCheck(anchor):
                anchor = DeviceCoordinates(
                    anchor[0], anchor[1], Coordinates(anchor[2], anchor[3], anchor[4]))
            self.pozyx.addDevice(anchor, remote_id)
        if len(self.anchor_list) < 3 or len(self.anchor_list) > 16:
            print("Not enough anchors to do positioning")

    # Saving

    def save_registers(self, remote_id=None):
        registers = PozyxRegisters.ALL_UWB_REGISTERS
        registers.append(PozyxRegisters.POSITIONING_FILTER)
        registers.append(PozyxRegisters.POSITIONING_ALGORITHM)
        registers.append(PozyxRegisters.POSITIONING_INTERVAL)
        registers.append(PozyxRegisters.POSITIONING_NUMBER_OF_ANCHORS)
        registers.append(PozyxRegisters.RANGING_PROTOCOL)
        self.pozyx.saveAnchorIds(remote_id)
        self.pozyx.saveRegisters(registers, remote_id)

    # Printing information

    def printConfiguration(self):
        self.printUwbSettings()
        self.printFilterSettings()
        self.printAlgorithmSettings()
        self.printUpdateInterval()
        self.printAnchorSelectionMode()
        self.printRangingProtocol()
        self.printSensorMode()

    def printUwbSettings(self):
        uwb_settings = UWBSettings()
        pozyx.getUWBSettings(uwb_settings)
        print("- UWB settings: %s" % uwb_settings)

    def printFilterSettings(self):
        filter_data = FilterData()
        self.pozyx.getPositionFilterData(filter_data)
        print("- FILTER: %s" % filter_data)

    def printAlgorithmSettings(self):
        algorithm_data = AlgorithmData()
        pozyx.getPositioningAlgorithmData(algorithm_data)
        print("- ALGORITHM: %s" % algorithm_data)

    def printUpdateInterval(self):
        update_interval = Data([0])
        pozyx.getUpdateInterval(update_interval)
        print("- UPDATE INTERVAL: %sms" % update_interval)

    def printAnchorSelectionMode(self):
        anchor_selection_mode = SingleRegister()
        pozyx.getAnchorSelectionMode(anchor_selection_mode)
        if anchor_selection_mode == PozyxConstants.ANCHOR_SELECT_MANUAL:
            print("- ANCHOR SELECTION MODE: Manual")
        if anchor_selection_mode == PozyxConstants.ANCHOR_SELECT_AUTO:
            print("- ANCHOR SELECTION MODE: Automatic")

    def printRangingProtocol(self):
        ranging_protocol = SingleRegister()
        pozyx.getRangingProtocol(ranging_protocol)
        if ranging_protocol == PozyxConstants.RANGE_PROTOCOL_PRECISION:
            print("- RANGING PROTOCOL: Precision")
        if ranging_protocol == PozyxConstants.RANGE_PROTOCOL_FAST:
            print("- RANGING PROTOCOL: Fast")

    def printSensorMode(self):
        sensors_mode = SingleRegister()
        pozyx.getSensorMode(sensors_mode)
        print("- SENSORS MODE: %s" % int(str(sensors_mode), 16))
        print("")


if __name__ == "__main__":
    # serial port
    serial_port = get_first_pozyx_serial_port()
    if serial_port is None:
        print("No Pozyx connected. Check your USB cable or your driver!")
        quit()

    # get the pozyx
    pozyx = PozyxSerial(serial_port)

    # sets the tags to configure
    tags = [None, 0x1000, 0x1001, 0x1002, 0x1003, 0x1004]
    # tags = [None]

    # set to True if needed to save to flash
    save_to_flash = True

    # set th new uwb_settings
    uwb_settings = UWBSettings(channel=1,
                               bitrate=1,
                               prf=2,
                               plen=0x04,
                               gain_db=24.5)

    # set the filter
    # PozyxConstants.FILTER_TYPE_NONE
    # PozyxConstants.FILTER_TYPE_MOVING_AVERAGE
    # PozyxConstants.FILTER_TYPE_MOVING_MEDIAN
    # PozyxConstants.FILTER_TYPE_FIR
    filter = PozyxConstants.FILTER_TYPE_NONE
    filter_strength = 0

    # set the positioning Algorithm
    # PozyxConstants.POSITIONING_ALGORITHM_UWB_ONLY
    # PozyxConstants.POSITIONING_ALGORITHM_TRACKING
    # PozyxConstants.POSITIONING_ALGORITHM_NONE
    positioning_algorithm = PozyxConstants.POSITIONING_ALGORITHM_TRACKING

    # set the dimension
    # PozyxConstants.DIMENSION_2D
    # PozyxConstants.DIMENSION_2_5D
    # PozyxConstants.DIMENSION_3D
    dimension = PozyxConstants.DIMENSION_3D

    # sets the update interval
    # Pozyx can be run in continuous mode to provide continuous positioning.
    # The interval in milliseconds between successive updates can be configured with this register.
    # The value is capped between 10ms and 60000ms (1 minute).
    # Writing the value 0 to this registers disables the continuous mode.
    update_interval = 0

    # sets the anchor selection mode
    # PozyxConstants.MANUAL
    # indicates fixed anchor set. The anchor network IDs that have been supplied by
    # POZYX_POS_SET_ANCHOR_IDS are used for positioning.
    # PozyxConstants.ANCHOR_SELECT_AUTO
    # indicates automatic anchor selection. Anchors from the internal anchor list
    # are used to make the selection.
    anchor_selection_mode = PozyxConstants.ANCHOR_SELECT_AUTO

    # sets the tag ranging mode
    # PozyxConstants.RANGE_PROTOCOL_PRECISION
    # This method provides accurate measurements in all UWB settings but takes the most time.
    # PozyxConstants.RANGE_PROTOCOL_FAST
    # This method is more than twice as fast as the PRECISION method, however,
    # it can only be used when ranging or positioning continuously.
    # Furthermore, the results in the first 100ms will be very inaccurate (up to a few meters in error). After this time, the algorithm will have stabilized and will give the same accuracy as the PRECISION method. This method is only guaranteed to work accurate for preamble lengths up to 1536.
    ranging_protocol = PozyxConstants.RANGE_PROTOCOL_FAST

    # sets the sensor mode
    # Possible values:
    # Non-fusion modes:
    # 0 : MODE_OFF
    # 1 : ACCONLY
    # 2 : MAGONLY
    # 3 : GYROONLY
    # 4 : ACCMAGx
    # 5 : ACCGYRO
    # 6 : MAGGYRO
    # 7 : AMG

    # Fusion modes:
    # 8 : IMU
    # 9 : COMPASS
    # 10 : M4G
    # 11 : NDOF_FMC_OFF
    # 12 : NDOF
    sensor_mode = 12

    # anchors on the device
    anchor_list = [DeviceCoordinates(0xa000, 1, Coordinates(0, 0, 2500)),
                   DeviceCoordinates(0x6968, 1, Coordinates(0, 3100, 2500)),
                   DeviceCoordinates(0x6945, 1, Coordinates(1900, 0, 2500)),
                   DeviceCoordinates(0x696b, 1, Coordinates(1900, 3100, 2500))]

    # configure the tag
    s = ConfigureTag(tags, pozyx, uwb_settings, filter,
                     filter_strength, positioning_algorithm,
                     dimension, update_interval, anchor_selection_mode,
                     ranging_protocol, sensor_mode, anchor_list, save_to_flash)
