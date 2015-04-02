# KegPi
A Raspberry Pi based keggerator management system that is built on Flask. Just plug in two flow sensors into the GPIO and run the kegpi.py and kegpiapp.py to get started!

Dependencies:
[Flask](https://github.com/mitsuhiko/flask)
[Flask WTForms](https://github.com/lepture/flask-wtf)

This is just a simple solution for a two tap system for the meantime.

Right now there isn't an easy installer for this just yet. So, in order to make this work on your pi, navigate to the KegPi directory and run or create a script:

sudo python kegpi.py & sudo python kegpiapp.py

This will launch both the web app and the data collector.

Materials List:

* A Keggerator, you can buy or build on your own.
* 1 Raspberry Pi (Preferrably a the Pi2 or Model B+).
* [Flow Meter](https://www.adafruit.com/products/828) - I'm using the ones from AdaFruit. Any hall effect flow sensor will work. They just need to be calibrated by going to the admin panel.