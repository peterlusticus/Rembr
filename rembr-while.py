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
m1 =7
SPI_CS_PIN = 17
SPI_SDISDO_PIN = 22 # mosi
SPI_CLK_PIN = 23
GPIO.setup(m1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SPI_CS_PIN, GPIO.OUT)
GPIO.setup(SPI_CLK_PIN, GPIO.OUT)
GPIO.setup(SPI_SDISDO_PIN, GPIO.OUT)
GPIO.output(SPI_CLK_PIN, False)
GPIO.output(SPI_SDISDO_PIN, False)
GPIO.output(SPI_CS_PIN, False)

#needle gear
m2 = 8
m2_oben = 10
m2_unten = 12
GPIO.setup(m2, GPIO.OUT)
GPIO.setup(m2_oben, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(m2_unten, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#string pulling thing
m3 = 16
m3_oben = 18
m3_unten = 22
GPIO.setup(m3, GPIO.OUT)
GPIO.setup(m3_oben, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(m3_unten, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#needle storage arm
m4 = 24
m4_oben = 26
m4_unten = 28
GPIO.setup(m4, GPIO.OUT)
GPIO.setup(m4_oben, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(m4_unten, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#maschien head
m5_right = 24
m5_left = 30
m5_oben = 26
GPIO.setup(m5_right, GPIO.OUT)
GPIO.setup(m5_left, GPIO.OUT)
GPIO.setup(m5_oben, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(m5_unten, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#String cutting knife
m6 = 24
m6_oben = 26
m6_unten = 28
GPIO.setup(m6, GPIO.OUT)
GPIO.setup(m6_oben, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(m6_unten, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#Unterfadenwächter
ufw = 28
GPIO.setup(ufw, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

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

def adjustMotor(sensor, motor):
    while True:
        if GPIO.input(sensor) == GPIO.HIGH:
            GPIO.output(motor, GPIO.LOW)
        else:
            GPIO.output(motor, GPIO.HIGH)
        
def findPosition():
    adjustMotor(m1, m1_low) #Nadelposition
    adjustMotor(m2_unten, m2) #Getriebe
    adjustMotor(m4_unten, m4) #Nadelarm
    adjustMotor(m3_unten, m3) #Fadenrückholer
    #adjustMotor(m6_unten, m6) #TODO Fadenabschneider  
    return True

def MoveHead_Right(count): #fertig
    for x in range(count):
        if GPIO.input(m5_oben) == GPIO.HIGH:
            GPIO.output(m5_right, GPIO.HIGH)
            time.sleep(.2)
            adjustMotor(m5_unten, m5_right)
            time.sleep(.1)
        else:
            GPIO.output(m5_right, GPIO.HIGH)
            time.sleep(.2)
            adjustMotor(m5_oben, m5_right)
            time.sleep(.1)

def MoveHead_Left(count): #fertig
    for x in range(count):
        if GPIO.input(m5_oben) == GPIO.HIGH:
            GPIO.output(m5_left, GPIO.HIGH)
            time.sleep(.2)
            adjustMotor(m5_unten, m5_left)
            time.sleep(.1)
        else:
            GPIO.output(m5_left, GPIO.HIGH)
            time.sleep(.2)
            adjustMotor(m5_oben, m5_left)
            time.sleep(.1)

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

def setM1(b):
    b = "0000" "00" "{0:010b}".format(b)
    GPIO.output(SPI_CS_PIN, False)
    for x in b:
        GPIO.output(SPI_SDISDO_PIN, int(x))
        GPIO.output(SPI_CLK_PIN, True)
        GPIO.output(SPI_CLK_PIN, False)
    time.sleep(.1)
    GPIO.output(SPI_CS_PIN, True)
    time.sleep(.1)

def softStart(): #fertig
    print("[WARN] Ihnen bleiben 10 Sekunden um den Motor zu starten")
    time.sleep(10)
    print("[WARN] Nun muss der Motor auf hochtouren laufen, der GCODE wird nun ausgeführt")
    # while True:
    #     for i in range(0, 100, 10):
    #         print 'set_value:' + str(i)
    #         setM1(i)
    #         time.sleep(.1)

def embroideryStart(): #fertig
    softStart()
    return True

def softStop(): #fertig
    print("[WARN] Ihnen bleiben 10 Sekunden um den Motor zu stoppen")
    time.sleep(10)
    print("[WARN] Nun muss der Motor aus sein")
    # while True:
    #     for i in range(100, 0, 10):
    #         print 'set_value:' + str(i)
    #         setM1(i)
    #         time.sleep(.1)

def embroideryStop(): #fertig
    softStop()
    adjustMotor(m1, m1_low) #Nadelposition
    adjustMotor(m2_unten, m2) #Getriebe
    adjustMotor(m4_unten, m4) #Nadelarm
    print("[WARN] Ihnen bleiben 20 Sekunden um den Faden abzuschneiden")
    time.sleep(20)
    print("[WARN] Nun muss Faden abgeschnitten sein")
    #cutRope()
    return True

def change2StartColor(): #fertig
    MoveHead_Left(color_before)
    color_before = 0
    adjustMotor(m5_unten, m5)


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

print("[INFO] Der Dateiname ist: " + str(color_list)) #nur zum Test, ob der filename = "grün.txt" oder nur "grün" ist (wichtig für "ColorConverter()")
time.sleep(5)
execute()
GPIO.cleanup()
exit()
