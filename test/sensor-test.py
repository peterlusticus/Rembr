import time
import RPi.GPIO as GPIO

# Pins definitions
btn_pin = 21

# Set up pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(btn_pin, GPIO.IN)

# If button is pushed, light up LED
try:
    while True:
        if GPIO.input(btn_pin):
            print("a")
            time.sleep(0.2)
        else:
            print("b")
            time.sleep(0.2)

# When you press ctrl+c, this will be called
finally:
    GPIO.cleanup()
