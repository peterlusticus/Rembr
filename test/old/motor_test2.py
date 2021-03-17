import sys
import time
import RPi.GPIO as GPIO
#GPIO.setwarnings(False)
# Set up pins
GPIO.setmode(GPIO.BCM)
#Motor
motor = 18 
switch_up = 13
switch_down = 19 
GPIO.setup(motor, GPIO.OUT)
GPIO.setup(switch_up, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(switch_down, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
    
    if GPIO.input(motor) == GPIO.HIGH:
        state = 1
        print(state)
        #time.sleep(0.2)
    if GPIO.input(switch_down) == GPIO.HIGH:
        state = 2
        print(state)
        #time.sleep(0.2)
    else:
        print("no state")
        #time.sleep(0.2)
        
#while True:
if state == 1:
    GPIO.output(motor, GPIO.HIGH)
if state == 2:
    GPIO.output(motor, GPIO.LOW)
else:
    print(state) 
 
GPIO.cleanup()
