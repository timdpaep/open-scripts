#!/usr/bin/env python3
"""
Pozyx basic troubleshooting (c) Pozyx Labs 2017
If you're experiencing trouble with Pozyx, this should be your first step to check for problems.
Please read the article on https://www.pozyx.io/Documentation/Tutorials/troubleshoot_basics/Python
"""

from pypozyx import (PozyxSerial, Data, AlgorithmData, get_first_pozyx_serial_port, FilterData,
                     PozyxConstants, DeviceList, POZYX_SUCCESS, UWBSettings, PozyxRegisters, SingleRegister)
from pypozyx.structures.device_information import DeviceDetails
from pypozyx.definitions.registers import POZYX_WHO_AM_I


def readable_sensor_mode(number):
    modes = [
        "Non-fusion mode: All meters off (MODE_OFF)",
        "Non-fusion mode: Accelorometer Only (ACCONLY)",
        "Non-fusion mode: Magnetometer Only (MAGONLY)",
        "Non-fusion mode: Gyroscope Only (GYROONLY)",
        "Non-fusion mode: Accelorometer & Magnetometer (ACCMAGx)",
        "Non-fusion mode: Accelorometer & Gyroscope (ACCGYRO)",
        "Non-fusion mode: Magnetometer & Gyroscope (MAGGYRO)",
        "Non-fusion mode: All (AMG)",
        "Fusion mode: IMU",
        "Fusion mode: COMPASS",
        "Fusion mode: M4G",
        "Fusion mode: NDOF_FMC_OFF",
        "Fusion mode: NDOF",
    ]
    return modes[number]


