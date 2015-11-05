import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

LIGHT=18

GPIO.setup(LIGHT, GPIO.OUT)

try:
  while True:
    GPIO.output(LIGHT, True)
    print("Lights should be on")
    time.sleep(3)

    GPIO.output(LIGHT, False)
    print("Lights off")
    time.sleep(3)

except:
	pass
finally:
	GPIO.cleanup()
