import sqlite3
import sys
import time

#This delivers all the data from the db to the main app.
class BevDataBase(object):

    #keg = Kegs()
    def __init__(self):
        self.db = sqlite3.connect('beverage_db', check_same_thread=False)
        self.cursor = self.db.cursor()

    def beers_init(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS bevs_tap1(id INTEGER PRIMARY KEY, time_pour TEXT, date_pour TEXT,
            clicks INTEGER, ml_pour NUMERIC, oz_pour NUMERIC, pour_count INTEGER)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS bevs_tap2(id INTEGER PRIMARY KEY, time_pour TEXT, date_pour TEXT,
            clicks INTEGER, ml_pour NUMERIC, oz_pour NUMERIC, pour_count INTEGER)''')
        self.db.commit()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS beers1(id INTEGER PRIMARY KEY, beer_name TEXT, 
            og Numeric, fg Numeric, calibration Numeric, beer_desc TEXT, ibu Numeric, glass_type TEXT, keg_size Numeric)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS beers2(id INTEGER PRIMARY KEY, beer_name TEXT, 
            og Numeric, fg Numeric, calibration Numeric, beer_desc TEXT, ibu Numeric, glass_type TEXT, keg_size Numeric)''')
        self.db.commit()
        self.cursor.execute('''SELECT beer_name from beers1 where id=1''')
        idx = self.cursor.fetchone()
        if idx == None:
            self.cursor.execute('''INSERT INTO beers1(beer_name, og, fg, calibration, beer_desc, ibu, glass_type, keg_size) 
                VALUES (?,?,?,?,?,?,?,?)''', 
                ("Beer", 1, 1, 2.25, "Delicious!", 0, "Pint Glass", 640))
            self.cursor.execute('''INSERT INTO beers2(beer_name, og, fg, calibration, beer_desc, ibu, glass_type, keg_size)
                VALUES (?,?,?,?,?,?,?,?)''', 
                ("Beer", 1, 1, 2.25, "Delicious!", 0, "Pint Glass", 640))
            self.db.commit()
        else:
            pass

    def close(self):
        self.db.close()
    
    #Show details of just the last beer on tap 1 & 2 accordingly.
    def keg_size1(self):
        self.cursor.execute('''SELECT keg_size from beers1 where id=1''')
        keg = self.cursor.fetchone()[0]
        return keg

    def keg_size2(self):
        self.cursor.execute('''SELECT keg_size from beers2 where id=1''')
        keg = self.cursor.fetchone()[0]
        return keg

    def beer_desc1(self):
        self.cursor.execute('''SELECT beer_desc from beers1 where id=1''')
        desc = self.cursor.fetchone()[0]
        if desc != None:
            return desc
        else:
            return "Type a description!"

    def ibu1(self):
        self.cursor.execute('''SELECT ibu from beers1 where id=1''')
        ibu = self.cursor.fetchone()[0]
        if ibu != None:
            return ibu
        else:
            return 0

    def glass1(self):
        self.cursor.execute('''SELECT glass_type from beers1 where id=1''')
        glass = self.cursor.fetchone()[0]
        if glass != None:
            return glass
        else:
            return "Pint Glass"

    def beer_desc2(self):
        self.cursor.execute('''SELECT beer_desc from beers2 where id=1''')
        desc = self.cursor.fetchone()[0]
        if desc != None:
            return desc
        else:
            return "Type a description!"


    def ibu2(self):
        self.cursor.execute('''SELECT ibu from beers2 where id=1''')
        ibu = self.cursor.fetchone()[0]
        if ibu != None:
            return ibu
        else:
            return 0

    def glass2(self):
        self.cursor.execute('''SELECT glass_type from beers2 where id=1''')
        glass = self.cursor.fetchone()[0]
        if glass != None:
            return glass
        else:
            return "Pint Glass"

    def last_beer_tap1_id(self):
        self.cursor.execute('''SELECT max(id) from bevs_tap1''')
        last_id = self.cursor.fetchone()[0]
        if last_id != None:
            return last_id
        else:
            return 0

    def last_beer_tap1_oz(self):
        if self.last_beer_tap1_id() != 0:
            idx = self.last_beer_tap1_id()
            self.cursor.execute('''SELECT oz_pour from bevs_tap1 where id = ?''', (idx,))
            oz1 = self.cursor.fetchone()[0]
            return round(oz1,1)
        else:
            return 0

    def last_beer_tap1_ml(self):
        if self.last_beer_tap1_id() != 0:
            idx = self.last_beer_tap1_id()
            self.cursor.execute('''SELECT ml_pour from bevs_tap1 where id = ?''', (idx,))
            ml1 = self.cursor.fetchone()[0]
            return round(ml1,1)
        else:
            return 0

    def last_beer_tap1_time(self):
        if self.last_beer_tap1_id() != 0:
            idx = self.last_beer_tap1_id()
            self.cursor.execute('''SELECT date_pour from bevs_tap1 where id = ?''', (idx,))
            time1 = self.cursor.fetchone()[0]
            if time1 == time.strftime('%m/%d/%y'):
                time1 = "Today"
            return time1
        else:
            return 0

    def last_beer_tap2_id(self):
        self.cursor.execute('''SELECT max(id) from bevs_tap2''')
        last_id = self.cursor.fetchone()[0]
        if last_id != None:
            return last_id
        else:
            return 0

    def last_beer_tap2_oz(self):
        if self.last_beer_tap2_id() != 0:
            idx = self.last_beer_tap2_id()
            self.cursor.execute('''SELECT oz_pour from bevs_tap2 where id = ?''', (idx,))
            oz2 = self.cursor.fetchone()[0]
            return round(oz2,1)
        else:
            return 0

    def last_beer_tap2_ml(self):
        if self.last_beer_tap2_id() != 0:
            idx = self.last_beer_tap2_id()
            self.cursor.execute('''SELECT ml_pour from bevs_tap2 where id = ?''', (idx,))
            ml2 = self.cursor.fetchone()[0]
            return round(ml2,1)
        else:
            return 0

    def last_beer_tap2_time(self):
        if self.last_beer_tap2_id() != 0:
            idx = self.last_beer_tap2_id()
            self.cursor.execute('''SELECT date_pour from bevs_tap2 where id = ?''', (idx,))
            time2 = self.cursor.fetchone()[0]
            if time2 == time.strftime('%m/%d/%y'):
                time2 = "Today"
            return time2
        else:
            return "No pours recorded"

    #Show basic details of just the last 5 beers. Pass this as dict.
    def second_beer1(self):
        if self.last_beer_tap1_id() > 1:
            idx = self.last_beer_tap1_id()
            idy = idx - 1
            self.cursor.execute('''SELECT ml_pour, oz_pour, date_pour from bevs_tap1 where id = ?''', (idy,))
            li = self.cursor.fetchall()
            lix = li[0]
            ml = lix[0]
            oz = lix[1]
            dt = lix[2]
            #if dt == time.strftime('%m/%d/%y'):
            #    dt = "Today"
            return "%s oz / %d ml - %s" % (round(oz,1), ml, dt)
        else:
            return "None"

    def third_beer1(self):
        if self.last_beer_tap1_id() > 2:
            idx = self.last_beer_tap1_id()
            idy = idx - 2
            self.cursor.execute('''SELECT ml_pour, oz_pour, date_pour from bevs_tap1 where id = ?''', (idy,))
            li = self.cursor.fetchall()
            lix = li[0]
            ml = lix[0]
            oz = lix[1]
            dt = lix[2]
            #if dt == time.strftime('%m/%d/%y'):
            #    dt = "Today"
            return "%s oz / %d ml - %s" % (round(oz,1), ml, dt)
        else:
            return "None"

    def fourth_beer1(self):
        if self.last_beer_tap1_id() > 3:
            idx = self.last_beer_tap1_id()
            idy = idx - 3
            self.cursor.execute('''SELECT ml_pour, oz_pour, date_pour from bevs_tap1 where id = ?''', (idy,))
            li = self.cursor.fetchall()
            lix = li[0]
            ml = lix[0]
            oz = lix[1]
            dt = lix[2]
            #if dt == time.strftime('%m/%d/%y'):
            #    dt = "Today"
            return "%s oz / %d ml - %s" % (round(oz,1), ml, dt)
        else:
            return "None"

    def fifth_beer1(self):
        if self.last_beer_tap1_id() > 4:
            idx = self.last_beer_tap1_id()
            idy = idx - 4
            self.cursor.execute('''SELECT ml_pour, oz_pour, date_pour from bevs_tap1 where id = ?''', (idy,))
            li = self.cursor.fetchall()
            lix = li[0]
            ml = lix[0]
            oz = lix[1]
            dt = lix[2]
            #if dt == time.strftime('%m/%d/%y'):
            #    dt = "Today"
            return "%s oz / %d ml - %s" % (round(oz,1), ml, dt)
        else:
            return "None"

    def second_beer2(self):
        if self.last_beer_tap2_id() > 1:
            idx = self.last_beer_tap2_id()
            idy = idx - 1
            self.cursor.execute('''SELECT ml_pour, oz_pour, date_pour from bevs_tap2 where id = ?''', (idy,))
            li = self.cursor.fetchall()
            lix = li[0]
            ml = lix[0]
            oz = lix[1]
            dt = lix[2]
            if dt == time.strftime('%m/%d/%y'):
                dt = "Today"
            return "%s oz / %d ml - %s" % (round(oz,1), ml, dt)
        else:
            return "None"

    def third_beer2(self):
        if self.last_beer_tap2_id() > 2:
            idx = self.last_beer_tap2_id()
            idy = idx - 2
            self.cursor.execute('''SELECT ml_pour, oz_pour, date_pour from bevs_tap2 where id = ?''', (idy,))
            li = self.cursor.fetchall()
            lix = li[0]
            ml = lix[0]
            oz = lix[1]
            dt = lix[2]
            #if dt == time.strftime('%m/%d/%y'):
            #    dt = "Today"
            return "%s oz / %d ml - %s" % (round(oz,1), ml, dt)
        else:
            return "None"

    def fourth_beer2(self):
        if self.last_beer_tap2_id() > 3:
            idx = self.last_beer_tap2_id()
            idy = idx - 3
            self.cursor.execute('''SELECT ml_pour, oz_pour, date_pour from bevs_tap2 where id = ?''', (idy,))
            li = self.cursor.fetchall()
            lix = li[0]
            ml = lix[0]
            oz = lix[1]
            dt = lix[2]
            if dt == time.strftime('%m/%d/%y'):
                dt = "Today"
            return "%s oz / %d ml - %s" % (round(oz,1), ml, dt)
        else:
            return "None"

    def fifth_beer2(self):
        if self.last_beer_tap2_id() > 4:
            idx = self.last_beer_tap2_id()
            idy = idx - 4
            self.cursor.execute('''SELECT ml_pour, oz_pour, date_pour from bevs_tap2 where id = ?''', (idy,))
            li = self.cursor.fetchall()
            lix = li[0]
            ml = lix[0]
            oz = lix[1]
            dt = lix[2]
            #if dt == time.strftime('%m/%d/%y'):
            #    dt = "Today"
            return "%s oz / %d ml - %s" % (round(oz,1), ml, dt)
        else:
            return "None"

    #Keg volumes initialzied from Kegs class.
    #Add all volumes in ml together and find the percentage left.
    def keg_volume1_pints(self):
        starting_vol = self.keg_size1() #5 gallons in oz, we should init from Keg class, but not now.
        self.cursor.execute('''SELECT sum(oz_pour) from bevs_tap1''')
        vol1 = self.cursor.fetchone()[0]
        if vol1 != None:
            remaining_vol1 = starting_vol - vol1
            return round((remaining_vol1),1)
        else:
            return self.keg_size1()

    def keg_volume2_pints(self):
        starting_vol = self.keg_size2() #5 gallons in oz
        self.cursor.execute('''SELECT sum(oz_pour) from bevs_tap2''')
        vol2 = self.cursor.fetchone()[0]
        if vol2 != None:
            remaining_vol2 = starting_vol - vol2
            return round((remaining_vol2),1)
        else:
            return self.keg_size2()

    def beer_name1(self):
        self.cursor.execute('''SELECT beer_name from beers1 where id=1''')
        beer = self.cursor.fetchone()[0]
        return beer

    def og1(self):
        self.cursor.execute('''SELECT og from beers1 where id=1''')
        og = self.cursor.fetchone()[0]
        return og

    def fg1(self):
        self.cursor.execute('''SELECT fg from beers1 where id=1''')
        fg = self.cursor.fetchone()[0]
        return fg

    def calibration1(self):
        self.cursor.execute('''SELECT calibration from beers1 where id=1''')
        cal = self.cursor.fetchone()[0]
        return cal

    def beer_name2(self):
        self.cursor.execute('''SELECT beer_name from beers2 where id=1''')
        beer = self.cursor.fetchone()[0]
        return beer

    def og2(self):
        self.cursor.execute('''SELECT og from beers2 where id=1''')
        og = self.cursor.fetchone()[0]
        return og

    def fg2(self):
        self.cursor.execute('''SELECT fg from beers2 where id=1''')
        fg = self.cursor.fetchone()[0]
        return fg

    def calibration2(self):
        self.cursor.execute('''SELECT calibration from beers2 where id=1''')
        cal = self.cursor.fetchone()[0]
        return cal
