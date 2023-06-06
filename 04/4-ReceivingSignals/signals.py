#!/usr/bin/python3
# 
# Testing function which generates dbus signals
# This program starts an event loop that repeats greetings that are passed to the bus
#
# To use this program, run it in one terminal and in another send a message onto the dbus system bus
#   with the following command:
#       
#       $ dbus-send --system --type=signal / com.example.greeting.GreetingSignal string:"howdy"
# 
#   and in the window running this program will print out "howdy" as the callback function, 
#       greeting_signal_received(), reacts to that signal

import dbus
import dbus.mainloop.glib
from gi.repository import GLib

# Event loop initialization
mainloop = None

# Function to receive callbacks when the signal comes
def greeting_signal_received(greeting):
    print(greeting)

# When exporting objects or receiving signals we must attach to a main loop
#   This line attaches the main loop
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

# Connect to system bus
bus = dbus.SystemBus()

# Registering to receive the signal
#   The dbus_interface could be anything we wish as it is an example.
#   Same goes for signal_name as long as both of theses names match the args 
#   in your dbus-send command
bus.add_signal_receiver(greeting_signal_received,
                        dbus_interface = "com.example.greeting",
                        signal_name = "GreetingSignal")

# Acquire and start a main loop
mainloop = GLib.MainLoop()
mainloop.run()