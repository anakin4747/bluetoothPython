# 3. Device Discovery

Device discovery is the procedure of a BLE central device can list the peripheral devices that are in range and advertizing.

Device discovery is more complicated in BlueZ than other architectures.

Remember that BlueZ (bluetoothd) supports one or more applications concurrently.

When BlueZ performs scanning, on discovering a device, an object representing the device is created and retained by BlueZ and exported to the D-Bus system bus. These are managed objects.

At the same time, a signal InterfacesAdded is emitted and this informs interested, connected D-Bus services of the newly discovered device.

If a InterfacesAdded signal is emitted and another application requests scanning shortly afterwards, any devices already known to BlueZ will not be reported again by signalling. This can be why some devices in range can miss being signalled when BlueZ is scanning.

To resolve this, the D-Bus org.bluez service exports a root object which implements a number of standard interfaces, including:

    org.freedesktop.DBus.ObjectManager

Applications can request the list of objects currently known to BlueZ by calling the GetManagedObjects method. These managed objects are not only devices. Devices are objects which implement the org.bluez.Device1 interface. org.bluez.Adapter1 represent Bluetooth adapters that the system has. So for an application to catch all devices they need to scan and obtain the managed objects list.

Discovered devices has a default timeout of 30 seconds before it is removed and a InterfaceRemoved signal is sent to indicate this. To change the timeout, you can edit the /etc/bluetooth/main.conf BlueZ config file. The property will be called TemporaryTimeout.

When one or more properties of a managed device object changes a signal called PropertiesChanged is emitted.

The standard procedure for obtaining a list of devices to consider connecting to is:
- Call GetManagedObjects on the ObjectManager interface
- Scan for new devices
- Concatenate these results
- Keep properties up to date by handling PropertiesChanged signals
- Remove devices as they appear in InterfaceRemoved signals

## Implementing Device Discovery

