# LightController.py
# Andy Lincoln
# RPiSecCam
import RPi.GPIO as GPIO
from time import sleep


class LightController:
    GREEN_LIGHT=18
    RED_LIGHT=23
    PURPLE_LIGHT=24

    lights = [GREEN_LIGHT,RED_LIGHT,PURPLE_LIGHT]

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.lights, GPIO.OUT, initial=GPIO.LOW)
        for light in self.lights:
            self.on(light)
        sleep(1)
        for light in self.lights:
            self.off(light)
        sleep(4)
        self.on(self.GREEN_LIGHT)

    def __del__(self):
        for light in self.lights:
            self.off(light)
        GPIO.cleanup()

    def on(self,light):
        GPIO.output(light, True)

    def off(self,light):
        GPIO.output(light, False)
