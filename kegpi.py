'''KegPi - Bradley Brockman
	Simple and elegant Raspberry Pi Keg Monitoring system.
'''

from flowmeter import *
from kegs import *
import os
import time
import RPi.GPIO as GPIO
import sqlite3 as lite

beers_drank_while_coding_this = "6"

flow_pin_tap1 = 23
#flow_pin_tap2 = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(flow_pin_tap1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(flow_pin_tap2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(flow_pin, GPIO.RISING, callback=to_pi)

def to_pi(channel):
	FlowMeter.update()

tap_1_last_pour = FlowMeter.last_pour_in_oz()
#tap2_last = update.FlowMeter(to_pi)
#tap_2_last_pour = FlowMeter.last_pour_in_oz()


print(tap1_last, " ml poured from Tap 1")
#print(tap2_last, " ml poured from Tap 2")



try:
 	while True:
		time.sleep(1)

except KeyboardInterrupt:
	print "Goodbye"
 	GPIO.cleanup()
	sys.exit()