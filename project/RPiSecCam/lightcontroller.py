# LightController.py
# Andy Lincoln
# RPiSecCam
import RPi.GPIO as GPIO
import pykka
from time import sleep

GREEN_LIGHT=18
RED_LIGHT=23
PURPLE_LIGHT=24
lights = [GREEN_LIGHT,RED_LIGHT,PURPLE_LIGHT]

class LightController(pykka.ThreadingActor):

    def on(self,light):
        GPIO.output(light, True)

    def off(self,light):
        GPIO.output(light, False)

    def normal(self):
        self.off(RED_LIGHT)
        self.on(GREEN_LIGHT)

    def error(self):
        self.off(self.GREEN_LIGHT)
        self.on(self.RED_LIGHT)

    def __init__(self):
        super(LightController, self).__init__()

    def on_start(self):

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(lights, GPIO.OUT, initial=GPIO.LOW)

        for light in lights:
            self.on(light)
        sleep(2)
        for light in lights:
            self.off(light)

    def on_stop(self):
        for light in lights:
            self.off(light)

    def on_receive(self, message):
        if (message == { 'msg' : "NORMAL"}):
            self.normal()
        elif (message == { 'msg' : "ERROR"}):
            self.error()









