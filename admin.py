"""
KegPi

The tastiest solution to monitor your keggerator.

The Keg class will help us update our keg volumes and tap numbers associated with
each and every keg.
"""
from flowmeter import *
from bevdb import *
import sqlite3
import time

bevdb = BevDataBase()

f = FlowMeter()

class AdminActions(object):

    def __init__(self):
        self.db = sqlite3.connect('beverage_db', check_same_thread=False)
        self.cursor = self.db.cursor()

        #Constants
        self.corny_keg_start_ml = 18927.05 #ml
        self.corny_keg_start_oz = 640.0 #oz

        #Store these to be called
        self.og1 = 0
        self.fg1 = 0
        self.beer_name1 = ''
        self.ml_cal1 = 2.25

        self.og2 = 0
        self.fg2 = 0
        self.beer_name2 = ''
        self.ml_cal2 = 2.25


    def close(self):
        self.db.close()

    def calibrations_tap1(self):
        cal = (float(self.ml_cal1) / f.last_pour)
        self.cursor.execute('''REPLACE INTO beers1 (calibration) Values (?)'''[cal])
        self.db.commit()
        return "Success! Calibration is", cal, "ml per click!"

    def calibrations_tap2(self):
        cal = (float(self.ml_cal2) / f.last_pour)
        self.cursor.execute('''REPLACE INTO beers2 (calibration) Values (?)'''[cal])
        self.db.commit()
        return "Success! Calibration is", cal, "ml per click!"

    def beer_name1_post(self):
        self.cursor.execute('''UPDATE beers1 set beer_name=? where id=1''',[self.beer_name1])
        self.db.commit()
        return "Success"

    def beer_name2_post(self):
        self.cursor.execute('''UPDATE beers2 set beer_name=? where id=1''',[self.beer_name2])
        self.db.commit()
        return "Success"

    def og1_post(self):
        self.cursor.execute('''UPDATE beers1 set og=? where id=1''',[self.og1])
        self.db.commit()
        print "Success"

    def fg1_post(self):
        self.cursor.execute('''UPDATE beers1 set fg=? where id=1''',[self.fg1])
        self.db.commit()
        return "Success"

    def og2_post(self):
        self.cursor.execute('''UPDATE beers2 set og=? where id=1''',[self.og2])
        self.db.commit()
        return "Success"

    def fg2_post(self):
        self.cursor.execute('''UPDATE beers2 set fg=? where id=1''',[self.fg2])
        self.db.commit()
        return "Success"

    #Drop the tables for the keg, store totals only in db. Then reinitialize kegs.
    def kick_keg1(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS kegs1(id INTEGER PRIMARY KEY, beer_name TEXT, date_kicked TEXT)''')
        self.cursor.execute('''INSERT INTO kegs1(beer_name, date_kicked) VALUES (?,?)''', (bevdb.beer_name1, time.ctime()))
        self.cursor.execute('''DROP TABLE beers1''')
        self.cursor.execute('''INSERT INTO beers1(beer_name, og, fg, calibration) VALUES (?,?,?,?)''', ("Beer", 0, 0, 2.25))
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS bevs_tap1(id INTEGER PRIMARY KEY, time_pour TEXT, date_pour TEXT,
            clicks INTEGER, ml_pour NUMERIC, oz_pour NUMERIC, pour_count INTEGER)''')
        self.db.commit()
        return "Success!"

    def kick_keg2(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS kegs2(id INTEGER PRIMARY KEY, beer_name TEXT, date_kicked TEXT)''')
        self.cursor.execute('''INSERT INTO kegs2(beer_name, date_kicked) VALUES (?,?)''', (bevdb.beer_name1, time.ctime()))
        self.cursor.execute('''DROP TABLE beers2''')
        self.cursor.execute('''INSERT INTO beers2(beer_name, og, fg, calibration) VALUES (?,?,?,?)''', ("Beer", 0, 0, 2.25))
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS bevs_tap1(id INTEGER PRIMARY KEY, time_pour TEXT, date_pour TEXT,
            clicks INTEGER, ml_pour NUMERIC, oz_pour NUMERIC, pour_count INTEGER)''')
        self.db.commit()
        return "Success!"
