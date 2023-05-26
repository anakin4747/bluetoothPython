# 5. Receiving Method Calls
For applications to be able to receive method calls from other D-Bus services or emit its own signals it must register objects and any owned interfaces and their callable methods with a bus.

Methods are registered with a name and the signature of amy input arguments and return values.

The act of registering an object, its interfaces and callable methods in this way is known as exporting.

## calculator.py

This script creates a subclass of a dbus.service.Object. This act of subclassing automatically makes this object automatically support D-Bus introspection.

The class' constructor takes a bus as a parameter in our implementation.

The constructor sets the instance's path variable to the path identifier we choose for this object which is:

    /com/example/calculator
The bus and the objects path are both then passed to the constructor of the superclass,

    dbus.service.Object
We then create a decorated function for our class. This class receives the decorator:

    @dbus.service.method
This makes the following method available through the interface:

    com.example.calculator_interface
We also describe the IO of the method using the keyword arguments in_signature and out_signature. You will also need to specify the data types of the IO.

It then attaches a main loop.

Then creates a Calculator object passing the system bus to the constructor.

To use this script run it and then use D-Feet to analyze your object. 

To find it I had to scroll down to the bottom and found a dynamically allocated connection name like

    :1.258
    activatable: no, pid: 14152, cmd: /usr/bin/python3 ./calculator.py

Then find the Add Method in the interface of the object.
Open it, and type two ints into the Method input section and click execute. You should see the results of your method in the ./calculator.py process.