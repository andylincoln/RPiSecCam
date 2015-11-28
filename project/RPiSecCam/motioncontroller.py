# motioncontroller.py
# Andy Lincoln
# RPiSecCam

import RPi.GPIO as GPIO
import picamera
import logging
import time
import pykka
from datetime import datetime
from datetime import date

class MotionController(pykka.ThreadingActor):

    motion_pin = 26

    def __init__(self):
        super(MotionController, self).__init__()

    def on_stop(self):
        self.closeCamera()
        self.camera = None

    def on_failure(self, exception_type, exception_value, traceback):
        logging.error("Error encountered: {type} {value} {traceback}".format(exception_type, exception_value, traceback))

    def on_start(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.motion_pin, GPIO.IN)
        self.camera = picamera.PiCamera()

    def on_receive(self, message):
        if (message == { 'msg' : "IS MOTION DETECTED?"}):
            return self.motionDetected()
        elif (message == { 'msg' : "CAPTURE PHOTO" }):
            return self.capturePhoto()

    def closeCamera(self):
       self.camera._check_camera_open()
       self.camera.close()

    # Returns True if Motion Pin is high
    def motionDetected(self):
        return GPIO.input(self.motion_pin)

    def capturePhoto(self):
        filename =  '../photos/' + (datetime.now().strftime("%m-%d-%y-%I%M%S")) + '.jpg'
        self.camera.capture(filename)
        return filename
