"""
KegPi

The tastiest solution to monitor your keggerator.
"""

from flowmeter import *
#from kegs import *
import os
import time
import RPi.GPIO as GPIO
import threading
import ConfigParser

config = ConfigParser.ConfigParser()
config.read("tap_config.ini")

#This will soon update when I get around to using this app.
beers_drank_while_coding_this = "8"
f = FlowMeter()



#Flow meter pins on GPIO based on BCM layout.
flow_pin_tap1 = 23
#flow_pin_tap2 = 24

#Initialize the GPIO pins, and set our callback to call update method.
GPIO.setmode(GPIO.BCM)
GPIO.setup(flow_pin_tap1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(flow_pin_tap2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#This is the def for the callback.
def to_pi_tap1(channel):
	f.calibration = float(config.get('taps', 'calibration_0'))
	f.update()

#def to_pi_tap2(channel):
#	f.calibration = float(config.get('taps', 'calibration_1'))
#	f.update()

#Add the event detection to trigger callback.
GPIO.add_event_detect(flow_pin_tap1, GPIO.RISING, callback=to_pi_tap1)
#GPIO.add_event_detect(flow_pin_tap2, GPIO.RISING, callback=to_pi_tap2)

try:
 	while True:
		time.sleep(1)
		f.last_pour_func()

except KeyboardInterrupt:
	print "Goodbye"
 	GPIO.cleanup()
	sys.exit()