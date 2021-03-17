import sys
import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
m5_right = 26
m5_left = 15
GPIO.setmode(GPIO.BCM)
GPIO.setup(m5_left, GPIO.OUT)
GPIO.setup(m5_right, GPIO.OUT)


#print("TURN RIGHT")
#GPIO.output(m5_right, GPIO.HIGH)
#time.sleep(1)
#GPIO.output(m5_right, GPIO.LOW)
#time.sleep(.4)

print("TURN LEFT")
GPIO.output(m5_left, GPIO.HIGH)
time.sleep(.5)
print("END")
GPIO.output(m5_left, GPIO.LOW)

GPIO.cleanup
