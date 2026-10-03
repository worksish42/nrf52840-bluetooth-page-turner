{\rtf1\ansi\ansicpg1252\cocoartf2870
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import time\
import board\
import digitalio\
import alarm\
\
from adafruit_ble import BLERadio\
from adafruit_ble.advertising import Advertisement\
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement\
from adafruit_ble.services.standard.hid import HIDService\
\
from adafruit_hid.keyboard import Keyboard\
from adafruit_hid.keycode import Keycode\
\
\
# ============================================================\
# SETTINGS\
# ============================================================\
\
DEVICE_NAME = \'abBT page turner\'bb\
\
# Enter deep sleep after 10 minutes without a button press.\
SLEEP_AFTER = 600\
\
\
# ============================================================\
# BUTTONS\
# ============================================================\
\
# Physical order:\
# button1 = 020\
# button2 = 100\
# button3 = 106\
\
button1 = digitalio.DigitalInOut(board.P0_20)\
button1.direction = digitalio.Direction.INPUT\
button1.pull = digitalio.Pull.UP\
\
button2 = digitalio.DigitalInOut(board.P1_00)\
button2.direction = digitalio.Direction.INPUT\
button2.pull = digitalio.Pull.UP\
\
button3 = digitalio.DigitalInOut(board.P1_06)\
button3.direction = digitalio.Direction.INPUT\
button3.pull = digitalio.Pull.UP\
\
# ============================================================\
# BLUETOOTH HID\
# ============================================================\
\
hid = HIDService()\
keyboard = Keyboard(hid.devices)\
\
ble = BLERadio()\
ble.name = DEVICE_NAME\
\
advertisement = ProvideServicesAdvertisement(hid)\
advertisement.appearance = 961\
\
scan_response = Advertisement()\
scan_response.complete_name = DEVICE_NAME\
\
\
# ============================================================\
# FUNCTIONS\
# ============================================================\
\
def wait_for_release(button):\
    while not button.value:\
        time.sleep(0.01)\
\
    # Small debounce delay\
    time.sleep(0.03)\
\
\
def go_to_sleep():\
    print("Sleeping...")\
\
    # Release the GPIO pins before using them as wake alarms.\
    button1.deinit()\
    button2.deinit()\
    button3.deinit()\
\
    if ble.advertising:\
        ble.stop_advertising()\
\
    wake1 = alarm.pin.PinAlarm(\
        pin=board.P0_20,\
        value=False,\
        pull=True\
    )\
\
    wake2 = alarm.pin.PinAlarm(\
        pin=board.P1_00,\
        value=False,\
        pull=True\
    )\
\
    wake3 = alarm.pin.PinAlarm(\
        pin=board.P1_06,\
        value=False,\
        pull=True\
    )\
\
    alarm.exit_and_deep_sleep_until_alarms(\
        wake1,\
        wake2,\
        wake3\
    )\
\
# ============================================================\
# MAIN\
# ============================================================\
\
last_activity = time.monotonic()\
\
print("Starting fkn page turner")\
\
while True:\
\
    # --------------------------------------------------------\
    # BLUETOOTH CONNECTION\
    # --------------------------------------------------------\
\
    if not ble.connected:\
        if not ble.advertising:\
            print("Advertising...")\
            ble.start_advertising(\
                advertisement,\
                scan_response\
            )\
\
    # --------------------------------------------------------\
    # BUTTON 1 \'97 GPIO 020\
    # --------------------------------------------------------\
\
    if not button1.value:\
        print("BUTTON 1")\
\
        if ble.connected:\
            keyboard.send(Keycode.LEFT_ARROW)\
\
        last_activity = time.monotonic()\
        wait_for_release(button1)\
\
    # --------------------------------------------------------\
    # BUTTON 2 \'97 GPIO P1_00\
    # --------------------------------------------------------\
\
    if not button2.value:\
        print("BUTTON 2")\
\
        if ble.connected:\
            keyboard.send(Keycode.ENTER)\
\
        last_activity = time.monotonic()\
        wait_for_release(button2)\
\
    # --------------------------------------------------------\
    # BUTTON 3 \'97 GPIO P1_06\
    # --------------------------------------------------------\
\
    if not button3.value:\
        print("BUTTON 3")\
\
        if ble.connected:\
            keyboard.send(Keycode.RIGHT_ARROW)\
\
        last_activity = time.monotonic()\
        wait_for_release(button3)\
\
    # --------------------------------------------------------\
    # AUTO SLEEP\
    # --------------------------------------------------------\
\
    if time.monotonic() - last_activity >= SLEEP_AFTER:\
        go_to_sleep()\
\
    time.sleep(0.01)}