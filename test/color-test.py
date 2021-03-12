import RPi.GPIO as GPIO
import time

#zu dieser Farbe soll es wechseln
# ACHTUNG
# sollte zur 3. Farbe wechseln
# funktioniert nur einmal, dannach musst du mich mal anrufen, bzw. eigentlich nur die color_before=2 setzten und die color=0
# Alle Motoren müssen in der richtigen Position sein, insbesondere der m5 muss oben sein (GPIO.input(m5_oben, GPIO.HIGH))
# 
color = 2

#Define Pins
GPIO.setmode(GPIO.BOARD)
m5_right = 24
m5_left = 30
m5_oben = 26
GPIO.setup(m5_right, GPIO.OUT)
GPIO.setup(m5_left, GPIO.OUT)
GPIO.setup(s5_oben, GPIO.IN)

#Global var's
color_before = 0

#Functions
def MoveHead_Right(count):
    for x in range(count):
        GPIO.output(m5_right, GPIO.HIGH)
        time.sleep(0.2)
        while(GPIO.input(m5_oben, GPIO.LOW)):
            GPIO.output(m5_right, GPIO.HIGH)
        GPIO.output(m5_right, GPIO.LOW)
        time.sleep(0.7)

def MoveHead_Left(count):
    for x in range(count):
        GPIO.output(m5_left, GPIO.HIGH)
        time.sleep(0.2)
        while(GPIO.input(m5_oben, GPIO.LOW)):
            GPIO.output(m5_left, GPIO.HIGH)
        GPIO.output(m5_left, GPIO.LOW)
        time.sleep(0.7)

def changeColor(color):
    color_idx = int(color)
    diff = color_idx - color_before
    if(diff > 0):
        MoveHead_Left(diff)
    if(diff < 0):
        diff = -diff
        MoveHead_Right(diff)
    color_before = color_idx

changeColor(color)

GPIO.cleanup()
