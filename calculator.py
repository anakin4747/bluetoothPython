#!/usr/bin/python3
#
# To use this script you must run it in one window and interact with it on d-feet

import dbus
import dbus.service
import dbus.mainloop.glib
from gi.repository import GLib

# Event loop initilaization
mainloop = None

# Create a class that is a subclass of dbus.service.Object
class Calculator(dbus.service.Object):
    # Constructor method of class which accepts a bus as an arg
    def __init__(self, bus):
        # Identifying path value known to bus once object is exported
        self.path = '/com/example/calculator'
        # Call to constructor of superclass dbus.service.Object
        #   This exports the object and should now be known to the bus
        dbus.service.Object.__init__(self, bus, self.path)

    # This indicates that the following function should be exposed as dbus method
    #   com.example.calculator_interface is the name of the dbus interface
    @dbus.service.method("com.example.calculator_interface",
                        # The input signiture of the method has 2 int args
                         in_signature='ii',
                        # The output signiture of the method has 1 int output
                         out_signature='i')
    # Decorated function
    def Add(self, a1, a2):
        sum = a1 + a2
        print(a1, " + ", a2, " = ", sum)
        return sum

# Exported objects or receiving signals must always be attached to a main loop
#   This call does this
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

# Connect to system bus
bus = dbus.SystemBus()

# Create a Calculator instance called calc passing which bus to use
calc = Calculator(bus)

# Create MainLoop instance
mainloop = GLib.MainLoop()
print("Waiting for some calculations to do ...")
# Run mainloop
mainloop.run()