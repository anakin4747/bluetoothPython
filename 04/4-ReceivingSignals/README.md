# 4. Receiving Signals

Signals are messages which an application might receive asynchronously.
To receive a specific signal, an application must register its interest with the bus it is connected to and also provide a callback function which is run in response to receiving the signal.

To asynchronously receive anything in a DBus application requires the use of an event loop. Event loops cause the applications to block.

The application can execute signal handler functions that execute when the signal is called.

The implementation of an event loop used is Glib. See https://docs.gtk.org/glib/main-loop.html for documentation.

## signals.py

This script registers for a signal which delivers a string value as an argument and prints the argument whenever the expected signal is received.

Instead of writing another script to generate signals on the D-Bus system bus, we can use the CLT dbus-send.

The script defines a function "greeting_signal_received" which is run when the signal is detected on the bus. 

The script then connects to the system bus and registers to receive a GreetingSignal on the D-Bus interface:

    com.example.greeting
and attaches the greeting_signal_received as the call back function.

To see this code in action run this script in one window and in another run the following command:

    $ dbus-send --system --type=signal / com.example.greeting.GreetingSignal string:"hello"
Change "hello" out with whatever you would like. This sends a signal (opposed to a method call) to the system bus. The forward slash is the object that owns the interface that emitted the signal. In our case we're using the root path.

You should see the text "hello" printed out by your running process. This is the callback function in action.