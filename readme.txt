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
   When using ydotool backend requires to access /tmp/.ydotool_socket

   How to use user mode:
   # usermod -a -G input <myusername>
   start
      /usr/bin/three-finger-drag
   in yout DE autostart.
   If using ydotool don't forget to make socket and device
   user-accessible with console.perms, udev or other your preferred
   method

2. System:
   works as systemd service three-finger-scroll.service
   Explicit use ydotool, requires ydotool.service to be running
   You may specify your touchpad device in /etc/sysconfig/touchdev:
   TOUCHPAD_DEVICE_NAME=mytouchpad

   How to use system mode:
   # systemctl enable three-finger-drag
   # systemctl start three-finger-drag
   Maybe you'll need logout/login
