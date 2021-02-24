#Depending librarys
import RPi.GPIO as GPIO
import time
import os, sys

#Global var's
filename = 'test.txt'
dir_left = GPIO.HIGH
dir_right = GPIO.LOW
delay = 0.1
path = "/files/"
color_list = os.listdir( path )
all_color_list = ["schwarz","weiß","orange","lila","beige","blau","gelb","grün"]
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

#Unterfadenwächter
wfw = 28
GPIO.setup(ufw, GPIO.IN)

#----------------------------------HELP-METHODS----------------------------------
#Excecute the count of x-steps
def X(Fsteps,Bsteps):
        GPIO.output(xena, GPIO.HIGH)
        for i in range(Fsteps):
            XSTEP(dir_left)
        for i in range(Bsteps):
            XSTEP(dir_right)
        GPIO.output(xena, GPIO.LOW)
            
#Excecute the count of y-steps
def Y(Fsteps, Bsteps):
        GPIO.output(yena, GPIO.HIGH)
        for i in range(Bsteps):
            YSTEP(dir_left)
        for i in range(Fsteps):
            YSTEP(dir_right)
        GPIO.output(yena, GPIO.LOW)

#Make a step on the x-axis
def XSTEP(dir):
    GPIO.output(xdir, dir)
    GPIO.output(xpul, GPIO.HIGH)
    time.sleep(0.009)
    GPIO.output(xpul, GPIO.LOW)
    time.sleep(0.009)

#Make a step on the y-axis
def YSTEP(dir):
    GPIO.output(ydir, dir)
    GPIO.output(ypul, GPIO.HIGH)
    time.sleep(0.009)
    GPIO.output(ypul, GPIO.LOW)
    time.sleep(0.009)

#Define axis and directions (call X() or Y() functions)
def JOG(Axis, Delta):
    if Delta > 0:
            Axis(abs(Delta),0)
    elif Delta < 0:
            Axis(0,abs(Delta))

#Open steps-file and execute the steps
def LIFR(filename):
        with open(filename) as file:
                for line in file:
                        if "X" and "Y" in line:
                                #Split line and call jog-method
                                Gx = (line.split(' ')[1])
                                Gx = (Gx[1:])
                                JOG(X,int(Gx))

                                Gy = (line.split(' ')[2])
                                Gy = (Gy[1:])
                                Gy = Gy.replace('.','')
                                JOG(Y,int(Gy))
        #Turn motor off
        GPIO.output(xena, GPIO.HIGH)
        GPIO.output(yena, GPIO.HIGH)

#engage needle gear
def needleGear_engage():
    if GPIO.input(s2):
        GPIO.output(m2, GPIO.HIGH)
        time.sleep(delay)
    if GPIO.input(s1, GPIO.HIGH):
        GPIO.output(m2, GPIO.LOW)
        time.sleep(delay)
    else:
        print("[needleGear_engage] Error")

#disengage needle gear 
def NeedleGear_disengage():
    if GPIO.input(s1):
        GPIO.output(m2, GPIO.HIGH)
        time.sleep(delay)
    if GPIO.input(s2):
        GPIO.output(m2, GPIO.LOW)
        time.sleep(delay)
    else:
        print("[NeedleGear_disengage] needle gear Motor at a wrong position")

#move Needle Storage Arm up
def NeedleStorageArm_up():
    if GPIO.input(s5):
        GPIO.output(m4, GPIO.HIGH)
        time.sleep(delay)
    if GPIO.input(s6):
        GPIO.output(m4, GPIO.LOW)
        time.sleep(delay)
    else:
        print("[NeedleStorageArm_up] Error")

#move Needle Storage Arm down
def NeedleStorageArm_down():
    if GPIO.input(s6, GPIO.HIGH):
        GPIO.output(m4, GPIO.HIGH)
        time.sleep(delay)
    if GPIO.input(s5, GPIO.HIGH):
        GPIO.output(m4, GPIO.LOW)
        time.sleep(delay)
    else:
        print("[NeedleStorageArm_down] Error")

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

#Move Head left
def MoveHead_Left(count):
    for x in range(count):
        if GPIO.input(s7), 
            GPIO.output(m5, GPIO.HIGH)
            time.sleep(delay)
        if GPIO.input(s8):
            GPIO.output(m5, GPIO.LOW)
            time.sleep(delay)
        else:
            print("[MoveHead_Left] Error")

def ColorConverter():
    for filename in enumerate(os.listdir( path )):
        if filename = "schwarz":
            dst = "1" + ".txt"
        if filename = "weiß":
            dst = "2" + ".txt"
        if filename = "orange":
            dst = "3" + ".txt"
        if filename = "lila":
            dst = "4" + ".txt"
        if filename = "beige":
            dst = "5" + ".txt"
        if filename = "blau":
            dst = "6" + ".txt"
        if filename = "gelb":
            dst = "7" + ".txt"
        if filename = "grün":
            dst = "8" + ".txt"
        src = path + filename
        dst = path + dst 
        os.rename(src, dst)

def RefreshColorList():
    color_list = os.listdir( path )

def embroideryStop():
    msc #TODO digital code for high resistance = low motor speed
    two low speed rotations
    nps #TODO the needle must be sensed down
    cutRope()
    msc #TODO low Speed to up position
    GPIO.output(m1, GPIO.LOW)
    free_Rope()
    NeedleGear_disengage()
    NeedleStorageArm_up()

def post():
    NeedleStorageArm_down() #TODO
    needleGear_engage() #TODO

def msc_start():
    #langsam anlaufen
    GPIO.output(msc, GPIO.HIGH) #TODO: Statt GPIO.HIGH - "for loop von langsam zu schnell"

def real_start():
    #voll durchrattern
    GPIO.output(msc, GPIO.HIGH) #TODO: Statt GPIO.HIGH - "ganz schnell"

#Start embroidery
def embroideryStart():
    while ufw:
        msc_start()
        time.sleep(6)
        real_start()

def check():
    #TODO
    a = True
    if GPIO.input(s2):
        a=True
        if GPIO.input(s5):
            a=True
            if GPIO.input(s9):
                a=True
                if GPIO.input(s3):
                    a=True
    else:
        a=False
    return a
#----------------------------------MAIN-METHOD----------------------------------

def execute()
    if(check()):
        #Change color
        prep()
        ColorConverter()
        RefreshColorList()
        color_before = 0
        for color in color_list:
            #Setup color
            color_idx = int(color)
            diff = color_idx - color_before
            if diff > 0 :
                Move Head left(diff)
            if diff < 0 :
                MoveHead_Right(diff)
            color_before = color_idx
            post()
            #Start embroidery
            embroideryStart()
            time.sleep(2)
            #Start gcode-execution
            LIFR(color)
            time.sleep(2)
            #Finish embroidery
            embroideryStop()

        if nps #needle in up position: TODO
            #TODO

execute()

