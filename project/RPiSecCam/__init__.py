#
# Andy Lincoln
#

import time
import threading
import notificationcontroller
import lightcontroller
import motioncontroller
import logging
import signal

logging.basicConfig(filename='../log/RasPiSecCam.log',
                    filemode='w',
                    level=logging.DEBUG, datefmt='%m-%d %h:%M')
logging.info("RPiSecCam by Andy Lincoln")

class Thread(threading.Thread):
    def __init__(self, t, *args):
        threading.Thread.__init__(self, target=t, args=args)
        self.setDaemon(True)
        self.start()

def bootNotifCtrl():
    notificationController = notificationcontroller.NotificationController()
    logging.debug('Notification Controller booted successfully')

def bootLightCtrl():
    lightController = lightcontroller.LightController()
    time.sleep(2)
    logging.debug('Light Controller booted successfully')

    # If everythings working fine, show green light, otherwise red
    error = False

def bootMotionCtrl():
    motionController = motioncontroller.MotionController()
    logging.debug('Motion Controller booted successfully')
    #TODO If motion is detected, take picture


"""Entry point for the application script"""
def main():

    threads=[]

    lightThread = Thread(bootLightCtrl)
    motionThread = Thread(bootMotionCtrl)
    notifThread = Thread(bootNotifCtrl)

    threads.append(lightThread)
    threads.append(motionThread)
    threads.append(notifThread)

    logging.debug("Booting controllers")

    while(True):
        try:

            time.sleep(1)

        except KeyboardInterrupt:
            for thread in threads:
                thread.join()
            quit()
main()

