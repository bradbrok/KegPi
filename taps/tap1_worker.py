#!/usr/bin/python

"""
KegPi

The tastiest solution to monitor your keggerator.
"""

from flowmeter import *
import os
import sys
import time
import RPi.GPIO as GPIO
import sqlite3
from kegpi.bevdb import *

#FlowMeter class.
f = FlowMeter()
bevdb = BevDataBase()

#This will soon update when I get around to using this app.
beers_drank_while_coding_this = "13"

db = sqlite3.connect('beverage_db', check_same_thread=False)
cursor = db.cursor()
bevdb.beers_init()

#Flow meter pins on GPIO based on BCM layout.
flow_pin_tap1 = 23

#Initialize the GPIO pins, and set our callback to call update method.
GPIO.setmode(GPIO.BCM)
GPIO.setup(flow_pin_tap1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#This is the def for the callback for either tap.
def to_pi_tap1(channel):
    taps.set_tap(1)
    f.update()
    f.calibration = bevdb.calibration1()

#Add the event detection to trigger callback.
GPIO.add_event_detect(flow_pin_tap1, GPIO.RISING, callback=to_pi_tap1)

#Called when the pour event happens.
def update_db():
    time_pour = time.strftime('%I:%M %p')
    date_pour = time.strftime('%m/%d/%y')
    clicks = f.last_clicks
    ml_pour = f.to_ml
    oz_pour = f.last_pour_oz
    cursor.execute('''INSERT INTO bevs_tap1(time_pour, date_pour, clicks, ml_pour, oz_pour)
    VALUES (?,?,?,?,?)''', (time_pour, date_pour, clicks, ml_pour, oz_pour))
    db.commit()
    f.pour_event_occured = False

try:
    while True:
        time.sleep(1)
        f.last_pour_func()
        if f.pour_event_occured == True:
            update_db()
        else:
            pass

except KeyboardInterrupt:
    print "Goodbye, enjoy your delicious beverages!"
    GPIO.cleanup()
    db.close()
    sys.exit()
