#!/usr/bin/python
# https://wikifactory.com/@jonbull/video-motion-control/v/6d817f1/file/README.md

import threading
from threading import Lock, Thread
import time
from time import sleep
import RPi.GPIO as GPIO

xdir = 13
xpul = 11
xena = 15
ydir = 21
ypul = 19
yena = 23
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
motorPins = [
    ypul,
    ydir,
    yena,
    xpul,
    xdir,
    xena,
    ]
for pin in motorPins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)
lock = Lock()
sem = threading.Semaphore()
pul_delay = 0.001
GPIO.output(xena, GPIO.HIGH)
print '[INIT] CNC-initialization completed'

#Global var's
filename = 'test.txt'
dir_left = GPIO.HIGH
dir_right = GPIO.LOW

#Move X-Stepper
def X(lock, steps):
    if steps > 0:
        #left
        GPIO.output(xena, GPIO.HIGH)
        sleep(.5)  # pause due to a possible change direction
        startTime = time.time()
        GPIO.output(xdir, dir_left)
        for x in range(steps):
            GPIO.output(xpul, GPIO.HIGH)
            sleep(pul_delay)
            GPIO.output(xpul, GPIO.LOW)
            sleep(pul_delay)
            sem.acquire()
            x += 1
            sem.release()
        endTime = time.time()
        sleep(.5)  # pause for possible change direction
        timeDuration = endTime - startTime
        return
    elif steps < 0:
        #right
        GPIO.output(xena, GPIO.HIGH)
        sleep(.5)  # pause due to a possible change direction
        startTime = time.time()
        GPIO.output(xdir, dir_right)
        for x in range(steps):
            GPIO.output(xpul, GPIO.HIGH)
            sleep(pul_delay)
            GPIO.output(xpul, GPIO.LOW)
            sleep(pul_delay)
            sem.acquire()
            x += 1
            sem.release()
        endTime = time.time()
        sleep(.5)  # pause for possible change direction
        timeDuration = endTime - startTime
        return

#Move Y-Stepper
def Y(lock, steps):
    if steps > 0:
        #left
        GPIO.output(yena, GPIO.HIGH)
        sleep(.5)  # pause due to a possible change direction
        startTime = time.time()
        GPIO.output(ydir, dir_left)
        for x in range(steps):
            GPIO.output(ypul, GPIO.HIGH)
            sleep(pul_delay)
            GPIO.output(ypul, GPIO.LOW)
            sleep(pul_delay)
            sem.acquire()
            x += 1
            sem.release()
        endTime = time.time()
        sleep(.5)  # pause for possible change direction
        timeDuration = endTime - startTime
        return
    elif steps < 0:
        #right
        GPIO.output(yena, GPIO.HIGH)
        sleep(.5)  # pause due to a possible change direction
        startTime = time.time()
        GPIO.output(ydir, dir_right)
        for x in range(steps):
            GPIO.output(ypul, GPIO.HIGH)
            sleep(pul_delay)
            GPIO.output(ypul, GPIO.LOW)
            sleep(pul_delay)
            sem.acquire()
            x += 1
            sem.release()
        endTime = time.time()
        sleep(.5)  # pause for possible change direction
        timeDuration = endTime - startTime
        return

#Open steps-file and execute the steps
def run():
        with open(filename) as file:
                for line in file:
                        if "X" and "Y" in line:
                                #Split g-code line into "xsteps" and "ysteps"
                                xsteps = (line.split(' ')[1])
                                xsteps = (xsteps[1:])
                                ysteps = (line.split(' ')[1])
                                ysteps = (ysteps[1:])
                                #Maßstab einrechnen
                                xsteps = xsteps*100
                                ysteps = ysteps*100
                                #Start threading
                                lock = threading.Lock()
                                t1 = threading.Thread(target=X, args=(lock, int(xsteps)))
                                t2 = threading.Thread(target=Y, args=(lock, int(ysteps)))
                                t1.start()
                                t2.start()
                                t1.join()
                                t2.join()
                                time.sleep(1)
                                

#Call run method
if __name__ == '__main__':
    run()