def device_check(pozyx, remote_id=None):
    system_details = DeviceDetails()
    pozyx.getDeviceDetails(system_details, remote_id=remote_id)

    # General Information
    print("")
    print("General Information")
    print("-----------------------------------")
    print("")
    print("\tLocal %s with id 0x%0.4x" %
          (system_details.device_name, system_details.id))
    print("\t-----------------------------------")
    print("")
    print("\tWho am i: 0x%0.2x" % system_details.who_am_i)
    print("\tFirmware version: v%s" % system_details.firmware_version_string)
    print("\tHardware version: v%s" % system_details.hardware_version_string)
    print("\tSelftest result: %s" % system_details.selftest_string)
    print("\tError: 0x%0.2x" % system_details.error_code)
    print("\tError message: %s" % system_details.error_message)
    operation_mode = SingleRegister()
    pozyx.getOperationMode(operation_mode)
    if operation_mode == PozyxConstants.TAG_MODE:
        print("\tDevice Type: Tag")
    else:
        print("\tDevice Type: Anchor")
    print("")

    # Positioning Settings
    print("POSITIONING SETTINGS")
    print("-----------------------------------")
    print("")

    # What are you?
    print("")

    # UWB Settings
    print("\tUWB settings")
    print("\t-----------------------------------")
    uwb_settings = UWBSettings()
    pozyx.getUWBSettings(uwb_settings, remote_id=remote_id)
    print("\t%s" % uwb_settings)
    print("")

    # Filter
    print("\tFilter")
    print("\t-----------------------------------")
    filter_data = FilterData()
    pozyx.getPositionFilterData(filter_data)
    print("\t%s" % filter_data)
    print("")

    # Positioning Algorithm
    print("\tAlgorithm")
    print("\t-----------------------------------")
    algorithm_data = AlgorithmData()
    pozyx.getPositioningAlgorithmData(algorithm_data)
    print("\t%s" % algorithm_data)
    print("")

    # Update Interval
    print("\tUpdate Interval")
    print("\t-----------------------------------")
    update_interval = Data([0])
    pozyx.getUpdateInterval(update_interval)
    print("\t%sms" % update_interval)
    print("")

    # Update Interval
    print("\tRanging Protocol")
    print("\t-----------------------------------")
    ranging_protocol = SingleRegister()
    pozyx.getRangingProtocol(ranging_protocol)
    if ranging_protocol == PozyxConstants.RANGE_PROTOCOL_PRECISION:
        print("\tPrecision")
    if ranging_protocol == PozyxConstants.RANGE_PROTOCOL_FAST:
        print("\tFast")
    print("")

    # Sensors Mode
    print("\tSensors Mode")
    print("\t-----------------------------------")
    sensors_mode = SingleRegister()
    pozyx.getSensorMode(sensors_mode)
    print("\t%s" % readable_sensor_mode(int(str(sensors_mode), 16)))
    print("")

    # Anchor Settings
    print("ANCHOR SETTINGS")
    print("-----------------------------------")
    print("")

    # Anchor Selection Mode
    print("\tAnchor Selection Mode")
    print("\t-----------------------------------")
    anchor_selection_mode = SingleRegister()
    pozyx.getAnchorSelectionMode(anchor_selection_mode)
    if anchor_selection_mode == PozyxConstants.ANCHOR_SELECT_MANUAL:
        print("\tFixed anchors: the anchor network IDs that have been supplied by POZYX_POS_SET_ANCHOR_IDS are used for positioning.")
    if anchor_selection_mode == PozyxConstants.ANCHOR_SELECT_AUTO:
        print("\tAutomatic anchor selection: Anchors from the internal anchor list are used to make the selection.")
    print("")

    # Get number of anchors
    print("\tAnchors")
    print("\t-----------------------------------")
    number_of_anchors = SingleRegister()
    pozyx.getNumberOfAnchors(number_of_anchors)
    anchor_list = DeviceList(list_size=number_of_anchors[0])
    pozyx.getPositioningAnchorIds(anchor_list)
    print("\tThere are {} anchors in my list.".format(
        int(str(number_of_anchors), 16)))
    print("\t%s" % anchor_list)
    print("")

    # Registers
    print("THERE ARE %s SAVED REGISTERS" %
          pozyx.getNumRegistersSaved(remote_id=remote_id))
    print("-----------------------------------")
    print("")
    saved_registers = pozyx.getSavedRegisters(remote_id=remote_id)
    if saved_registers:
        print("\tFilled in positioning registers: ")
        print("\t-----------------------------------")
        for register, register_name in zip(PozyxRegisters.ALL_POSITIONING_REGISTERS, ["Filter", "Algorithm & Dimension", "Ranging protocol", "Height"]):
            byte_num = int(register / 8)
            bit_num = register % 8
            register_saved = bool(saved_registers[byte_num] >> bit_num & 0x1)
            print("\t{}: {}".format(register_name, register_saved))
        print("")
        print("\tFilled in UWB registers: ")
        print("\t-----------------------------------")
        for register, register_name in zip(PozyxRegisters.ALL_UWB_REGISTERS, ["Channel", "Bitrate & PRF", "Preamble length", "Gain"]):
            byte_num = int(register / 8)
            bit_num = register % 8
            register_saved = bool(saved_registers[byte_num] >> bit_num & 0x1)
            print("\t{}: {}".format(register_name, register_saved))
        print("")
    else:
        print("Failed to retrieve saved registers.")
        print("")

    # Discover
    pozyx.clearDevices(remote_id)
    if pozyx.doDiscovery(discovery_type=PozyxConstants.DISCOVERY_ALL_DEVICES, remote_id=remote_id) == POZYX_SUCCESS:
        print("Found devices")
        print("-----------------------------------")
        pozyx.printDeviceList(remote_id, include_coordinates=False)
        print("")


if __name__ == '__main__':
    serial_port = get_first_pozyx_serial_port()
    if serial_port is None:
        print("No Pozyx connected. Check your USB cable or your driver!")
        quit()

    # get the pozyx
    pozyx = PozyxSerial(serial_port)

    # do a device check
    device_check(pozyx)
