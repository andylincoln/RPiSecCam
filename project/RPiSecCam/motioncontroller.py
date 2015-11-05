# motioncontroller.py
# Andy Lincoln
# RPiSecCam

import RPi.GPIO as GPIO
import picamera
import time
from datetime import datetime

class MotionController:

    motion_pin = 26

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.motion_pin, GPIO.IN)

        self.camera = picamera.PiCamera()

    def __del__(self):
        self.camera.close()

    def detector(self):
        return GPIO.input(self.motion_pin)

    def capturePhoto(self):
        self.camera.capture( '../photos/' + str(datetime.now()) + '.jpg')
