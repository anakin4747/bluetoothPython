#!/usr/bin/python3
import dbus

# Connect to the dbus system bus
bus = dbus.SystemBus()

# Create a proxy to the /org/freedesktop/hostname1 object owned by the 
#   org.freedesktop.hostname1 service
proxy = bus.get_object('org.freedesktop.hostname1', '/org/freedesktop/hostname1')

# Obtain a reference to the org.freedesktop.DBUS.Properties interface
#   since it has the methods we wish to call
interface = dbus.Interface(proxy, 'org.freedesktop.DBus.Properties')

# Get the 'Hostname' property from the org.freedesktop.hostname1 service
hostname = interface.Get('org.freedesktop.hostname1', 'Hostname')
print("The hostname is ", hostname)
