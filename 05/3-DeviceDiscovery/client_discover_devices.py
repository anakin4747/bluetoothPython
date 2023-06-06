#!/usr/bin/python3
from gi.repository import GLib
import bluetooth_utils
import bluetooth_constants
import dbus
import dbus.mainloop.glib
import sys

# Allocating variables
adapter_interface = None
mainloop = None
timer_id = None
devices = {}
managed_objects_found = 0


def get_known_devices(bus):
    global managed_objects_found
    # Get a reference to the object manager so that we can call GetManagedObjects
    object_manager = dbus.Interface(bus.get_object(bluetooth_constants.BLUEZ_SERVICE_NAME, "/"),
                                    bluetooth_constants.DBUS_OM_IFACE)
    managed_objects = object_manager.GetManagedObjects()

    for path, ifaces in managed_objects.items():
        for iface_name in ifaces:
            if iface_name == bluetooth_constants.DEVICE_INTERFACE:
                managed_objects_found += 1
                print("EXI path : ", path)
                device_properties = ifaces[bluetooth_constants.DEVICE_INTERFACE]
                devices[path] = device_properties
                if 'Address' in device_properties:
                    print("EXI bdaddr : ", bluetooth_utils.dbus_to_python(
                        device_properties['Address']))
                    print("----------------------------")


def properties_changed(interface, changed, invalidated, path):
    if interface != bluetooth_constants.DEVICE_INTERFACE:
        return
    if path in devices:
        devices[path] = dict(devices[path].items())
        devices[path].update(changed.items())
    else:
        devices[path] = changed

    dev = devices[path]
    print("CHG path :", path)
    if 'Address' in dev:
        print("CHG baddr: ", bluetooth_utils.dbus_to_python(dev['Address']))
    if 'Name' in dev:
        print("CHG name: ", bluetooth_utils.dbus_to_python(dev['Name']))
    if 'RSSI' in dev:
        print("CHG RSSI: ", bluetooth_utils.dbus_to_python(dev['RSSI']))
    print("-------------")


def interfaces_added(path, interfaces):
    # Interfaces is an array of dict entries
    # Ensure that the interface org.bluez.Adapter1 in interfaces
    # Or else the signal received does not relate to the discovery of a device
    if not bluetooth_constants.DEVICE_INTERFACE in interfaces:
        return

    device_properties = interfaces[bluetooth_constants.DEVICE_INTERFACE]

    if path not in devices:
        print("NEW path :", path)
        devices[path] = device_properties
        dev = devices[path]
        if 'Address' in dev:
            print("NEW bdaddr: ",
                  bluetooth_utils.dbus_to_python(dev['Address']))
        if 'Name' in dev:
            print("NEW name: ", bluetooth_utils.dbus_to_python(dev['Name']))
        if 'RSSI' in dev:
            print("NEW RSSI: ", bluetooth_utils.dbus_to_python(dev['RSSI']))
        print("---------------")


def interfaces_removed(path, interfaces):

    if not bluetooth_constants.DEVICE_INTERFACE in interfaces:
        return
    if path in devices:
        dev = devices[path]
        if 'Address' in dev:
            print("DEL bdaddr: ",
                  bluetooth_utils.dbus_to_python(dev['Address']))
        else:
            print("DEL path: ", path)
            print("---------------")
        del devices[path]


def list_devices_found():
    print("Full list of devices", len(devices), "discovered:")
    print("---------------------")
    for path in devices:
        dev = devices[path]
        print(bluetooth_utils.dbus_to_python(dev['Address']))


def discovery_timeout():
    global adapter_interface
    global mainloop
    global timer_id
    GLib.source_remove(timer_id)
    mainloop.quit()
    adapter_interface.StopDiscovery()
    bus = dbus.SystemBus()
    bus.remove_signal_receiver(interfaces_added, "InterfacesAdded")
    bus.remove_signal_receiver(interfaces_removed, "InterfacesRemoved")
    bus.remove_signal_receiver(properties_changed, "PropertiesChanged")
    list_devices_found()
    return True


def discover_devices(bus, timeout):
    global adapter_interface
    global mainloop
    global timer_id

    # The path to the adapter object is /org/bluez/hci0
    #   So this line is just /org/bluez/ + hci0
    adapter_path = bluetooth_constants.BLUEZ_NAMESPACE + \
        bluetooth_constants.ADAPTER_NAME

    # Acquire an adapter proxy object and its Adapter1 interface so we can call its methods
    # We do this by passing the service name, org.bluez, and the path to the object, /org/bluez/hci0
    adapter_object = bus.get_object(
        bluetooth_constants.BLUEZ_SERVICE_NAME, adapter_path)
    adapter_interface = dbus.Interface(
        adapter_object, bluetooth_constants.ADAPTER_INTERFACE)

    # Register signal handler functions so we can asynchronously report discovered devices
    # InterfacesAdded signal is emitted by BlueZ when an advertising packet from a device it doesn't know about is received
    bus.add_signal_receiver(interfaces_added,
                            # This signal belongs to org.freedesktop.DBus.ObjectManager (DBUS_OM_IFACE)
                            # Can be found in D-Feet at the connection name org.bluez,
                            # in the object '/' under the interface name
                            dbus_interface=bluetooth_constants.DBUS_OM_IFACE,
                            signal_name="InterfacesAdded")

    bus.add_signal_receiver(interfaces_removed,
                            # This signal belongs to org.freedesktop.DBus.ObjectManager (DBUS_OM_IFACE)
                            # Can be found in D-Feet at the connection name org.bluez,
                            # in the object '/' under the interface name
                            dbus_interface=bluetooth_constants.DBUS_OM_IFACE,
                            signal_name="InterfacesRemoved")

    bus.add_signal_receiver(properties_changed,
                            # This signal belongs to org.freedesktop.DBus.Properties
                            # Can be found at connection name org.freedesktop.DBus,
                            # in the object /org/freedesktop/DBus with the above interface name
                            dbus_interface=bluetooth_constants.DBUS_PROPERTIES,
                            signal_name="PropertiesChanged",
                            path_keyword="path")

    # Create an instance of an event loop
    mainloop = GLib.MainLoop()

    timer_id = GLib.timeout_add(timeout, discovery_timeout)

    # Call the StartDiscovery method from the org.bluez.Adapter1 interface
    adapter_interface.StartDiscovery(byte_arrays=True)

    # Start event loop
    mainloop.run()


# Ensure this script is ran with 1 argument
if (len(sys.argv) != 2):
    print("Wrong usage")
    sys.exit(1)

# Covert input to int and milliseconds
scantime = int(sys.argv[1]) * 1000

# dbus initialization steps
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

# Connect to system bus
bus = dbus.SystemBus()

print("Listing devices already known to BlueZ:")
get_known_devices(bus)
print("Scanning")
discover_devices(bus, scantime)
