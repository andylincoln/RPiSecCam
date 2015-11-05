#
# Andy Lincoln
#

import time
import threading
import notificationcontroller
import lightcontroller
import motioncontroller

def bootNotifCtrl():
    return notificationcontroller.NotificationController()
def bootLightCtrl():
    return lightcontroller.LightController()
def bootMotionCtrl():
    return motioncontroller.MotionController()

def main():

    """Entry point for the application script"""

    print("RPiSecCam by Andy Lincoln")
    print("Booting controllers")

    lightCtrl = bootLightCtrl()
    print ("Light Controller Booted Successfully")
    time.sleep(2)
    notifCtrl = bootNotifCtrl()
    print("Notification Controller Booted Successfully")

    motionCtrl = bootMotionCtrl()
    print ("Motion Controller Booted Successfully")

    print ("Taking Picture!")
    motionCtrl.capturePhoto()
    print ("Done!")
main()
