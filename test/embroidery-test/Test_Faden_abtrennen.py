#Depending librarys
import RPi.GPIO as GPIO
import time

#Define and set up Pins
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


def check():
    #TODO
    a = True
    if GPIO.input(nps): #Nadelgetriebe in der Untenposition der Nadel
        a=False
        if GPIO.input(s1): #Nadelgetriebe AN    S2 Nadelgetriebe AUS
            a=True
            if GPIO.input(s5): #Nadelarm Unten "Farbe ausgewählt"
                a=True
                if GPIO.input(s3):
                    a=True
    else:
        printn" fehler in zuarbeitungs Motore"
    return a

#nach einem Abgeschlossenen Stickvorgang mus der Faden durchtrennt werden, um in eine neue Farbe wechseln zu können
#cut Rope under needle
def cutRope():
    if GPIO.input(s9, GPIO.HIGH):
        GPIO.output(m6, GPIO.HIGH)
        time.sleep(delay)
    if GPIO.input(s10, GPIO.HIGH):
        GPIO.output(m6, GPIO.LOW)
        time.sleep(delay)
    else:
        print("[cutRope] rope Motor is at a wrong position")

if (check()):
    cutRope()


