import RPi.GPIO as GPIO
import time
import os, sys
import threading

#Global var's
path = "/home/pi/Desktop/Rembr-main/cnc/"
color_list = os.listdir(path)
color_before = 0
m1_start = 30
m1_speed = .1
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
m1 = 7
s1 = 5
GPIO.setup(s1,GPIO.IN)
GPIO.setup(m1, GPIO.OUT)
GPIO.output(m1,GPIO.HIGH)
m1 = GPIO.PWM(m1, 100)
m1.start(1)

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
def colorConverter():
    for name in color_list:
        if(name == "schwarz.txt"):
            dst = "1.txt"
        if(name == "weiß.txt"):
            dst = "2.txt"
        if(name == "orange.txt"):
            dst = "3.txt"
        if(name == "lila.txt"):
            dst = "4.txt"
        if(name == "beige.txt"):
            dst = "5.txt"
        if(name == "blau.txt"):
            dst = "6.txt"
        if(name == "gelb.txt"):
            dst = "7.txt"
        if(name == "grün.txt"):
            dst = "8.txt"
        src = path + "/" + name
        dst = path + "/" + dst
        os.rename(src, dst)
    global color_list
    color_list = os.listdir(path)
    print("[INFO]\tFunction ColorConverter():\t executed successfully")

def adjustMotor(sensor, motor):
    GPIO.output(motor, GPIO.HIGH)
    GPIO.wait_for_edge(sensor, GPIO.RISING)
    GPIO.output(motor, GPIO.LOW)
        
def checkPosition():
    adjustMotor(s1, m1) #Nadelposition
    adjustMotor(m2_unten, m2) #Getriebe
    adjustMotor(m4_unten, m4) #Nadelarm
    adjustMotor(m3_unten, m3) #Fadenrückholer
    #adjustMotor(m6_unten, m6) #TODO Fadenabschneider  
    print("[INFO]\tFunction checkPosition():\t executed successfully")

def moveHead_Right(count):
    #TODO: m5_oben so ausrichten, dass der Sensor an ist, wenn die Richtige Postion erreicht wurde
    for x in range(count):
        GPIO.output(m5_right, GPIO.HIGH)
        time.sleep(.2)
        adjustMotor(m5_oben, m5_right)

def moveHead_Left(count):
    #TODO: m5_oben so ausrichten, dass der Sensor an ist, wenn die Richtige Postion erreicht wurde
    for x in range(count):
        GPIO.output(m5_left, GPIO.HIGH)
        time.sleep(.2)
        adjustMotor(m5_oben, m5_left)

def changeColor(color):
    #TODO: int()'s mit letzten Version vergleichen
    color_idx = color[0:1]
    diff = int(color_idx) - int(color_before)
    print("[INFO]\tFunction changeColor():\t diff=" + str(diff))
    if(diff > 0):
        moveHead_Left(diff)
    if(diff < 0):
        diff = -diff
        moveHead_Right(diff)
    global color_before
    color_before = color_idx
    print("[INFO]\tFunction changeColor():\t executed successfully")

def softStart(): #GLEICH
    for x in range(0,1):
        for i in range(m1_start,101):
            m1.ChangeDutyCycle(i)
            sleep(m1_speed)

def embroideryStart(): #GLEICH
    softStart()
    print("[INFO]\tFunction embroideryStart():\t executed successfully")

def softStop(): #GLEICH
    for x in range(0,1):
        for i in range(100,m1_start,-1):
            m1.ChangeDutyCycle(i)
            sleep(m1_speed)

def embroideryStop():
    softStop()
    adjustMotor(s1, m1) #Nadelposition
    adjustMotor(m2_unten, m2) #Getriebe
    adjustMotor(m4_unten, m4) #Nadelarm
    print("[WARN]\tFunction embroideryStop():\t Ihnen bleiben 30 Sekunden um den Faden abzuschneiden")
    time.sleep(35)
    print("[INFO]\tFunction embroideryStop():\t executed successfully")
    #cutRope()

def change2StartColor():
    moveHead_Left(color_before)
    global color_before
    color_before = 0

#CNC
def x(Fsteps,Bsteps):
        GPIO.output(xena, GPIO.HIGH)
        for i in range(Fsteps):
            xstep(dir_left)
        for i in range(Bsteps):
            xstep(dir_right)
        GPIO.output(xena, GPIO.LOW)
     
def y(Fsteps, Bsteps):
        GPIO.output(yena, GPIO.HIGH)
        for i in range(Bsteps):
            ystep(dir_left)
        for i in range(Fsteps):
            ystep(dir_right)
        GPIO.output(yena, GPIO.LOW)

def xstep(dir):
    GPIO.output(xdir, dir)
    GPIO.output(xpul, GPIO.HIGH)
    time.sleep(0.009)
    GPIO.output(xpul, GPIO.LOW)
    time.sleep(0.009)

def ystep(dir):
    GPIO.output(ydir, dir)
    GPIO.output(ypul, GPIO.HIGH)
    time.sleep(0.009)
    GPIO.output(ypul, GPIO.LOW)
    time.sleep(0.009)

def jog(Axis, Delta):
    if Delta > 0:
            Axis(abs(Delta),0)
    elif Delta < 0:
            Axis(0,abs(Delta))

def lifr(filename):
        with open(filename) as file:
                for line in file:
                        if "X" and "Y" in line:
                                Gx = (line.split(' ')[1])
                                Gx = (Gx[1:])
                                Gy = (line.split(' ')[2])
                                Gy = (Gy[1:])
                                Gy = Gy.replace('.','')
                                GPIO.wait_for_edge(s1, GPIO.RISING)
                                jog(x,int(Gx))
                                jog(y,int(Gy))
        GPIO.output(xena, GPIO.HIGH)
        GPIO.output(yena, GPIO.HIGH)

def cncStart(color):
    lifr(color)
    return True

def printColor(color):
    checkPosition()
    changeColor(color)
    embroidery = threading.Thread(target=embroideryStart)
    cnc = threading.Thread(target=cncStart, args=[color])
    embroidery.start()
    time.sleep(.2)
    cnc.start()
    embroidery.join()
    cnc.join()

#----------------------------------MAIN-METHOD----------------------------------
def execute():
    colorConverter()
    for color in color_list:
        printColor(color)
    change2StartColor()

execute()
GPIO.cleanup()
exit()