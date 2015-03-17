import time
from random import randint
from flowmeter import *

rand_flow = randint(142, 242)
f = FlowMeter()
clicks = 0

while True:
	if (clicks < rand_flow):
		clicks = clicks + 1
		time.sleep(.02)
		f.update()
	else:
		print "stopped"
		time.sleep(10)
		print f.last_pour_func()
		print f.last_pour_in_oz()
		print f.last_pour_in_ml()
		break