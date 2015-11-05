# Andy Lincoln
# 91.350 Internet of Things
# Raspberry Pi Security System
# 10/15/15

import RPi.GPIO as GPIO
from time import sleep

light=20

def setup():

	GPIO.setmode(GPIO.BCM)
	GPIO.setup(light, GPIO.OUT, initial=GPIO.LOW)

def on(light):
	GPIO.output(light, True)

def off(light):
	GPIO.output(light, False)

try:
    setup()
    on(light)
    sleep(10)
#    off(light)
finally:
    GPIO.cleanup()
