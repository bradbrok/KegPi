#!/usr/bin/python

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Response
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from bevdb import *
from admin import * #This is going to post our calibration, fg, og, and beer names too!
import sqlite3
import ConfigParser
from functools import wraps
#Configs
app = Flask(__name__)
app.debug = True
app.secret_key = 'beer'
WTF_CSRF_ENABLED = False
#Class calls
#admin = AdminActions()
db = BevDataBase()
#Misc functions
def check_auth(username, password):
    #lol, need to hash these in the db.
    return username == 'beer' and password == 'beer'

def authenticate():
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

def gravity_calc(og, fg):
    abv = ((og - fg) / 0.736 * 100)
    return round(abv, 1)

def calorie_calc(og, fg, ml):
    #These are a bit complicated, basically convert og and fg to plato or sg, then find the abw
    #basically calculates by weight of carbs and alcohol. Carbs = 4cal/gram, alcohol = 7cal/gram
    pog = (-1 * 616.868) + (1111.14 * og) - (630.272 * (og ** 2)) + (135.997 * (og ** 3)) 
    pfg = (-1 * 616.868) + (1111.14 * fg) - (630.272 * (fg ** 2)) + (135.997 * (fg ** 3))
    abv = ((og - fg) / 0.75 * 100)
    abw = ((0.79 * abv) / fg)
    rex = (0.1808 * pog) + (0.8192 * pfg)
    calories = ((6.9 * abv) + 4 * (rex - 0.1)) * fg * (ml /100)
    return round(calories, 1)

# Main page and dashboard.
@app.route('/', methods=['GET', 'POST'])
def dashboard():
    db.beers_init()
    #Tap 1
    beer_name1 = db.beer_name1()
    last1 = db.last_beer_tap1_id()
    last_oz1 = db.last_beer_tap1_oz()
    last_ml1 = db.last_beer_tap1_ml()
    time1 = db.last_beer_tap1_time()
    pints1_left = db.keg_volume1_pints()
    second1 = db.second_beer1()
    third1 = db.third_beer1()
    fourth1 = db.fourth_beer1()
    fifth1 = db.fifth_beer1()
    og1 = db.og1()
    fg1 = db.fg1()
    abv1 = gravity_calc(og1, fg1)
    calories1 = calorie_calc(og1, fg1, last_ml1)
    #Tap2
    beer_name2 = db.beer_name2()
    last2 = db.last_beer_tap2_id()
    last_oz2 = db.last_beer_tap2_oz()
    last_ml2 = db.last_beer_tap2_ml()
    time2 = db.last_beer_tap2_time()
    pints2_left = db.keg_volume2_pints()
    second2 = db.second_beer2()
    third2 = db.third_beer2()
    fourth2 = db.fourth_beer2()
    fifth2 = db.fifth_beer2()
    og2 = db.og2()
    fg2 = db.fg2()
    abv2 = gravity_calc(og2, fg2)
    calories2 = calorie_calc(og2, fg2, last_ml2)
    return render_template('index.html',
        #Tap1
        beer_name1 = beer_name1,
        last1 = last1,
        last_oz1 = last_oz1,
        last_ml1 = last_ml1,
        time1 = time1,
        pints1_left = pints1_left,
        og1 = og1,
        fg1 = fg1,
        abv1 = abv1,
        calories1 = calories1,
        second1 = second1,
        third1 = third1,
        fourth1 = fourth1,
        fifth1 = fifth1,
        #Tap2
        beer_name2 = beer_name2,
        last2 = last2,
        last_oz2 = last_oz2,
        last_ml2 = last_ml2,
        time2 = time2,
        pints2_left = pints2_left,
        calories2 = calories2,
        second2 = second2,
        third2 = third2,
        fourth2 = fourth2,
        fifth2 = fifth2,
        og2 = og2,
        fg2 = fg2,
        abv2 = abv2)
#Forms
class TapAdmin1(Form):
    beer_name1 = StringField('Beer Name')
    og1 = StringField('Original Gravity')
    fg1 = StringField('Final Gravity')
    submit1 = SubmitField('Submit')

class TapAdmin2(Form):
    beer_name2 = StringField('Beer Name')
    og2 = StringField('Original Gravity')
    fg2 = StringField('Final Gravity')
    submit2 = SubmitField('Submit')

@app.route('/admin', methods=['GET', 'POST'])
@requires_auth
def admin():
    admin = AdminActions()
    form1 = TapAdmin1()
    if form1.validate_on_submit():
        admin.beer_name1 = form1.beer_name1.data
        admin.og1 = form1.og1.data
        admin.fg1 = form1.fg1.data
        if admin.og1 != '' and admin.og1 > 1:
            admin.og1_post()
        if admin.fg1 != '' and admin.fg1 > 1:
            admin.fg1_post()
        if admin.beer_name1 != '':
            admin.beer_name1_post()
    form2 = TapAdmin2()
    if form2.validate_on_submit():
        admin.beer_name2 = form2.beer_name2.data
        admin.og2 = form2.og2.data
        admin.fg2 = form2.fg2.data
        if admin.og2 != '' and admin.og2 > 1:
            admin.og2_post()
        if admin.fg2 != '' and admin.fg2 > 1:
            admin.fg2_post()
        if admin.beer_name2 != '':
            admin.beer_name2_post()
    return render_template('/admin.html',form1=form1, form2=form2)

@app.route('/update', methods=['POST'])
def admin_update():
    return redirect('/admin')
    

@app.route('/calibrate', methods=['GET', 'POST'])
def calibrate_page():
    return "Place holder for calibration."

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
