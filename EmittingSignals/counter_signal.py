#!/usr/bin/python3

import dbus
import dbus.service
import dbus.mainloop.glib
from gi.repository import GLib
import time

# Event loop initialization
mainloop = None

# Create a class that is a subclass of dbus.service.Object
class Counter(dbus.service.Object):
    # Constructor method of class which accepts a bus as an arg
    def __init__(self, bus):
        # Identifying path value known to bus once object is exported
        self.path = '/com/example/calculator'
        self.c = 0
        # Call to constructor of superclass dbus.service.Object
        #   This exports the object and should now be known to the bus
        dbus.service.Object.__init__(self, bus, self.path)

    # Decorate the function as a signal with the interface com.example.Counter
    @dbus.service.signal('com.example.Counter')
    def CounterSignal(self, counter):
        # The function doesn't need to do anything but the pass is
        # required to make the syntax valid
        pass

    # A function which call the CounterSignal function
    def emitCounterSignal(self):
        self.CounterSignal(self.c)
    
    def increment(self):
        self.c = self.c + 1
        print(self.c)


# Exported objects or receiving signals must always be attached to a main loop
#   This call does this
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

# Connect to system bus
bus = dbus.SystemBus()

# Create a Counter instance called calc passing which bus to use
counter = Counter(bus)

# Our own event loop which sends the signal every second
while True:
    counter.increment()
    counter.emitCounterSignal()
    time.sleep(1)