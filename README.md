# RPiSecCam
A motion-activated security camera framework for Raspberry Pi's

In my final semester of college I took an Internet of Things course focused around creating smart device prototypes with Raspberry Pi's.
For my project, I decided to create a motion-activated security camera that notifies users of activity in their home.

## The Hardware
- Raspberry Pi B+
- Raspberry Pi Camera module
- PIR Motion Sensor
- WiFi adapter
- Adafruit FONA 808 GSM module (with antenna and battery)
- Breadboard
- LED lights
- Jumper Wires

# The Software
- Python language
- RPi.GPIO library for interfacing with the Pi's breadboard
- Pykka library for threading 
- MySQL database

## Abstract
Smart security cameras are really useful. Plug them in, attach them to your WiFi and you have an internet-connected watchdog just for you.
But what if your internet goes out? You lose your watchdog. Have a cabin in the woods? Home internet connections, if available,
might not be up to par. SMS alerts over a cellular network solves that problem, with high availability and reliability to get those alerts in time.
Perhaps you want both for redundancy's sake.

The RPiSecCam aims to solve that problem.

- The system can be armed and disarmed via a text message
- When armed, if motion is detected, a photo is taken.

## More Information
For more info on this project you can view my slideshow [here](https://docs.google.com/presentation/d/1_HyxDdqjYmLZSFyykjzSTuMqAKqHB3Q7sk9VWebv18w/edit?usp=sharing)
