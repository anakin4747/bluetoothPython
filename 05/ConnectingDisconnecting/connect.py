#!/usr/bin/python3

import bluetooth_utils
import bluetooth_constants
import dbus
import sys

# Define variables so they can be referenced before use
bus = None
device_interface = None

def connect(device_path):
    global bus
    global device_interface

    try:
        device_interface.Connect()
    except Exception as e:
        print("Failed to connect")
        print(e.get_dbus_name())
        print(e.get_dbus_message())
        if("UnknownObject" in e.get_dbus_name()):
            print("Try scanning first to resolve this problem")
        return bluetooth_constants.RESULT_EXCEPTION
    else:
        print("Connected OK")
        return bluetooth_constants.RESULT_OK
    
if(len(sys.argv) != 2):
    print("Wrong Usage")
    sys.exit(1)

bdaddr = sys.argv[1]

bus = dbus.SystemBus()

adapter_path = bluetooth_constants.BLUEZ_NAMESPACE + bluetooth_constants.ADAPTER_NAME

device_path = bluetooth_utils.device_address_to_path(bdaddr, adapter_path)

device_proxy = bus.get_object(bluetooth_constants.BLUEZ_SERVICE_NAME, device_path)

device_interface = dbus.Interface(device_proxy, bluetooth_constants.DEVICE_INTERFACE)

print("Connecting to " + bdaddr)

connect(device_path)