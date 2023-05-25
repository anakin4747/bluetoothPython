#!/usr/bin/python3
# 
# Testing function which generates dbus signals
# This program starts an event loop that repeats greatings that are passed to the bus
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

# Event loop initilaization
mainloop = None

# Function to receive callbacks when the signal comes
def greeting_signal_received(greeting):
    print(greeting)

# Setting up mainloop properties
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

# Connect to system bus
bus = dbus.SystemBus()

# Registering to receive the signal
bus.add_signal_receiver(greeting_signal_received,
                        dbus_interface = "com.example.greeting",
                        signal_name = "GreetingSignal")

# Acquire and start a main loop
mainloop = GLib.MainLoop()
mainloop.run()