#!/usr/bin/python

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from bevdb import *
from flowmeter import *
from admin import * #This is going to grab our calibration fg og and beer names too!
import sqlite3
import ConfigParser

app = Flask(__name__)
app.config.from_object('config')
app.debug = True

admin = AdminActions()

db = BevDataBase()
bevdb = sqlite3.connect('beverage_db',check_same_thread=False)
#Keg Conifguration tables
cursor = bevdb.cursor()

def beers_init():
    cursor.execute('''CREATE TABLE IF NOT EXISTS beers1(id INTEGER PRIMARY KEY, beer_name TEXT, 
        og Numeric, fg Numeric, calibration Numeric)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS beers2(id INTEGER PRIMARY KEY, beer_name TEXT, 
        og Numeric, fg Numeric, calibration Numeric)''')
    cursor.execute('''SELECT beer_name from beers1 where id=1''')
    idx = cursor.fetchone()
    if idx == None:
        cursor.execute('''INSERT INTO beers1(beer_name, og, fg, calibration) VALUES (?,?,?,?)''', 
            ("Beer", 0, 0, 2.25))
        cursor.execute('''INSERT INTO beers2(beer_name, og, fg, calibration) VALUES (?,?,?,?)''', 
            ("Beer", 0, 0, 2.25))
    else:
        print "DataBase has been initialized already."

def close_db():
    bevdb.close()

def gravity_calc(og, fg):
    abv = ((og - fg) / 0.75 * 100)
    return round(abv, 1)

def calorie_calc(og, fg, ml):
    abv = ((og - fg) / 0.75 * 100)
    abw = ((0.79 * abv) / fg)
    return abw

# Main page and dashboard.
@app.route('/', methods=['GET', 'POST'])
def dashboard():
    beers_init()
    #Tap 1
    beer_name1 = db.beer_name1()
    last1 = db.last_beer_tap1_id()
    last_oz1 = db.last_beer_tap1_oz()
    time1 = db.last_beer_tap1_time()
    pints1_left = db.keg_volume1_pints()
    og1 = db.og1()
    fg1 = db.fg1()
    abv1 = gravity_calc(og1, fg1)
    #Tap2
    beer_name2 = db.beer_name2()
    last2 = db.last_beer_tap2_id()
    last_oz2 = db.last_beer_tap2_oz()
    time2 = db.last_beer_tap2_time()
    pints2_left = db.keg_volume2_pints()
    og2 = db.og2()
    fg2 = db.fg2()
    abv2 = gravity_calc(og2, fg2)
    return render_template('index.html',
        #Tap1
        beer_name1 = beer_name1,
        last1 = last1,
        last_oz1 = last_oz1,
        time1 = time1,
        pints1_left = pints1_left,
        og1 = og1,
        fg1 = fg1,
        abv1 = abv1,
        #Tap2
        beer_name2 = beer_name2,
        last2 = last2,
        last_oz2 = last_oz2,
        time2 = time2,
        pints2_left = pints2_left,
        og2 = og2,
        fg2 = fg2,
        abv2 = abv2,
        )

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    return render_template('admin.html')

@app.route('/calibrate', methods=['GET', 'POST'])
def calibrate_page():
    return "Place holder for calibration."

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
