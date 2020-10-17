Implement three-finger-drag and three-finger-select for a
libinput-capable environments like GNOME/KDE.

Install:

# cp src/three-finger-drage /usr/bin
# cp systemd/three-finger-drag.service /usr/lib/systemd/system
# systemctl daemon-reload

Modes supported:

1. User:
   works inside user session
   Requires proper permissions to access /dev/input/event*
   Uses ydotool daemon or xdotool to perform actions
   When using ydotool backend requires to access /tm/.ydotool_socket

   Activate mode:
   start /usr/bin/three-finger-drag in autostart

2. System:
   works as systemd service three-finger-scroll.service
   Explicit use ydotool, requires ydotool.service to be running
   You may specify your touchpad device in /etc/sysconfig/touchdev:
   TOUCHPAD_DEVICE_NAME=mytouchpad

   Activate mode:
   # systemctl enable three-finger-drag
