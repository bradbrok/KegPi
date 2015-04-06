"""
KegPi

The tastiest solution to monitor your keggerator.

The FlowMeter clas helps us interface with the meter on the GPIO.
"""

import time
import ConfigParser

class FlowMeter(object):
 
    version = 'v0.1'

    #Initialize all_the_things.jpg!!!
    def __init__(self):
        self.click_count = 0
        self.click_control = 0
        self.last_click_time = 0
        self.this_pour = 0
        self.last_pour = 0
        self.last_pour_time = 0
        self.total_pour = 0
        self.drink_count = 0
        self.enabled = True
        self.calibration = 0 #2.25
        self.cal_input = 0
        self.ml_in_a_pint = 473.176
        self.ml_in_an_oz = 29.5735
        self.to_ml = 0
        self.last_pour_oz = 0
        self.last_pour_time = 0
        self.pour_event_occured = False
        self.last_clicks = 0
        self.hertz = 0

    #This doesn't get called anymore, currently defunct.
    #User will input the calibration
    #Approximately this should be between 2 and 2.5 ml per click for most sensors.
    def calibrate(self, cal_input):
        print "Please measure your last pour in ml, and then enter the volume:"
        print "Hint: The bigger the pour, the more accurate the calibration."
        #cal_input = yield ###raw_input("> ")
        if self.cal_input == '':
            print "You didn't input anything, please try again."
            self.cal_input = 0
        elif self.cal_input.isdigit() != True: #This doesn't seem to work for floats.
            print "That is not a number. Please retry the calibration."
            self.cal_input = 0
        else:
            self.calibration = (float(self.cal_input) / self.last_pour)
            print self.calibration, "ml in a click."
            return self.calibration

    #GPIO detects the rising edge, and updates the current count.
    #Find the time of the last click. This will calculate Hertz.
    #The unfortunate thing is it ignores the first click to make sure the Hz control works.
    def update(self):
        self.click_control = max(((time.time()* 1000.0) - self.last_click_time), 1)
        self.hertz = (1000 / self.click_control)
        if (self.hertz > 5 and self.hertz < 100):
            self.click_count = self.click_count + 1
        else:
            self.last_click_time = int(time.time() * 1000.0)
        print "Last click was found at", self.last_click_time

    #If no clicks are found in the last 20 seconds, record the clicks as a last pour.
    #Reset click count for next pour.
    def last_pour_func(self):
        if (self.click_count == 0):
            pass
        elif (time.time() - (self.last_click_time / 1000) > 15):
            self.last_pour = self.click_count
            self.last_clicks = self.click_count
            self.click_count = 0
            self.last_pour_time = time.ctime()
            if (self.calibration == 0):
                self.calibration = 1
            #Call this to update our volumes and totals in one go.
            self.update_all()
            return self.last_pour
        else:
            print "Waiting for pour to finish."

    #Update all of these in one call.
    def update_all(self):
        self.last_pour_in_ml()
        self.last_pour_in_oz()
        #self.store_total_clicks() don't really need this.
        self.last_click_time = time.time()
        self.pour_event_occured = True #Use this to update our database lazily.
        self.count_drinks()

    #Store the total click count to update keg volume.
    def store_total_clicks(self):
        self.total_pour = self.last_pour + self.total_pour
        return self.total_pour

    #We can use this to determine how many beers total were had.
    def count_drinks(self):
        self.drink_count = self.drink_count + 1
        print self.drink_count, "drinks total."
        return self.drink_count

    #Store the last pour in ml
    def last_pour_in_ml(self):
        self.to_ml = (self.last_pour * self.calibration)
        print self.to_ml, "ml poured at", self.calibration, "ml per click."
        return self.to_ml

    #Store the last pour in OZ
    def last_pour_in_oz(self):
        self.last_pour_oz = ((self.last_pour * self.calibration) / self.ml_in_an_oz)
        print self.last_pour_oz, "oz poured."
        return self.last_pour_oz
