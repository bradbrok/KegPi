import time
from random import randint
from flowmeter import *

import ConfigParser

f = FlowMeter()


rand_flow = randint(142, 200)
f = FlowMeter()
clicks = 0

while True:
	if (clicks < rand_flow):
		clicks = clicks + 1
		time.sleep(.34)
		f.update()
	else:
		print "stopped"
		time.sleep(15)
		f.last_pour_func()
		break