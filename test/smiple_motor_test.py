import sys
import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
motor = 15
GPIO.setmode(GPIO.BCM)
GPIO.setup(motor, GPIO.OUT)

onoff = float(input("1 for on or 0 for off. "))

if onoff == 1:
    GPIO.output(motor, GPIO.HIGH)
if onoff == 0:
    GPIO.output(motor, GPIO.LOW)
    
else:
    print("Invalid")
    
GPIO.cleanup