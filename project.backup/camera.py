#!/usr/bin/env python
# Andy Lincoln
# 91.350 Internet of Things
# Lab 2
# 09/29/2015

import picamera

from datetime import datetime
from time import sleep

camera = picamera.PiCamera()

camera.start_preview()

try:
    for i in range(100):
        camera.brightness = i
        sleep(0.2)

        camera.capture( str(datetime.now()) + '.jpg')
finally:
    camera.stop_preview()
    camera.close()

