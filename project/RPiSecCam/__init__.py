#
# Andy Lincoln
#

import time
import notificationcontroller
import lightcontroller
import motioncontroller
import logging
import RPi.GPIO as GPIO

logging.basicConfig(filename='../log/RPiSecCam.log',
                    filemode='w',
                    level=logging.DEBUG, datefmt='%m-%d %h:%M')
logging.info("RPiSecCam by Andy Lincoln")



"""Entry point for the application script"""
ARMED = False
MSG_ARM     = {'msg' : "ARM"}
MSG_DISARM  = {'msg' : "DISARM"}
MSG_ERROR   = {'msg' : "ERROR"}
MSG_NORMAL  = {'msg' : "NORMAL"}
MSG_IS_MOTION_DETECTED = { 'msg' : "IS MOTION DETECTED?"}

logging.debug("Booting controllers")
notif_ref = notificationcontroller.NotificationController.start()
light_ref = lightcontroller.LightController().start()
motion_ref = motioncontroller.MotionController().start()

ACTOR_REFS=[light_ref, motion_ref, notif_ref]

notif_proxy = notif_ref.proxy()
light_proxy   = light_ref.proxy()
motion_proxy = motion_ref.proxy()

PROXIES=[notif_proxy, light_proxy, motion_proxy]

# Start the program with everything normal
light_ref.tell(MSG_NORMAL)
counter = 0
while(True):
    try:
        counter = counter + 1
        if counter < 5 :
            ARMED = True
        else:
            ARMED = False
        #Check for text message saying ARM if so, set ARMED to True


        # If system is armed, check for motion, if motion detected, take picture
        logging.debug("Checking if armed")
        if (ARMED):
            logging.debug("Armed, waiting for motion")
            motionDetected = motion_ref.ask(MSG_IS_MOTION_DETECTED, block=True)
            if (motionDetected):
                logging.debug("Motion detected, taking photo!")
                photoFilename = motion_ref.ask(MSG_CAPTURE_PHOTO, block=True).get()
                logging.debug("Photo taken! Filename is {filename}".format(filename=photoFilename))
            else:
                logging.debug("Found nothing, going to sleep")
                time.sleep(30)
        else:
            logging.debug("Not Armed")
            time.sleep(30)

    except KeyboardInterrupt:
        for actor in ACTOR_REFS:
            actor.stop()
        GPIO.cleanup()
        quit()
