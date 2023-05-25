# Learning Bluetooth, Python, D-BUS, and BlueZ on Linux

I am following along the bluetooth tutorial for linux developers found at https://www.bluetooth.com/bluetooth-resources/bluetooth-for-linux/

## Linux and Bluetooth Architecture

The BLE stack has two major blocks, the Host and the Controller.

The stack is modelled as follows

Host
--------------------
BlueZ implements the host layers of the stack

Controller
--------------------
The controller typically resides within a chip or another device. The BLE controller is referred to as an adapter in BlueZ documentation

Radio
--------------------
Antenna and RF

## HCI
---
HCI is the Host Controller Interface. It facilitates communication between the Host and the Controller. HCI can be implemented using UART, USB, Secure Digital (SD), and 3-wire UART.

## Applications
---
Applications run within the Host section of the stack running either GAP/GATT applications or Bluetooth mesh nodes.

Depending on what type of application is run a specific BlueZ daemon is run. For GAP/GATT the bluetoothd daemon runs. For Bluetooth mesh the bluetooth-meshd runs. Only one daemon can be running at a time.

These daemons serialize and handles all HCI traffic on behalf of the applications.

## D-Bus
---
The D-Bus handles interprocess communication between applications and between applications and a BlueZ daemon. D-Bus has its own deamon which manages this called the dbus-daemon.

D-Bus (more specifically the daemon) is the middle man between applications and BlueZ daemons.

There are two D-Bus buses. A system bus and a session bus.

A process which connects to a message bus is called a client. A process which listens for and accepts a connection is called a server. 

When an applications connects to the bus it is dynamically allocated a unique name which looks like, :1.16.

### Objects
---
Applications using the D-Bus contain various objects.

Objects implement interfaces which consist of one or more methods.

Interfaces have dot-separated names similar to domain names. 

For example,

    org.freedesktop.DBus.Introspectable
    org.bluez.GattManager1

An application can call a method of an object owned by another application by sending messages over the bus. Method can possibly return a result over the bus.

Objects must be registered with dbus-deamon to allow this feature.

Registering an object is called exporting an object. Each object gets a unique identifier which takes the form of a path.

    /org/bluez/hci0/dev_4C_D7_64_CD_22_0A

### Servers
---
A server is an application which exposes an object to the bus for use as a service.

### Signals
---
An interface of an object can emit signals. Signals are analogous to events. Applications can subscribe to or register an interest in receiving particular signals.

### Properties
---
An object can have properties. A property is an attribute whose value can be retrieved using a get operation and can be changes with a set operation. Properties are referenced by name and are accessible via an interface that the object implements.

### Proxy Objects
---
A proxy object represents a remote object in another application. The proxy object takes care of turning local method calls into sending and receiving of D-Bus messages. Proxy objects are an abstraction to provide a higher level interaction between applications and the bus.

### Static Names (Well-known Names)
---
Just like TCP/IP, applications can register names statically instead of dynamically. This is analogous to using a static IP instead of DHCP in TCP/IP. This is more common with system services such as BlueZ.

bluetoothd is a D-Bus server which owns the well known name:
    
    org.bluez
bluetooth-meshd owns the name:

    org.bluez.mesh

### Standard Interfaces
---
Standard interfaces exits which are often used when working with BlueZ. For example:

    org.freedesktop.DBus.ObjectManager
This interface defines the signals InterfacesAdded and InterfacesRemoved. The InterfacesAdded signal is emitted when BlueZ discovers a new device and the InterfacesRemoved signal is emitted when the device is no longer known to BlueZ.

It also defines the method GetManagedObjects which allows applications to discover all the objects that a process, which is connected to the D-Bus, possesses.

Another standard interface is:

    org.freedesktop.DBus.Properties
Which defines methods that allow property values to be retrieved or set. It also defines the signal PropertiesChanged which is emitted when an object's property changes.

### Data Types
---
DBus is programming language agnostic and supports typical data types such as numeric types, strings, arrays, and dictionaries.

The data type is indicated in a *type signature* in the header fields of messages. For example, a type specifier of a(ii) means the message contains an array (a) of structs, each containing two 32-bit int (ii)

Another data type that is common is a *variant*. It acts as a generic wrapper around other types (Analogous to casting as void??).

### Introspection
---
Introspection allows the disclosure of the objects supported, their methods, signals, and properties. An object can be described using XML and this description can be retrieved from a process using the standard method,

    org.freedesktop.DBus.Introspectable.Introspect

### Security Policies
---
D-Bus includes a framework which requires communication between services and their objects and methods tp be explicitly allowed or denied based on a configuration file.

## dbus-monitor
---
You can monitor either of D-Bus' buses by using dbus-monitor:

    $ sudo dbus-monitor --system
or

    $ sudo dbus-monitor --session
You will need to enable Eavesdropping by adding a config file called:

    /etc/dbus-1/system-local.conf

## dbus-send
---
Another command line tool is dbus-send. This allows you to inject messages onto a D-Bus bus.

    $ dbus-send --system --type=signal / com.studyguide.greeting_signal string:"Hello World"
This will put the message "Hello World" of type string on the system bus.