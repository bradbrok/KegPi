"""
KegPi

The tastiest solution to monitor your keggerator.
"""

import time


class FlowMeter(object):
    version = 'v0.1'
    enabled = True
    click_count = 0
    last_click_time = 0
    this_pour = 0
    last_pour = 0
    last_pour_time = 0
    total_pour = 0
    time_now = 0
    ml_per_click = 2.5 #This is an assumption, need to have easy way to calibrate.
    oz_per_click = 0.08454
    ml_in_a_pint = 473.176
    ml_in_an_oz = 29.5735
    to_ml = 0

    #Initialize all the things.jpg!!!
    def __init__(self):
        self.click_count = 0
        self.last_click_time = 0
        self.this_pour = 0
        self.last_pour = 0
        self.last_pour_time = 0
        self.total_pour = 0
        self.enabled = True
        self.ml_per_click = 2.5
        self.oz_per_click = 0.08454
        self.ml_in_a_pint = 473.176
        self.ml_in_an_oz = 29.5735
        self.to_ml = 0

    #GPIO detects the rising edge, and updates the current count.
    #Find the time of the last click.
    def update(self):
        self.click_count = self.click_count + 1
        self.last_click_time = time.time()
        print self.click_count, "Last Click"
        print self.last_click_time, "was the time this cick was found."


    #If no clicks are found in the last 20 seconds, record the clicks as a last pour.
    #Reset click count for next pour.
    def last_pour_func(self):
        if (time.time() - self.last_click_time > 5):
            self.last_pour = self.click_count
            self.click_count = 0
            print "Last pour was ", self.last_pour, " clicks."
            print "Click count reset to: ", self.click_count
            return self.last_pour
        else:
            print "Nothing happened."
            time.sleep(1)
            self.last_pour_func()

    #Store the total click count to update keg volume.
    def store_total_clicks(self):
        self.total_pour = self.last_pour + self.total_pour
        return self.total_pour

    #Store the last pour in ml
    def last_pour_in_ml(self):
        self.to_ml = (self.last_pour * self.ml_per_click)
        print self.to_ml, " Ml poured."
        return self.to_ml

    #Store the last pour in OZ
    def last_pour_in_oz(self):
        self.last_pour_oz = (self.last_pour * self.oz_per_click)
        print self.last_pour_oz, "oz poured."
        return self.last_pour_oz

