#!/usr/bin/python3
import dbus
import dbus.mainloop.glib
from gi.repository import GLib

mainloop = None



dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)