#Depending librarys
import RPi.GPIO as GPIO
import time
import os, sys
import spidev
import threading

#Global var's
path = "/home/pi/Desktop/Rembr-main/cnc/f"
color_list = os.listdir( path )
color_before = 0
dir_left = GPIO.HIGH
dir_right = GPIO.LOW
m1_start = 30
m1_speed = .3

#Define and set up Pins
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
#X-Axis
xdir = 38
xpul = 36
xena = 40
GPIO.setup(xdir, GPIO.OUT)
GPIO.setup(xpul, GPIO.OUT)
GPIO.setup(xena, GPIO.OUT)
#Y-Axis
ydir = 26
ypul = 24
yena = 32
GPIO.setup(ydir, GPIO.OUT)
GPIO.setup(ypul, GPIO.OUT)
GPIO.setup(yena, GPIO.OUT)

#big needle motor 24V
m1 = 8
s1 = 5
GPIO.setup(s1,GPIO.IN)
GPIO.setup(m1, GPIO.OUT)

#needle gear
m2 = 16
m2_oben = 29
m2_unten = 31
GPIO.setup(m2, GPIO.OUT)
GPIO.setup(m2_oben, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(m2_unten, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#string pulling thing
m3 = 18
m3_oben = 7
m3_unten = 11
GPIO.setup(m3, GPIO.OUT)
GPIO.setup(m3_oben, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(m3_unten, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#needle storage arm
m4 = 22
m4_oben = 19
m4_unten = 21
GPIO.setup(m4, GPIO.OUT)
GPIO.setup(m4_oben, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(m4_unten, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#maschien head
m5_right = 37
m5_left = 10
m5_oben = 13
m5_unten = 15
GPIO.setup(m5_right, GPIO.OUT)
GPIO.setup(m5_left, GPIO.OUT)
GPIO.setup(m5_oben, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(m5_unten, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#String cutting knife
m6 = 12
m6_oben = 33
m6_unten = 35
GPIO.setup(m6, GPIO.OUT)
GPIO.setup(m6_oben, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(m6_unten, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#Unterfadenwächter
#ufw = 28
#GPIO.setup(ufw, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#----------------------------------HELP-METHODS----------------------------------
#STICKEN
def ColorConverter(): #fertig
    for name in color_list:
        print(name)
        if(name == "schwarz.txt"):
            dst = "1" + ".txt"
        if(name == "weiß.txt"):
            dst = "2" + ".txt"
        if(name == "orange.txt"):
            dst = "3" + ".txt"
        if(name == "lila.txt"):
            dst = "2" + ".txt"
        if(name == "beige.txt"):
            dst = "5" + ".txt"
        if(name == "blau.txt"):
            dst = "6" + ".txt"
        if(name == "gelb.txt"):
            dst = "7" + ".txt"
        if(name == "grün.txt"):
            dst = "8" + ".txt"
        src = path+ "/"+ name 
        os.rename(src, path + "/" + dst)

def adjustMotor(sensor, motor):
    print(str(sensor) + "  " + str(motor))
    if GPIO.input(sensor) == GPIO.HIGH:
        GPIO.output(motor, GPIO.LOW)
    else:
        GPIO.output(motor, GPIO.HIGH)
        
def findPosition():
    adjustMotor(s1, m1) #Nadelposition
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
    color_before = int(7)
    color_idx = int(color)
    diff = color_idx - color_before
    print(str(diff) + " Schritte nach drüben")
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
    GPIO.output(8,GPIO.HIGH)
    m1 = GPIO.PWM(8, 100)
    m1.start(1)
    for x in range(0,1):
        for i in range(m1_start,101):
            m1.ChangeDutyCycle(i)
            time.sleep(m1_speed)
            print(i)

def embroideryStart(): #fertig
    softStart()
    return True

def softStop(): #fertig
    GPIO.output(m1,GPIO.HIGH)
    m1 = GPIO.PWM(m1, 100)
    m1.start(1)
    for x in range(0,1):
        for i in range(100,m1_start,-1):
            m1.ChangeDutyCycle(i)
            sleep(m1_speed)
            print(i)

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
        print(filename)
        with open(filename) as file:
                for line in file:
                        if "X" and "Y" in line:
                                Gx = (line.split(' ')[1])
                                Gx = (Gx[1:])
                                Gy = (line.split(' ')[2])
                                Gy = (Gy[1:])
                                Gy = Gy.replace('.','')
                                GPIO.wait_for_edge(s1, GPIO.RISING)
                                JOG(X,int(Gx))
                                JOG(Y,int(Gy))
        GPIO.output(xena, GPIO.HIGH)
        GPIO.output(yena, GPIO.HIGH)

def CncStart(color): #fertig
    LIFR(color+".txt")
    return True

#----------------------------------MAIN-METHODS----------------------------------
def startthread(color):
    embroidery = threading.Thread(target=embroideryStart)
    cnc = threading.Thread(target=CncStart, args=[color])
    embroidery.start()
    time.sleep(0.002)
    cnc.start()
    embroidery.join()
    cnc.join()

def printColor(color): #fertig
    if(findPosition()):
        if(changeColor(color)):
            startthread(color)
            time.sleep(100000)
            return True

def execute(): #fertig
    ColorConverter()
    color_list = os.listdir( path )
    for color in color_list:
        color = color[0:1]
        printColor(color)
    change2StartColor()

print(str(color_list)) #nur zum Test, ob der filename = "1.txt" oder nur "1" ist (wichtig für "CncStart()")
time.sleep(.5)
execute()
GPIO.cleanup()
exit()