import subprocess
import sys
import threading
import time


pattern = "touchpad"
"""Pattern for device to be tracked"""

MODE_READY = 0
MODE_ACTING = 1
MODE_WAITING = 2

class GestureHandler(object):
    def __init__(self, scale=1, sleep_interval=1.2):
        self.lock = threading.RLock()
        self.mode = MODE_READY
        self.scale = scale
        self.serial = 0
        self.double_lag = sleep_interval

    def start(self):
        with self.lock:
            self._start_activity()

    def end(self, forced=False):
        with self.lock:
            if not forced:
                threading.Thread(target=self._commit, args=[self.serial]).start()
            elif self.mode != MODE_READY:
                self._end_activity()

    def handle(self, x, y):
        with self.lock:
            dx = x * self.scale
            dy = y * self.scale
            execute("xdotool mousemove_relative -- %s %s" % (dx, dy))

    def _end_activity(self):
        with self.lock:
            execute("xdotool mouseup 1")
            self.mode = MODE_READY

    def _start_activity(self):
        with self.lock:
            self.serial += 1
            if self.mode != MODE_WAITING:
                execute("xdotool mousedown 1")
            self.mode = MODE_ACTING

    def _commit(self, serial):
        self.mode = MODE_WAITING
        time.sleep(self.double_lag)
        with self.lock:
            if self.mode == MODE_WAITING and self.serial == serial:
                self._end_activity()


def execute(cmdline):
    try:
        subprocess.call(cmdline.split())
    except Exception as err:
        print("Error: %s" % err)


def run_loop(device, handler):
    with subprocess.Popen(
        ("stdbuf -oL -- libinput debug-events %s" % device).split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        bufsize=0
    ) as child:
        while True:
            try:
                child.wait(timeout=0)
                break
            except subprocess.TimeoutExpired:
                data = child.stdout.readline().decode("utf-8").replace("\n", "")
            parts = data.split("\t")
            action = parts[0].split()
            if action[1] == "POINTER_AXIS" or action[1] == "POINTER_MOTION":
                handler.end(True)
            elif action[1].startswith("GESTURE_SWIPE"):
                fingers = parts[1][0:1]
                if not data:
                    continue
                elif action[1] == "GESTURE_SWIPE_BEGIN" and fingers == "3":
                    handler.start()
                elif action[1] == "GESTURE_SWIPE_END" and fingers == "3":
                    handler.end()
                elif action[1] == "GESTURE_SWIPE_UPDATE" and fingers == "3":
                    remn = parts[1][1:].strip().split("/")
                    x = remn[0]
                    y = remn[1].split()[0]
                    handler.handle(float(x), float(y))


def list_devices():
    """Returns list of tuples (device_name, device_file)"""
    devices = []
    current_device = {}
    with subprocess.Popen(
        "libinput list-devices".split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        bufsize=0
    ) as child:
        while True:
            data = child.stdout.readline().decode("utf-8").replace("\n", "")
            if not data:
                if not current_device:
                    child.terminate()
                    child.wait()
                    break
                else:
                    if ("device" in current_device) and ("kernel" in current_device):
                        devices.append((current_device["kernel"], current_device["device"]))
                    current_device = {}
            else:
                tokens = [x.strip() for x in data.split(":")]
                if len(tokens) > 1:
                    key = tokens[0].lower()
                    tokens.pop(0)
                    value = ":".join(tokens)
                    current_device[key] = value
    return devices


def find_device_file(device_list, pattern):
    for dev in device_list:
        name = dev[1].lower()
        if name.find(pattern.lower()) >= 0:
            return dev
    return None


devices = list_devices()
device_info = find_device_file(devices, pattern)
if device_info is None:
    print("Unable to find gesturable device. The devices known are:")
    for device_info in devices:
        print("%s => %s" % device_info)
    print("Aborting")
    exit(1)

print("Found device: %s => %s" % device_info)
handler = GestureHandler()
run_loop(device_info[0], handler)
