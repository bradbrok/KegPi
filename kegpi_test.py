import time
from random import randint
from flowmeter import *

import ConfigParser

f = FlowMeter()

config = ConfigParser.ConfigParser()
config.read("tap_config.ini")

rand_flow = randint(142, 200)
f = FlowMeter()
clicks = 0

while True:
	if (clicks < rand_flow):
		clicks = clicks + 1
		time.sleep(.01)
		f.update()
	else:
		f.calibration = float(config.get('taps', 'calibration_0'))
		print f.calibration
		print "stopped"
		time.sleep(10)
		f.last_pour_func()
		break