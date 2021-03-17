import sys
import time
import RPi.GPIO as GPIO

# Set up pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)



while True:
    if GPIO.input(27) == GPIO.HIGH:
        print("geschlossen")
    else:
        print ("offen")
    
GPIO.cleanup()
