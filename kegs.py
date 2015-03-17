"""
KegPi

The tastiest solution to monitor your keggerator.
"""
import time
import math
from flowmeter import *

class Kegs(FlowMeter):

	corny_keg = 18927 # in Ml
	custom_keg_size = 0 # in Ml
	ml_left_in_keg = 0


	def __init__(self):
		self.corny_keg = 5
		self.custom_keg_size = 0
		self.ml_left_in_keg = 18927