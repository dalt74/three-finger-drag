Implement three-finger-drag and three-finger-select for a
libinput-capable environments like GNOME/KDE.

Presetup:

1. Install xdotool / ydotool:
   # dnf install xdotool ydotool

2. Make sure you can access /dev/input/event* from your
   user context. There are many ways to do it: console.perms,
   udev, others. I just added my account into "input" group:
   # usermod -a -G input viking

3. Enable libinput events. For the GNOME environment it can
   be performed with command line:
   $ gsettings set org.gnome.desktop.peripherals.touchpad send-events enabled
   or through dconf-editor UI

4. Run scroll-handler:
   $ scroll-handler.py

What scroll-handler will do?

1. It scans input devices
2. Selects first device that has "touchpad" within it's name
3. Uses the device to emulate left mouse click/drag on three-finger gestures
