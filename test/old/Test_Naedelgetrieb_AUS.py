import RPi.GPIO as GPIO
import time

#Define and set up Pins
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


#needle gear
m2 = 8
s1 = 10
s2 = 12
GPIO.setup(m2, GPIO.OUT)
GPIO.setup(s1, GPIO.IN)
GPIO.setup(s2, GPIO.IN)
 
 def check():
    #TODO
    a = True
    if GPIO.input(m1): #Stickmotor aus
        a=False
        if GPIO.input(nps): #Stickmotor in der richtigen Position um eine Farbe zu wechseln
            a=True
            if GPIO.input(s5): #Nadelarm Unten "Farbe ausgewählt"
                a=True
               
    else:
        printn" fehler in zuarbeitungs Motore"
    

#Nadelgetriebe soll von der "AN" Position in die "AUS" Position bewegt werden
def needleGear(on):
    if GPIO.input(s1):
        print"Nadelgetriebe: Startpositionssensor erreicht...Motor an"
        GPIO.output(m2, GPIO.HIGH)
        time.sleep(delay)
    if GPIO.input(s2, GPIO.HIGH):
        print"Nadelgetriebe: Endpositionssensor erreicht... Motor aus"
        GPIO.output(m2, GPIO.LOW)
        time.sleep(delay)

if(check()):
    needleGear(on)
    
