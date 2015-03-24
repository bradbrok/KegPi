#!/usr/bin/python

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from bevdb import *
from flowmeter import *
import sqlite3

app = Flask(__name__)
app.debug = True

db = BevDataBase()
bevdb = sqlite3.connect('beverage_db',check_same_thread=False)

def close_db():
    bevdb.close()

# Main
@app.route('/', methods=['GET', 'POST'])
def index():
    last1 = db.last_beer_tap1_id()
    last_oz = db.last_beer_tap1_oz()
    time1 = db.last_beer_tap1_time()
    ml_left = db.keg_volume1()
    close_db()
    return render_template('index.html',
        last1 = last1,
        last_oz = last_oz,
        time1 = time1,
        ml_left = ml_left)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    return render_template('admin.html')

@app.route('/calibrate', methods=['POST'])
def calibrate_page():
    return "Place holder for calibration."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)