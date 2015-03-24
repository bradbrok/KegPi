"""
KegPi

The tastiest solution to monitor your keggerator.
"""

from flowmeter import *
import os
import sys
import time
import RPi.GPIO as GPIO
import ConfigParser
import sqlite3

#This will soon update when I get around to using this app.
beers_drank_while_coding_this = "9"

#The ini settings to load calibration constants from.
config = ConfigParser.ConfigParser()
config.read("tap_config.ini")

#Database config.
db = sqlite3.connect('beverage_db')
cursor = db.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS bevs_tap1(id INTEGER PRIMARY KEY, time_pour TEXT, date_pour TEXT,
    clicks INTEGER, ml_pour NUMERIC, oz_pour NUMERIC, pour_count INTEGER)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS bevs_tap2(id INTEGER PRIMARY KEY, time_pour TEXT, date_pour TEXT,
    clicks INTEGER, ml_pour NUMERIC, oz_pour NUMERIC, pour_count INTEGER)''')
#db.commit()

#FlowMeter class.
f = FlowMeter()

#Flow meter pins on GPIO based on BCM layout.
flow_pin_tap1 = 23
flow_pin_tap2 = 24

#Initialize the GPIO pins, and set our callback to call update method.
GPIO.setmode(GPIO.BCM)
GPIO.setup(flow_pin_tap1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(flow_pin_tap2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

tap = 1

#This is the def for the callback for either tap.
def to_pi_tap1(channel):
    tap = 1
    f.update()
    f.calibration = float(config.get('taps', 'calibration_0'))

def to_pi_tap2(channel):
    tap = 2
    f.update()
    f.calibration = float(config.get('taps', 'calibration_1'))


#Add the event detection to trigger callback.
GPIO.add_event_detect(flow_pin_tap1, GPIO.RISING, callback=to_pi_tap1)
GPIO.add_event_detect(flow_pin_tap2, GPIO.RISING, callback=to_pi_tap2)

#Called when the pour event happens.
def update_db():
    time_pour = time.time()
    date_pour = time.ctime()
    clicks = f.last_clicks
    ml_pour = f.to_ml
    oz_pour = f.last_pour_oz
    if (tap == 1):
        cursor.execute('''INSERT INTO bevs_tap1(time_pour, date_pour, clicks, ml_pour, oz_pour)
        VALUES (?,?,?,?,?)''', (time_pour, date_pour, clicks, ml_pour, oz_pour))
        db.commit()
    elif (tap == 2):
        cursor.execute('''INSERT INTO bevs_tap2(time_pour, date_pour, clicks, ml_pour, oz_pour)
        VALUES (?,?,?,?,?)''', (time_pour, date_pour, clicks, ml_pour, oz_pour))
        db.commit()
    else:
        print "No data for tap can be recorded. Something went wrong."
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
