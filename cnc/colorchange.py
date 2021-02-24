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
#color_list = ["schwarz","weiß","orange","lila","beige","blau","gelb","grün"]

#Define and set up Pins
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

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

#----------------------------------HELP-METHODS----------------------------------
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
        if GPIO.input(s7, GPIO.HIGH), 
            GPIO.output(m5, GPIO.HIGH)
            time.sleep(delay)
        if GPIO.input(s8, GPIO.HIGH):
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

#----------------------------------MAIN-METHODS----------------------------------
#Change color
def colorChange(color)
    msc #TODO digital code for high resistance = low motor speed
    two low speed rotations
    nps #TODO the needle must be sensed down
    cutRope()
    msc #TODO low Speed to up position
    GPIO.output(m1, GPIO.LOW)
    free_Rope()
    NeedleGear_disengage()
    NeedleStorageArm_up()

    ColorConverter()
    RefreshColorList()

    color_befor_change = 0
    for color in color_list:
        color_idx = int(color)
        diff = color_idx - color_before
        if diff > 0 :
            Move Head left(diff)
        if diff < 0 :
            diff = -diff
            MoveHead_Right(diff)
        color_before = color_idx

    NeedleStorageArm_down()
    needleGear_engage()
    msc #TODO m1 low speed 3x rotations

    if nps #needle in up position:
        #TODO

#Start embroidery
def embroideryStart()
    #TODO
