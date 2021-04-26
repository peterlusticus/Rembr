import RPi.GPIO as GPIO
import time

#Mosfet
#Define Pins
channel = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT)

#Main Functions
#Turn motor on
def mos_on(pin):
    GPIO.output(pin, GPIO.HIGH)

#Turn motor off
def mos_off(pin):
    GPIO.output(pin, GPIO.LOW)

mos_on(channel)
time.sleep(1)
mos_off(channel)
