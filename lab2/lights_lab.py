#!/usr/bin/env python
# Andy Lincoln
# 91.350 Internet of Things
# Lab 2
# 09/13/2015

import RPi.GPIO as GPIO
from time import sleep

lights = [16,20,21]
buttons = [18,23]


def setup():
	
	GPIO.setmode(GPIO.BCM)	
	GPIO.setup(lights, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(buttons, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)	
	
def on(light):
	GPIO.output(light, True)

def off(light):
	GPIO.output(light, False)

def cycle():
	print "Testing the lights!"
	try: 
		for val,light in enumerate(lights):
			on(light)
			print "Light #{} (PIN {}) on!".format(val + 1, light)
			sleep(1) 
			off(light)
			print "Light #{} (PIN {}) off!".format(val + 1, light)
			sleep(1) 
	except KeyboardInterrupt:
		print "\nCTRL-C detected, Shutting down"

def toggle():
	try:
		lit_led_index = 0
		on(lights[lit_led_index])
		while True:
			
			state_btn1 = GPIO.input(buttons[0])		
			state_btn2 = GPIO.input(buttons[1])		
		
			if (state_btn1): 

				off(lights[lit_led_index])
				sleep(0.1)

				lit_led_index = abs((lit_led_index - 1) % 3)
				on(lights[lit_led_index])
				sleep(0.1)
				print "Light #{}".format(lit_led_index + 1) 	
			
			if (state_btn2):
       			
		                off(lights[lit_led_index])
	                        sleep(0.1)
				lit_led_index = abs((lit_led_index + 1) % 3)
	                        on(lights[lit_led_index])
	              		sleep(0.1)
				print "Light #{}".format(lit_led_index + 1) 	
	
	except KeyboardInterrupt:
		print "\nCTRL-C detected, Shutting down"
	finally:
		GPIO.cleanup()

setup()
cycle()
toggle()


