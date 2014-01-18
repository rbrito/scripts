#!/usr/bin/env python
"""
Python script to essentially perform the same as:

   gdbus call \
       --session \
       --dest org.gnome.SettingsDaemon \
       --object-path /org/gnome/SettingsDaemon/Power \
       --method org.gnome.SettingsDaemon.Power.Screen.SetPercentage 75

References:

    http://ask.fedoraproject.org/question/980/brightness-applet-on-gnome-panel
    http://en.wikibooks.org/wiki/Python_Programming/Dbus
    http://www.devtech.com/inhibitapplet
"""

dbus_stuff = {
    'gnome': {
        "service": "org.gnome.SettingsDaemon",
        "path": "/org/gnome/SettingsDaemon/Power",
        "interface": "org.gnome.SettingsDaemon.Power.Screen",
        "method": "SetPercentage"
    },
    'mate': {
        "service": "org.mate.PowerManager",
        "path": "/org/mate/PowerManager/Backlight",
        "interface": "org.mate.PowerManager.Backlight",
        "method": "SetBrightness"
    }
}

def set_brightness(desktop, percentage):
    what = dbus_stuff[desktop]

    session_bus = dbus.SessionBus()
    proxy = session_bus.get_object(what['service'], what['path'])
    dbus_int = dbus.Interface(proxy, what['interface'])
    set_percentage = dbus_int.get_dbus_method(what['method'])

    set_percentage(percentage)


if __name__ == '__main__':
    import os
    import sys

    import dbus

    if len(sys.argv) == 1:
        percentage = 40
    else:
        percentage = int(sys.argv[1])

    desktop = os.getenv('DESKTOP_SESSION', 'gnome')

    if desktop not in dbus_stuff:
        print("Implemented desktop")
        sys.exit(1)

    set_brightness(desktop, percentage)
