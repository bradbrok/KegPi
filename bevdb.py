import sqlite3
import sys
#from kegs import *

#This class will interface with the Flask app.
class BevDataBase():

    #keg = Kegs()
    def __init__(self):
        self.db = sqlite3.connect('beverage_db', check_same_thread=False)
        self.cursor = self.db.cursor()

    def close(self):
        self.db.close()
    
    #Show details of just the last beer on tap 1 & 2 accordingly.
    def last_beer_tap1_id(self):
        self.cursor.execute('''SELECT max(id) from bevs_tap1''')
        last_id = self.cursor.fetchone()[0]
        if last_id != None:
            return last_id
        else:
            return "Something is wrong. No pours found."
        self.close()

    def last_beer_tap1_oz(self):
        idx = self.last_beer_tap1_id()
        self.cursor.execute('''SELECT oz_pour from bevs_tap1 where id = ?''', (idx,))
        oz1 = self.cursor.fetchone()[0]
        if oz1 != None:
            return oz1
        else:
            return "0"
        self.close()

    def last_beer_tap1_time(self):
        idx = self.last_beer_tap1_id()
        self.cursor.execute('''SELECT date_pour from bevs_tap1 where id = ?''', (idx,))
        time1 = self.cursor.fetchone()[0]
        if time1 != None:
            return time1
        else:
            return "0"
        self.close()

    def last_beer_tap2_id(self):
        self.cursor.execute('''SELECT max(id) from bevs_tap2''')
        last_id = self.cursor.fetchone()[0]
        if last_id != None:
            return last_id
        else:
            return "0"
        self.close()

    def last_beer_tap2_oz(self):
        if self.last_beer_tap2_id() != "0":
            idx = self.last_beer_tap1_id()
            self.cursor.execute('''SELECT oz_pour from bevs_tap2 where id = ?''', (idx,))
            oz2 = self.cursor.fetchone()[0]
            return oz2
        else:
            return "0"
        self.close()

    def last_beer_tap2_time(self):
        if self.last_beer_tap2_id() != "0":
            idx = self.last_beer_tap1_id()
            self.cursor.execute('''SELECT date_pour from bevs_tap2 where id = ?''', (idx,))
            time2 = self.cursor.fetchone()[0]
            return time2
        else:
            return "No pours recorded"
        self.close()

    #Show basic details of just the last 5 beers. Pass this as dict.
    def last_five_tap1(self):
        pass

    def last_five_tap2(self):
        pass

    #Keg volumes initialzied from Kegs class.
    #Add all volumes in ml together and find the percentage left.
    def keg_volume1_pints(self):
        starting_vol = 640.0 #5 gallons in oz, we should init from Keg class, but not now.
        self.cursor.execute('''SELECT sum(oz_pour) from bevs_tap1''')
        vol1 = self.cursor.fetchone()[0]
        if vol1 != None:
            remaining_vol1 = starting_vol - vol1
            return int(remaining_vol1 / 16)
        else:
            return "No"
        self.close()

    def keg_volume2_pints(self):
        starting_vol = 640.0 #5 gallons in oz
        self.cursor.execute('''SELECT sum(oz_pour) from bevs_tap2''')
        vol2 = self.cursor.fetchone()[0]
        if vol2 != None:
            remaining_vol1 = starting_vol - vol2
            return int(remaining_vol2 / 16)
        else:
            return "No"
        self.close()

    #Drop the tables for the keg, store totals only in db.
    def kick_keg1(self, beer_name1):
        pass

    def kick_keg2(self, beer_name2):
        pass