"""
KegPi

The tastiest solution to monitor your keggerator.

The Keg class will help us update our keg volumes and tap numbers associated with
each and every keg.
"""
from flowmeter import *
import sqlite3
import time

f = FlowMeter()

class Admin():

    def __init__(self):
        self.db = sqlite3.connect('beverage_db', check_same_thread=False)
        self.cursor = self.db.cursor()

        #Constants
        self.corny_keg_start_ml = 18927.05 #ml
        self.corny_keg_start_oz = 640.0 #oz

    def close(self):
        self.db.close()

    def calibrations_tap1(self, ml_cal):
        cal = f.calibrate(ml_cal)
        self.cursor.execute('''REPLACE INTO beers1 (calibration) Values (?)'''(cal))

    def calibrations_tap2(self):
        pass

    def beer_name1_pos(self, name):
        pass

    def og1_post(self, og):
        pass

    def fg1_post(self, og):
        pass

    def beer_name2_post(self, name):
        pass

    def og2_post(self, og):
        pass

    def fg2_post(self, og):
        pass
