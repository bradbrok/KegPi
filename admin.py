"""
KegPi

The tastiest solution to monitor your keggerator.

The admin class is the destructive database model. 
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
        self.sixth_oz = 661
        self.quarter_oz = 992
        self.half_bbl = 1984

        #Store these to be called
        self.og1 = 0
        self.fg1 = 0
        self.beer_name1 = ''
        self.ml_cal1 = 2.25
        self.bdesc1 = ''
        self.ibu2 = 0

        self.og2 = 0
        self.fg2 = 0
        self.beer_name2 = ''
        self.ml_cal2 = 2.25
        self.bdesc2 = ''
        self.ibu2 = 0


    def close(self):
        self.db.close()

    def desc1(self):
        desc = self.bdesc1
        self.cursor.execute('''UPDATE beers1 set beer_desc=? where id=1''',[desc])
        self.db.commit()
        return "Success!"

    def desc2(self):
        desc = self.bdesc2
        self.cursor.execute('''UPDATE beers2 set beer_desc=? where id=1''',[desc])
        self.db.commit()
        return "Success!"

    def ibu_1(self):
        ibu = int(self.ibu1)
        self.cursor.execute('''UPDATE beers1 set ibu=? where id=1''',[ibu])
        self.db.commit()
        return "Success!"

    def ibu_2(self):
        ibu = int(self.ibu2)
        self.cursor.execute('''UPDATE beers2 set ibu=? where id=1''',[ibu])
        self.db.commit()
        return "Success!"

    def calibrations_tap1(self):
        cal = (float(self.ml_cal1)/ bevdb.last_clicks1())
        print cal
        self.cursor.execute('''UPDATE beers1 set calibration=? where id=1''',[cal])
        self.db.commit()
        print "Success! Calibration is", cal, "ml per click!"

    def calibrations_tap2(self):
        cal = (float(self.ml_cal2) / bevdb.last_clicks2())
        print cal
        self.cursor.execute('''UPDATE beers2 set calibration=? where id=1''',[cal])
        self.db.commit()
        print "Success! Calibration is", cal, "ml per click!"

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
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS kegs(id INTEGER PRIMARY KEY, beer_name TEXT, date_kicked TEXT)''')
        self.cursor.execute('''INSERT INTO kegs(beer_name, date_kicked) VALUES (?,?)''', (bevdb.beer_name1(), time.strftime("%x")))
        self.cursor.execute('''DROP TABLE bevs_tap1''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS bevs_tap1(id INTEGER PRIMARY KEY, time_pour TEXT, date_pour TEXT,
            clicks INTEGER, ml_pour NUMERIC, oz_pour NUMERIC)''')
        self.cursor.execute('''UPDATE beers1 SET beer_name=?, og=?, fg=?, beer_desc=?, ibu=?, glass_type=?, keg_size=?, keg_start_volume=? 
                where id=1''',("Beer", 1, 1, "Delicious!", 0, "Pint Glass", 640, 0))
        self.db.commit()
        return "Success!"

    def kick_keg2(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS kegs(id INTEGER PRIMARY KEY, beer_name TEXT, date_kicked TEXT)''')
        self.cursor.execute('''INSERT INTO kegs(beer_name, date_kicked) VALUES (?,?)''', (bevdb.beer_name2(), time.strftime("%x")))
        self.cursor.execute('''DROP TABLE bevs_tap2''')
        self.db.commit()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS bevs_tap2(id INTEGER PRIMARY KEY, time_pour TEXT, date_pour TEXT,
            clicks INTEGER, ml_pour NUMERIC, oz_pour NUMERIC)''')
        self.db.commit()
        self.cursor.execute('''UPDATE beers2 SET beer_name=?, og=?, fg=?, beer_desc=?, ibu=?, glass_type=?, keg_size=?, keg_start_volume=? 
                where id=1''',("Beer", 1, 1, "Delicious!", 0, "Pint Glass", 640, 0))
        self.db.commit()
        return "Success!"
