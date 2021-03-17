import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) 
#Motor
GPIO.setup(23, GPIO.OUT)

GPIO.cleanup()