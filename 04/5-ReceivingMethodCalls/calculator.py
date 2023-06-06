#!/usr/bin/python3

import dbus
import dbus.service
import dbus.mainloop.glib
from gi.repository import GLib

# Event loop initialization
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
                        # The input signature of the method has 2 int args
                         in_signature='ii',
                        # The output signature of the method has 1 int output
                         out_signature='i')
    def Add(self, a1, a2):
        sum = a1 + a2
        print(a1, " + ", a2, " = ", sum)
        return sum

    @dbus.service.method("com.example.calculator_interface",
                         in_signature='iii',
                         out_signature='i')
    # Function for adding 3 ints together
    def Add3(self, a1, a2, a3):
        sum = a1 + a2 + a3
        print(a1, " + ", a2, " + ", a3, " = ", sum)
        return sum

    # To know what to pass in these parameters google "dbus data notation"
    @dbus.service.method("com.example.calculator_interface",
                         in_signature='dd',
                         out_signature='d')
    # Function for adding double precision floating points
    def Add_Double(self, a1, a2):
        sum = a1 + a2
        print(a1, " + ", a2, " = ", sum)
        return sum

    @dbus.service.method("com.example.calculator_interface",
                         in_signature='yy', # y for bYtes
                         out_signature='y')
    # Function for ANDing 2 bytes
    def bitwise_And(self, a1, a2):
        result = a1 & a2
        print(f"{a1:0>8b} & {a2:0>8b} = {result:0>8b}")
        return result

# Exported objects or receiving signals must always be attached to a main loop
#   This call does this
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

# Connect to system bus
bus = dbus.SystemBus()

# Create a Calculator instance called calc passing which bus to use
calc = Calculator(bus)

# Just to show path attribute of object that is set in the constructor
print("Calculator object path: ", calc.path)

# Create MainLoop instance
mainloop = GLib.MainLoop()
print("Waiting for some calculations to do ...")
# Run mainloop
mainloop.run()