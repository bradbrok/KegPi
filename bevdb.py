import sqlite3
import sys
#from kegs import *

#This class will interface with the Flask app.
class BevDataBase():

    #keg = Kegs()
    def __init__(self):
        self.db = sqlite3.connect('beverage_db', check_same_thread=False)
        self.cursor = self.db.cursor()
    
    #Show details of just the last beer on tap 1 & 2 accordingly.
    def last_beer_tap1_id(self):
        self.cursor.execute('''SELECT max(id) from bevs_tap1''')
        last_id = self.cursor.fetchone()
        last_id = tuple(last_id)[0]
        return last_id

    def last_beer_tap1_oz(self):
        idx = self.last_beer_tap1_id()
        self.cursor.execute('''SELECT oz_pour from bevs_tap1 where id = ?''', (idx,))
        oz1 = self.cursor.fetchone()
        oz1 = tuple(oz1)[0]
        return oz1

    def last_beer_tap1_time(self):
        idx = self.last_beer_tap1_id()
        self.cursor.execute('''SELECT time_pour from bevs_tap1 where id = ?''', (idx,))
        time1 = self.cursor.fetchone()
        time1 = tuple(time1)[0]
        return time1

    def last_beer_tap2(self):
        self.cursor.execute('''SELECT max(id) from bevs_tap2''')
        last_id = self.cursor.fetchone()
        last_id = tuple(last_id)[0]
        return last_id

    def last_beer_tap2_oz(self):
        idx = self.last_beer_tap1_id()
        self.cursor.execute('''SELECT oz_pour from bevs_tap2 where id = ?''', (idx,))
        oz2 = self.cursor.fetchone()
        oz2 = tuple(oz2)[0]
        return oz2

    def last_beer_tap2_time(self):
        idx = self.last_beer_tap1_id()
        self.cursor.execute('''SELECT time_pour from bevs_tap2 where id = ?''', (idx,))
        time2 = self.cursor.fetchone()
        time2 = tuple(time2)[0]
        return time2

    #Show basic details of just the last 5 beers.
    def last_five_tap1(self):
        pass

    def last_five_tap2(self):
        pass

    #Keg volumes initialzied from Kegs class.
    #Add all volumes in ml together and find the percentage left.
    def keg_volume1(self):
        starting_vol = 640.0 #5 gallons in oz
        self.cursor.execute('''SELECT sum(oz_pour) from bevs_tap1''')
        vol1 = self.cursor.fetchone()
        vol1 = tuple(vol1)[0]
        remaining_vol1 = starting_vol - vol1
        return int(remaining_vol1 / 16)

    def keg_volume2(self):
        starting_vol = 640.0 #5 gallons in oz
        self.cursor.execute('''SELECT sum(oz_pour) from bevs_tap2''')
        vol1 = self.cursor.fetchone()
        vol1 = tuple(vol1)[0]
        remaining_vol1 = starting_vol - vol1
        return int(remaining_vol1 / 16)

    #Drop the tables for the keg, store totals only in db.
    def kick_keg1(self):
        pass

    def kick_keg2(self):
        pass

    def close(self):
        self.db.close()