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

    # Returns True if Motion Pin is high
    def motionDetected(self):
        if (GPIO.input(self.motion_pin) == 1):
            return True
        else:
            return False

    def capturePhoto(self):
        self.camera.capture( '../photos/' + str(datetime.now()) + '.jpg')
