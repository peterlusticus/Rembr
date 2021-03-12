#Depending librarys
import RPi.GPIO as GPIO
import time
import os, sys
import spidev

#Global var's
path = "/home/pi/Desktop/Rembr-main/cnc"
color_list = os.listdir( path )
color_before = 0
dir_left = GPIO.HIGH
dir_right = GPIO.LOW

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
GPIO.setup(yena, GPIO.OUT)

#big needle motor 24V
#analog to digital converter controls digital potentiometer conrols motor speed = msc
#needle position sensor = nps
m1_slow = 3
m1_middle = 5
m1_fast = 4
m1 =7
GPIO.setup(m1_slow, GPIO.OUT)
GPIO.setup(m1_middle, GPIO.OUT)
GPIO.setup(m1_fast, GPIO.OUT)
GPIO.setup(m1, GPIO.IN)
#needle gear
m2 = 8
m2_oben = 10
m2_unten = 12
GPIO.setup(m2, GPIO.OUT)
GPIO.setup(s2_oben, GPIO.IN)
GPIO.setup(s2_unten, GPIO.IN)
#string pulling thing
m3 = 16
m3_oben = 18
m3_unten = 22
GPIO.setup(m3, GPIO.OUT)
GPIO.setup(s3_oben, GPIO.IN)
GPIO.setup(s3_unten, GPIO.IN)
#needle storage arm
m4 = 24
m4_oben = 26
m4_unten = 28
GPIO.setup(m4, GPIO.OUT)
GPIO.setup(s4_oben, GPIO.IN)
GPIO.setup(s4_unten, GPIO.IN)
#maschien head
m5_right = 24
m5_left = 30
m5_oben = 26
GPIO.setup(m5_right, GPIO.OUT)
GPIO.setup(m5_left, GPIO.OUT)
GPIO.setup(s5_oben, GPIO.IN)
GPIO.setup(s5_unten, GPIO.IN)
#String cutting knife
m6 = 24
m6_oben = 26
m6_unten = 28
GPIO.setup(m6, GPIO.OUT)
GPIO.setup(s6_oben, GPIO.IN)
GPIO.setup(s6_unten, GPIO.IN)        
#Unterfadenwächter
ufw = 28
GPIO.setup(ufw, GPIO.IN)

#----------------------------------HELP-METHODS----------------------------------
#STICKEN
def ColorConverter(): #fertig
    for name in enumerate(os.listdir( path )):
        if(name == "schwarz"):
            dst = "1" + ".txt"
        if(name == "weiß"):
            dst = "2" + ".txt"
        if(name == "orange"):
            dst = "3" + ".txt"
        if(name == "lila"):
            dst = "4" + ".txt"
        if(name == "beige"):
            dst = "5" + ".txt"
        if(name == "blau"):
            dst = "6" + ".txt"
        if(name == "gelb"):
            dst = "7" + ".txt"
        if(name == "grün"):
            dst = "8" + ".txt"
        src = path + name
        dst = path + dst 
        os.rename(src, dst)

def findPosition(): #TODO: m6 (Fadenabschneider) ansteuern und methode beenden
    while(GPIO.input(m1, GPIO.LOW)): #Nadelposition
        GPIO.output(m1_slow, GPIO.HIGH)

    while(GPIO.input(m2_unten, GPIO.LOW)): #Getriebe
        GPIO.output(m2, GPIO.HIGH)
    GPIO.output(m2, GPIO.LOW)

    while(GPIO.input(m4_unten, GPIO.LOW)): #Nadelarm
        GPIO.output(m4, GPIO.HIGH)
    GPIO.output(m4, GPIO.LOW)
    
    while(GPIO.input(m3_unten, GPIO.LOW)): #Fadenrückholer
        GPIO.output(m3, GPIO.HIGH)
    GPIO.output(m3, GPIO.LOW)
    
    while(GPIO.input(m6_unten, GPIO.LOW)): #Fadenabschneider TODO: ist noch unklar, ob es auch zwei schalter gibt, ansonsten schleife wie bei m1
        GPIO.output(m6, GPIO.HIGH)
    GPIO.output(m6, GPIO.LOW)
    
    return True

