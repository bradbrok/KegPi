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
    drink_count = 0
    time_now = 0
    calibration = 0
    ml_per_click = 3 #This parameter inherits from calibration method.
    oz_per_click = 0.08454
    ml_in_a_pint = 473.176
    ml_in_an_oz = 29.5735
    to_ml = 0
    last_pour_time = 0

    #Initialize all_the_things.jpg!!!
    def __init__(self):
        self.click_count = 0
        self.last_click_time = 0
        self.this_pour = 0
        self.last_pour = 0
        self.last_pour_time = 0
        self.total_pour = 0
        self.drink_count = 0
        self.enabled = True
        self.calibration = 0
        self.ml_per_click = self.calibration
        self.oz_per_click = 0.08454
        self.ml_in_a_pint = 473.176
        self.ml_in_an_oz = 29.5735
        self.to_ml = 0
        self.last_pour_time = 0

    #User will input the calibration
    #Need to add logic to detect if user doesn't eneter proper calibration.
    def calibrate(self):
        if (self.calibration > 0):
            print "Calibrated", self.calibration
        else:
            print "Please measure your last pour in ml, and then enter the volume:"
            print "Hint: The bigger the pour, the more accurate the calibration."
            cal_input = raw_input("> ")
            if cal_input == '':
                print "You didn't input anything, please try again."
                cal_input = 0
            elif cal_input.isdigit() != True: #This doesn't seem to work for floats.
                print "That is not a number. Please retry the calibration."
                cal_input = 0
            else:
                self.calibration = (float(cal_input) / self.last_pour)
                print self.calibration, "ml in a click."

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
        if (self.click_count == 0):
            time.sleep(1)
            print "Nothing to do yet."
            self.last_pour_func()
        elif (time.time() - self.last_click_time > 5):
            self.last_pour = self.click_count
            self.click_count = 0
            print "Last pour was", self.last_pour, " clicks."
            print "Click count reset to: ", self.click_count
            self.last_pour_time = time.time()
            if (self.calibration == 0):
                self.calibrate()
            else:
                print "Do nothing"
            #Call this to update our volumes and totals in one go.
            self.update_all()
            return self.last_pour
        else:
            print "Nothing happened."
            time.sleep(1)
            self.last_pour_func()

    #Update all of these in one call.
    def update_all(self):
        self.last_pour_in_ml()
        self.last_pour_in_oz()
        self.store_total_clicks()
        self.count_drinks()


    #Store the total click count to update keg volume.
    def store_total_clicks(self):
        self.total_pour = self.last_pour + self.total_pour
        return self.total_pour

    #We can use this to determine how many beers total were had.
    def count_drinks(self):
        self.drink_count = self.drink_count =+ 1
        print self.drink_count, "drinks total."
        return self.drink_count

    #Store the last pour in ml
    def last_pour_in_ml(self):
        if self.calibration == 0:
            print "Please calibrate by calling calibrate() method first."
        else:
            self.to_ml = (self.last_pour * self.calibration)
            print self.to_ml, "ml poured."
            return self.to_ml

    #Store the last pour in OZ
    def last_pour_in_oz(self):
        if self.calibration == 0:
            print "Please calibrate by calling calibrate() method first."
        else:
            self.last_pour_oz = ((self.last_pour * self.calibration) / self.ml_in_an_oz)
            print self.last_pour_oz, "oz poured."
            return self.last_pour_oz

