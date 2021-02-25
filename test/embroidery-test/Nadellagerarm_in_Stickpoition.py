import RPi.GPIO as GPIO
import time

#Define and set up Pins
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#needle storage arm
m4 = 24
s5 = 26
s6 = 28
GPIO.setup(m4, GPIO.OUT)
GPIO.setup(s5, GPIO.IN)
GPIO.setup(s6, GPIO.IN)

 def check():
    #TODO
    a = True
    if GPIO.input(m1): #Stickmotor aus
        a=False
        if GPIO.input(nps): #Stickmotor in der richtigen Position um eine Farbe zu wechseln
            a=True
            if GPIO.input(s5): #Nadelarm Unten "Farbe ausgewählt"
                a=True
               if GPIO.input(s2): #Nadelgetriebe aus
                   a=True
                   if GPIO.input(s3) #freeRope = Fadenrückholöse bedindet sich ausgefahren (ist berreit einen nächsten Farbwechsel auszuführen)
    else:
        printn" fehler in zuarbeitungs Motore"
    return a


#Die Nadelkasette mit dem "Nadellagerarm" aus dem Lager in die Stickposition fahren

def NeedleStorageArm(down):
    if GPIO.input(s6, GPIO.HIGH):
        GPIO.output(m4, GPIO.HIGH)
        time.sleep(delay)
    if GPIO.input(s5, GPIO.HIGH):
        GPIO.output(m4, GPIO.LOW)
        time.sleep(delay)
    else:
        print("[NeedleStorageArm_down] Error","Motor ine einer falschen Position")

if(check()):
    NeedleStorage(down)