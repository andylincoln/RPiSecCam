import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

LIGHT1=16
LIGHT2=21

GPIO.setup(LIGHT1, GPIO.OUT)
GPIO.setup(LIGHT2, GPIO.OUT)

try: 
  while True:
    GPIO.output(LIGHT1, True)
    GPIO.output(LIGHT2, True)
    print("Lights should be on")
    time.sleep(3)
 
    GPIO.output(LIGHT1, False)
    GPIO.output(LIGHT2, False)
    print("Lights off")
    time.sleep(3)

except:
	pass
finally:
	GPIO.cleanup()
