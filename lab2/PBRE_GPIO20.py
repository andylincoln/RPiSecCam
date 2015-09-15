import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(21, GPIO.OUT)
GPIO.setup(20, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

print("Light transitions will occur on push and release of button")

while True:

  GPIO.output(21, True)

  GPIO.wait_for_edge(20,GPIO.RISING)
  GPIO.output(21, False)
  GPIO.wait_for_edge(20,GPIO.FALLING)

