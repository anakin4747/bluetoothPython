# 6. Emitting Signals

For a process to send signals it needs to be exported in the same fashion as receiving signals.

## counter_signal.py

This script creates a Counter class which is a subclass of:

    dbus.service.Object
It is initailized with a object path identifier and a member c which is the count that is set to zero. The object id and bus are passed to the constructor of:

    dbus.service.Object
We then define a function that when called emits a signal to the bus. To make this function a signal we must decorate it with:

    @dbus.service.signal
and the name of the interface which will send the signal.

The Counter class has two other functions which call the decorated signal function and increment the count respectively.

It connects to the system bus and create a Counter instance. The program then loops endlessly incrementing the count and emitting the signal every second.

To see this script in action, run it and in another window run:

    $ dbus-monitor --system