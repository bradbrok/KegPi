#!/usr/bin/python

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from bevdb import *

app = Flask(__name__)
app.debug = True

db = BevDataBase()

# Main
@app.route('/')
def hello():
    return "Hello beer."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)