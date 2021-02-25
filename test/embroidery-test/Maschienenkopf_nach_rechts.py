import RPi.GPIO as GPIO
import time

#Define and set up Pins
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#maschien head 
m5 = 24
s7 = 26
s8 = 28
GPIO.setup(m5, GPIO.OUT)
GPIO.setup(s7, GPIO.IN)
GPIO.setup(s6, GPIO.IN)

def check():
    #TODO
    a = True
    if GPIO.input(s6): #Nadelarm oben 
        a=True
            if GPIO.input(m1): #Stickmotor aus
            a=False
                if GPIO.input(nps): #Stickmotor in der richtigen Position um eine Farbe zu wechseln
                    a=True
                        if GPIO.input(s1): #Nadelgtreibe aus
                        a=True
    else:
        a=False
    return a

#Move head right
def MoveHead_Right(count):
    count = -count
    for x in range(count):
        if GPIO.input(s7), 
            GPIO.output(m5, GPIO.HIGH)
            time.sleep(delay)
        if GPIO.input(s8):
            GPIO.output(m5, GPIO.LOW)
            time.sleep(delay)
        else:
            print("[MoveHead_Right] Error")

if(check()):
    MoveHead_Right(1)