# 3. Calling Methods

## dbusGet.py
---
This script is an example of how to retrieve the value of a property called 'hostname' which is the host name of the current machine.

It does this by first connecting to the D-Bus system bus.

It then creates a proxy object of the remote object called:
    
    /org/freedesktop/hostname1
using the interface of the service,

    org.freedesktop.hostname1
Since we want to call the Get method of the org.freedesktop.DBus.Properties interface, we obtain a reference to it.

Finally, it calls the interfaces Get method to retrieve the Hostname property.

## dbusGetAll.py
---
This script is nearly the same as the previous one except it also calls the GetAll method of the following interface:

    org.freedesktop.DBus.Properties
GetAll returns a dictionary of all the supported properties.

## Condensed

In the folder condensed the GetAll example is repeated but condensed to not save the proxy object as it is only called once to create an interface object.