#Depending librarys
import RPi.GPIO as GPIO
import time
import os, sys
import spidev

#Global var's
filename = 'test.txt'
dir_left = GPIO.HIGH
dir_right = GPIO.LOW
delay = 0.1
path = "/files/"
color_list = os.listdir( path )
dir_left = GPIO.HIGH
dir_right = GPIO.LOW
color_before = 0
#Define and set up Pins
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
#X-Axis
xdir = 13
xpul = 11
xena = 15
GPIO.setup(xdir, GPIO.OUT)
GPIO.setup(xpul, GPIO.OUT)
GPIO.setup(xena, GPIO.OUT)
#Y-Axis
ydir = 21
ypul = 19
yena = 23
GPIO.setup(ydir, GPIO.OUT)
GPIO.setup(ypul, GPIO.OUT)
GPIO.setup(yena, GPIO.OUT
#big needle motor 24V
#analog to digital converter controls digital potentiometer conrols motor speed = msc
#needle position sensor = nps
m1 =3
msc =5
nps =7
GPIO.setup(m1, GPIO.OUT)
GPIO.setup(msc, GPIO.OUT)
GPIO.setup(nps, GPIO.IN)
#needle gear
m2 = 8
s1 = 10
s2 = 12
GPIO.setup(m2, GPIO.OUT)
GPIO.setup(s1, GPIO.IN)
GPIO.setup(s2, GPIO.IN)
#string pulling thing
m3 = 16
s3 = 18
s4 = 22
GPIO.setup(m3, GPIO.OUT)
GPIO.setup(s3, GPIO.IN)
GPIO.setup(s4, GPIO.IN)
#needle storage arm
m4 = 24
s5 = 26
s6 = 28
GPIO.setup(m4, GPIO.OUT)
GPIO.setup(s5, GPIO.IN)
GPIO.setup(s6, GPIO.IN)
#maschien head 
m5 = 24
s7 = 26
s8 = 28
GPIO.setup(m5, GPIO.OUT)
GPIO.setup(s7, GPIO.IN)
GPIO.setup(s6, GPIO.IN)
#String cutting knife
m6 = 24
s9 = 26
s10 = 28
GPIO.setup(m6, GPIO.OUT)
GPIO.setup(s9, GPIO.IN)
GPIO.setup(s10, GPIO.IN)        
#Unterfadenwächter (Frage: der wird nirgendwo verwendet, soll das so sein?)
ufw = 28
GPIO.setup(ufw, GPIO.IN)



#----------------------------------HELP-METHODS----------------------------------
#STICKEN
def findPosition(): #TODO: m6 (Fadenabschneider) ansteuern und methode beenden
    while(GPIO.input(s1, GPIO.LOW)): #Nadelposition
        GPIO.output(m1, GPIO.HIGH)
    if(GPIO.input(m2_s1, GPIO.HIGH)): #Getriebe
        GPIO.output(m2, GPIO.HIGH)
        if(GPIO.input(m2_s2, GPIO.HIGH)): 
            GPIO.input(m2, GPIO.LOW)
    else:
        print("[ERROR] m2 Position")
    if(GPIO.input(m4_s1, GPIO.HIGH)): #Nadelarm
        GPIO.output(m4, GPIO.HIGH)
        if(GPIO.input(m4_s2, GPIO.HIGH)):
            GPIO.input(m4, GPIO.LOW)
    else:
        print("[ERROR] m2 Position")
    if(GPIO.input(m3_s1, GPIO.HIGH)): #Fadenrückholer
        GPIO.output(m3, GPIO.HIGH)
        if(GPIO.input(m3_s2, GPIO.HIGH)):
            GPIO.input(m3, GPIO.LOW)
    else:
        print("[ERROR] m2 Position")
    
    if(GPIO.input(m6_s1, GPIO.HIGH)): #Fadenabschneider TODO
        GPIO.output(m6, GPIO.HIGH)
        if(GPIO.input(m6_s2, GPIO.HIGH)):
            GPIO.input(m6, GPIO.LOW)
    else:
        print("[ERROR] m2 Position")
    return True

def MoveHead_Right(count): #TODO: Motorverkabelung für Rechts-Links bewegung (Die polarität muss getauscht werden, um die richtung zu ändern)
    for x in range(count):
        if GPIO.input(s7), 
            GPIO.output(m5, GPIO.HIGH)
            time.sleep(delay)
        if GPIO.input(s8):
            GPIO.output(m5, GPIO.LOW)
            time.sleep(delay)

def MoveHead_Left(count): #TODO: Motorverkabelung für Rechts-Links bewegung (Die polarität muss getauscht werden, um die richtung zu ändern)
    for x in range(count):
        if GPIO.input(s7), 
            GPIO.output(m5, GPIO.HIGH)
            time.sleep(0.1)
        if GPIO.input(s8):
            GPIO.output(m5, GPIO.LOW)
            time.sleep(0.1)

def changeColor(color): #fertig
    color_idx = int(color)
    diff = color_idx - color_before
    if diff > 0 :
        MoveHead_Left(diff)
    if diff < 0 :
        diff = -diff
        MoveHead_Right(diff)
    color_before = color_idx
    return True

def softStart(): #fertig
    print("[WARN] Ihnen bleiben 10 Sekunden um den Motor zu starten")
    time.sleep(10)
    print("[WARN] Nun muss der Motor auf hochtouren laufen, der GCODE wird nun ausgeführt")

def embroideryStart(): #fertig
    softStart()
    return True

def softStop(): #fertig
    print("[WARN] Ihnen bleiben 10 Sekunden um den Motor auzuschalten")
    time.sleep(10)
    print("[WARN] Nun muss der Motor komplett ausgeschaltet sein")

def findEndPosition(): #fertig (Frage: das macht das selbe wie die funktion dannach, soll das so sein?)
   softStop()
   while(GPIO.input(s1, GPIO.LOW)):
        GPIO.output(m1, GPIO.HIGH)

def embroideryStop(): #fertig
    while(GPIO.input(s1, GPIO.HIGH)): #Frage: hieß der sensor vorher nps?
        GPIO.output(m1, GPIO.HIGH)
    while(GPIO.input(s2, GPIO.LOW)):
        GPIO.output(m2, GPIO.HIGH)
    while(GPIO.input(s4, GPIO.LOW)):
        GPIO.output(m4, GPIO.HIGH)
    while(GPIO.input(s2, GPIO.LOW)): #vorher in eigener funktion "cutRope()"
        GPIO.output(m6, GPIO.HIGH)
    return True

def change2StartColor(): #fertig
    MoveHead_Left(color_before)
    color_before = 0
    while(GPIO.input(s5, GPIO.LOW)): #checken, ob es wirklich in der startposition ist
        GPIO.output(m5, GPIO.HIGH)


#CNC
def X(Fsteps,Bsteps): #fertig
        GPIO.output(xena, GPIO.HIGH)
        for i in range(Fsteps):
            XSTEP(dir_left)
        for i in range(Bsteps):
            XSTEP(dir_right)
        GPIO.output(xena, GPIO.LOW)
     
def Y(Fsteps, Bsteps): #fertig
        GPIO.output(yena, GPIO.HIGH)
        for i in range(Bsteps):
            YSTEP(dir_left)
        for i in range(Fsteps):
            YSTEP(dir_right)
        GPIO.output(yena, GPIO.LOW)

def XSTEP(dir): #fertig
    GPIO.output(xdir, dir)
    GPIO.output(xpul, GPIO.HIGH)
    time.sleep(0.009)
    GPIO.output(xpul, GPIO.LOW)
    time.sleep(0.009)

def YSTEP(dir): #fertig
    GPIO.output(ydir, dir)
    GPIO.output(ypul, GPIO.HIGH)
    time.sleep(0.009)
    GPIO.output(ypul, GPIO.LOW)
    time.sleep(0.009)

def JOG(Axis, Delta): #fertig
    if Delta > 0:
            Axis(abs(Delta),0)
    elif Delta < 0:
            Axis(0,abs(Delta))

def LIFR(filename): #fertig
        with open(filename) as file:
                for line in file:
                        if "X" and "Y" in line:
                                Gx = (line.split(' ')[1])
                                Gx = (Gx[1:])
                                JOG(X,int(Gx))

                                Gy = (line.split(' ')[2])
                                Gy = (Gy[1:])
                                Gy = Gy.replace('.','')
                                JOG(Y,int(Gy))
        GPIO.output(xena, GPIO.HIGH)
        GPIO.output(yena, GPIO.HIGH)

def CncStart(color): #fertig
    LIFTR(color+".txt")
    return True



#----------------------------------MAIN-METHODS----------------------------------
def printColor(color):
    if(findPosition()): #fertig
        print("[INFO] Nadel oben") 
        if(changeColor(color)): #fertig
            print("[INFO] Zur ersten Farbe gewechselt")
            if(embroideryStart()): #fertig
                print("[INFO] Sticken gestartet/Langsam angelaufen")
                if(CncStart(color)):  #fertig
                    print("[INFO] GCODE erfolgreich ausgeführt")
                    if(findEndPosition()): #fertig
                        print("[INFO] Langsam ausgelaufen")
                        if(embroideryStop()): #fertig
                            print("[INFO] Sticken beendet")

def execute(): #fertig
    if(ColorConverter()): #TODO: 
        for color in color_list:
            print(color) #nur zum Test, ob color = "1.txt" oder nur "1" ist (wichtig für den filename in "CncStart()")
            time.sleep(5)
            printColor(color)
    if(change2StartColor()): #fertig
        print("[INFO] Zur Ausgangsfarbe gewechselt")

execute()