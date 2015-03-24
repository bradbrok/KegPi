import sqlite3
import sys
from kegs import *

#This class will interface with the Flask app.
class BevDataBase():

    keg = Kegs()
    db = sqlite3.connect('beverage_db')
    cursor = db.cursor()
    
    #Show details of just the last beer on tap 1 & 2 accordingly.
    def last_beer_tap1():
        last_id = cursor.execute('''SELECT max(id) from bevs_tap1''')

        return last_id

    def last_beer_tap2():
        pass

    #Show basic details of just the last 5 beers.
    def last_five_tap1():
        pass

    def last_five_tap2():
        pass

    #Keg volumes initialzied from Kegs class.
    #Add all volumes in ml together and find the percentage left.
    def keg_volume1():
        pass

    def keg_volume2():
        pass
    
    #Drop the tables for the keg, store totals only in db.
    def kick_keg1():
        pass

    def kick_keg2():
        pass