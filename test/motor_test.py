import sys
import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False) 
#GPIO.setwarnings(True)
# Set up pins
GPIO.setmode(GPIO.BCM)
#Motor
motor = 14 
button = 27
GPIO.setup(motor, GPIO.OUT)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#if GPIO.input(17) == GPIO.HIGH:
#    state = True
#if GPIO.input(4) == GPIO.HIGH:
#    state = False
while True:
    if GPIO.input(button) == GPIO.HIGH:
        GPIO.output(motor, GPIO.LOW)
    else:
        GPIO.output(motor, GPIO.HIGH) 
   
GPIO.cleanup()
