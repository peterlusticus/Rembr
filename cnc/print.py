#Richard P - 05/02/2021
#This library execute a 2-axis-stepperstep-file on two stepper motor driver
#It supply coordinates in a text file called "test.txt" - file needs specific format: 
#G01 X10 Y15
#G01 X20 Y25

#Depending librarys
import RPi.GPIO as GPIO
import time

#Global var's
filename = 'test.txt'
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
#Needle stick sensor
#nsensor = 26
#GPIO.setup(nsensor, GPIO.IN)

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
def LIFR():
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

#Call "Load Input File and Parse Gcode" LIFTR method
LIFR()

#Turn motor off
GPIO.output(xena, GPIO.HIGH)
GPIO.output(yena, GPIO.HIGH)

exit()