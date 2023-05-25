# 5. Receiving Method Calls
For applications to be able to receive method calls from other D-Bus services or emit its own signals it must register objects and any owned interfaces and their callable methods with a bus.

Methods are registered with a name and the signature of amy input arguments and return values.

The act of registering an object, it interfaces and callable methods in this way is known as exporting.

## calculator.py
