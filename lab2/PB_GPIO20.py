import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(21, GPIO.OUT)
GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

print("Light should be on unless button is pushed")

while True:

  if(GPIO.input(18) ==1):
    GPIO.output(21, False)
    print("Button pushed - Light off")
  else:
    GPIO.output(21, True)

