#!/usr/bin/python3
import dbus

SERVICE_NAME = 'org.freedesktop.hostname1'
REMOTE_OBJECT_NAME = '/org/freedesktop/hostname1'
DBUS_PROP_IFACE = 'org.freedesktop.DBus.Properties'

# Connect to the dbus system bus
bus = dbus.SystemBus()

# Create a proxy to the /org/freedesktop/hostname1 object owned by the 
#   org.freedesktop.hostname1 service and the proxy gets passed as the first arg
#   of dbus.Interface()
# Obtain a reference to the org.freedesktop.DBUS.Properties interface
#   since it has the methods we wish to call
interface = dbus.Interface(bus.get_object(SERVICE_NAME, REMOTE_OBJECT_NAME),
                           DBUS_PROP_IFACE)

# GetAll properties from the org.freedesktop.hostname1 service
all_props = interface.GetAll(SERVICE_NAME)
print(all_props)

PROPERTY = 'Hostname'
# Get the 'Hostname' property from the org.freedesktop.hostname1 service
hostname = interface.Get(SERVICE_NAME, PROPERTY)
print("The hostname is ", hostname)