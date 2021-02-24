#Depending librarys
import RPi.GPIO as GPIO
import time

#Global var's
filename = 'test.txt'
dir_left = GPIO.HIGH
dir_right = GPIO.LOW
color_list = ["schwarz","weiß","orange","lila","beige","blau","gelb","grün"]

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
    if GPIO.input(s2, GPIO.HIGH):
        GPIO.output(m2, GPIO.HIGH)
    
    if GPIO.input(s1, GPIO.HIGH):
        GPIO.output(m2, GPIO.LOW)

#disengage needle gear 
def NeedleGear_disengage():
    if GPIO.input(s1, GPIO.HIGH):
         GPIO.output(m2, GPIO.HIGH)
    if GPIO.input(s2, GPIO.HIGH):
        GPIO.output(m2, GPIO.LOW)
    else:
        print("needle gear Motor at a wrong position")


#move Needle Storage Arm up
def NeedleStorageArm_up():
    if GPIO.input(s5, GPIO.HIGH):
        GPIO.output(m4, GPIO.HIGH)
    if GPIO.input(s6, GPIO.HIGH):
    GPIO.output(m4, GPIO.LOW)


#move Needle Storage Arm down
def NeedleStorageArm_down():
    if GPIO.input(s6, GPIO.HIGH):
        GPIO.output(m4, GPIO.HIGH)
    if GPIO.input(s5, GPIO.HIGH):
        GPIO.output(m4, GPIO.LOW)


#cut Rope under needle
def cutRope():
    if GPIO.input(s9, GPIO.HIGH):
        GPIO.output(m6, GPIO.HIGH)
    if GPIO.input(s10, GPIO.HIGH):
        GPIO.output(m6, GPIO.LOW)
    else:
        print("rope Motor is at a wrong position")


#free Rope after cuting  
def free_Rope():  
    if GPIO.input(s3, GPIO.HIGH):
        GPIO.output(m3, GPIO.HIGH)
    if GPIO.input(s4, GPIO.HIGH):
        GPIO.output(m3, GPIO.LOW)
        
    if GPIO.input(s4, GPIO.HIGH):
        GPIO.output(m3, GPIO.HIGH)
    if GPIO.input(s3, GPIO.HIGH):
         GPIO.output(m3, GPIO.LOW)


#Move head right
def MoveHead_Right():
    if GPIO.input(s7, GPIO.HIGH), 
        GPIO.output(m5, GPIO.HIGH)
    if GPIO.input(s8, GPIO.HIGH):
        GPIO.output(m5, GPIO.LOW)

#Move Head left
def MoveHead_Left():
    if GPIO.input(s7, GPIO.HIGH), 
        GPIO.output(m5, GPIO.HIGH)
        if GPIO.input(s8, GPIO.HIGH):
            GPIO.output(m5, GPIO.LOW)


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

    color_befor_change = 0 
    for idx, color in color_list:
        idx=idx++
        color_idx = idx
        diff = color_befor_change - color_idx
        if diff > 0 :
            for x in range(diff):
                Move Head left()
        if diff < 0 :
            diff = -diff
            for x in range(diff):
                MoveHead_Right()
        color_befor_change = idx

    NeedleStorageArm_down()
    needleGear_engage()
    msc #TODO m1 low speed 3x rotations

    if nps #needle in up position:
        #TODO

#Start embroidery
def embroideryStart()
    #TODO
