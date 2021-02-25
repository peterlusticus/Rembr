#Depending librarys
import RPi.GPIO as GPIO
import time

#Define and set up Pins
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


#string pulling thing
m3 = 16
s3 = 18
s4 = 22
GPIO.setup(m3, GPIO.OUT)
GPIO.setup(s3, GPIO.IN)
GPIO.setup(s4, GPIO.IN)

def check():
    #TODO
    a = True
    if GPIO.input(nps): #Nadel oben
        a=True
        if GPIO.output(1):
            a=False
           
    else:
        a=False
    return a
    
#free Rope after cuting  
def free_Rope():  
    if GPIO.input(s3):
        GPIO.output(m3, GPIO.HIGH)
        time.sleep(delay)
    if GPIO.input(s4):
        GPIO.output(m3, GPIO.LOW)
        time.sleep(delay)
     if GPIO.input(s4):
        GPIO.output(m3, GPIO.HIGH)
        time.sleep(delay)
    if GPIO.input(s3):
        GPIO.output(m3, GPIO.LOW)
        time.sleep(delay)
    else:
        print("[free_Rope] Error")

if(check()):
    free_Rope()