def MoveHead_Right(count): #fertig
    for x in range(count):
        GPIO.output(m5_right, GPIO.HIGH)
        time.sleep(0.2)
        while(GPIO.input(m5_oben, GPIO.LOW)):
            GPIO.output(m5_right, GPIO.HIGH)
        GPIO.output(m5_right, GPIO.LOW)
        time.sleep(0.7)

def MoveHead_Left(count): #fertig
    for x in range(count):
        GPIO.output(m5_left, GPIO.HIGH)
        time.sleep(0.2)
        while(GPIO.input(m5_oben, GPIO.LOW)):
            GPIO.output(m5_left, GPIO.HIGH)
        GPIO.output(m5_left, GPIO.LOW)
        time.sleep(0.7)

def changeColor(color): #fertig
    color_idx = int(color)
    diff = color_idx - color_before
    if(diff > 0):
        MoveHead_Left(diff)
    if(diff < 0):
        diff = -diff
        MoveHead_Right(diff)
    color_before = color_idx
    return True

def softStart(): #fertig
    print("[WARN] Ihnen bleiben 10 Sekunden um den Motor zu starten")
    time.sleep(10)
    print("[WARN] Nun muss der Motor auf hochtouren laufen, der GCODE wird nun ausgeführt")
    # GPIO.output(m1_slow, GPIO.HIGH)
    # time.sleep(2)
    # GPIO.output(m1_slow, GPIO.LOW)
    # GPIO.output(m1_middle, GPIO.HIGH)
    # time.sleep(2)
    # GPIO.output(m1_middle, GPIO.LOW)
    # GPIO.output(m1_fast, GPIO.HIGH)

def embroideryStart(): #fertig
    softStart()
    return True

def softStop(): #fertig
    print("[WARN] Ihnen bleiben 10 Sekunden um den Motor zu starten")
    time.sleep(10)
    print("[WARN] Nun muss der Motor auf hochtouren laufen, der GCODE wird nun ausgeführt")
    # GPIO.output(m1_fast, GPIO.LOW)
    # GPIO.output(m1_middle, GPIO.HIGH)
    # time.sleep(2)
    # GPIO.output(m1_middle, GPIO.LOW)
    # GPIO.output(m1_slow, GPIO.HIGH)
    # time.sleep(2)
    # GPIO.output(m1_slow, GPIO.LOW)

def cutRope(): #TODO: Sensoren, etc anpassen
    GPIO.output(m1, GPIO.LOW)
    GPIO.output(m6, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(m6, GPIO.LOW)

def embroideryStop(): #fertig
    softStop()
    while(GPIO.input(m1, GPIO.HIGH)):
        GPIO.output(m1_slow, GPIO.HIGH)

    while(GPIO.input(m2_unten, GPIO.LOW)):
        GPIO.output(m2, GPIO.HIGH)
    GPIO.output(m2, GPIO.LOW)
    
    while(GPIO.input(m4_unten, GPIO.LOW)):
        GPIO.output(m4, GPIO.HIGH)
    GPIO.output(m4, GPIO.LOW)
    
    cutRope()
    return True

def change2StartColor(): #fertig
    MoveHead_Left(color_before)
    color_before = 0
    if(GPIO.input(s5_unten, GPIO.LOW)):  #checken, ob es wirklich in der startposition ist
        GPIO.output(m5, GPIO.HIGH)
        if(GPIO.input(s5_unten, GPIO.HIGH)):
            GPIO.input(m5, GPIO.LOW)

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
def printColor(color): #fertig
    if(findPosition()):
        if(changeColor(color)):
            if(embroideryStart()):
                if(CncStart(color)):
                    if(embroideryStop()):
                        return True

def execute(): #fertig
    if(ColorConverter()):
        for color in color_list:
            printColor(color)
    change2StartColor()

print(str(color_list)) #nur zum Test, ob der filename = "grün.txt" oder nur "grün" ist (wichtig für "ColorConverter()")
time.sleep(5)
execute()