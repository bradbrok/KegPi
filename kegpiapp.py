#!/usr/bin/python

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from bevdb import *
from flowmeter import *
import sqlite3
import ConfigParser

app = Flask(__name__)
app.debug = True

db = BevDataBase()
bevdb = sqlite3.connect('beverage_db',check_same_thread=False)

def close_db():
    bevdb.close()

def gravity_calc(og, fg):
    abv = ((og - fg) / 0.75 * 100)
    return abv

def calorie_calc(og, fg):
    abv = ((og - fg) / 0.75 * 100)
    abw = ((0.79 * abv) / fg)
    return abw

# Main page and dashboard.
@app.route('/', methods=['GET', 'POST'])
def dashboard():
    #Tap 1
    last1 = db.last_beer_tap1_id()
    last_oz1 = db.last_beer_tap1_oz()
    time1 = db.last_beer_tap1_time()
    pints1_left = db.keg_volume1_pints()
    #Tap2
    last2 = db.last_beer_tap2_id()
    last_oz2 = db.last_beer_tap2_oz()
    time2 = db.last_beer_tap2_time()
    pints2_left = db.keg_volume2_pints()
    close_db()



    return render_template('index.html',
        #Tap1
        last1 = last1,
        last_oz1 = last_oz1,
        time1 = time1,
        pints1_left = pints1_left,
        #Tap2
        last2 = last2,
        last_oz2 = last_oz2,
        time2 = time2,
        pints2_left = pints2_left
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
