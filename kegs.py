"""
KegPi

The tastiest solution to monitor your keggerator.

The Keg class will help us update our keg volumes and tap numbers associated with
each and every keg.
"""
import time
import math
from flowmeter import *

class Kegs(FlowMeter):

	f = FlowMeter()

	corny_keg = 18927 # in Ml
	custom_keg_size = 0 # in Ml
	ml_left_in_keg = 0
	last_drink_count = f.drink_count()
	keg_selection = []
	keg_volume_left = 0
	tap_number = 0


	def __init__(self):
		self.corny_keg = 18927
		self.custom_keg_size = 0
		self.ml_left_in_keg = 0
		self.last_drink_count = f.drink_count()
		self.keg_selection = 0
		self.keg_volume_left = 0
		self.tap_number = 0

	#Method to determine the volume left in the keg based on volumer poured.
	def keg_volume(self):
		if (self.keg_volume_left == 0):
			print "It appears the keg is empty, did you put in a new full keg?"
			print "Yes = y ... No = n"
			user_input = raw_input('> ')
			if (user_input == 'y' or 'Y'):
				self.keg_volume_left = self.corny_keg
			else:
				print "Please brew some more beer!"
		else:
			self.keg_volume_left = self.keg_selection - f.last_pour
			print self.keg_volume_left, "ml left in the keg"
			print (self.keg_volume_left / 29.5735), "oz left in keg"
			print ((self.keg_volume_left / 29.5735) / 16.0), "pints left in the keg."
			return self.keg_volume_left

	#Determine which keg to subtract volume from.
	def keg_tap_number (self):
		pass