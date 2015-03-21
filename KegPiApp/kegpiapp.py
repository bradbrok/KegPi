#!/usr/bin/python

from flask import Flask
import sqlite3

app = Flask(__name__)
app.debug = True


def last_row_id():
    db = sqlite3.connect('beverage_db')
    cursor = db.cursor()
    cursor.execute('''SELECT id, time_pour, date_pour, clicks, ml_pour, oz_pour FROM bevs_tap1''')
    all_rows = cursor.fetchall()
    for row in all_rows:
        return('{0}: {1}, {2}, {3}, {4}'.format(row[0], row[1], row[2], row[3], row[4]))
   	db.close()

# Main
@app.route('/')
def hello():
    return last_row_id()

if __name__ == '__main__':
	app.run()