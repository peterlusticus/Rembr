#!/usr/bin/python
# https://wikifactory.com/@jonbull/video-motion-control/v/6d817f1/file/README.md

import threading
from threading import Lock, Thread
import time
from time import sleep
import RPi.GPIO as GPIO

# startTime = none
# endTime = none

m1PUL = 17  # Pulse
m1DIR = 27  # Controller Direction
m1ENA = 22  # Controller Enable
m2PUL = 6
m2DIR = 13
m2ENA = 19
m3PUL = 12
m3DIR = 16
m3ENA = 20
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
motorPins = [
    m1PUL,
    m1DIR,
    m1ENA,
    m2PUL,
    m2DIR,
    m2ENA,
    m3PUL,
    m3DIR,
    m3ENA,
    ]

# SET MOTORPINS AS OUTPUT

for pin in motorPins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)
print 'Initialization Completed'
lock = Lock()
sem = threading.Semaphore()
durationFwd = 80000  # This is the duration of the motor spinning. used for forward direction
durationBwd = 40000  # This is the duration of the motor spinning. used for reverse direction
durationRotate = 3200
durationRotate2 = 800
print 'Duration Fwd set to ' + str(durationFwd)
print 'Duration Bwd set to ' + str(durationBwd)
delay = 0.0001  # This is actualy a delay between PUL pulses - effectively sets the mtor rotation speed.
delay2 = 0.01
delay3 = 0.01
print 'Speed set to ' + str(delay)
GPIO.output(m1ENA, GPIO.HIGH)
GPIO.output(m2ENA, GPIO.HIGH)
GPIO.output(m3ENA, GPIO.HIGH)


# --- MAIN TIMER TEST ---

def m1forward(lock):
    GPIO.output(m1ENA, GPIO.HIGH)
    sleep(.5)  # pause due to a possible change direction
    startTime = time.time()
    GPIO.output(m1DIR, GPIO.LOW)
    print 'm1DIR set to LOW - Moving Forward at ' + str(delay)
    print 'Controller m1PUL being driven.'
    for x in range(durationFwd):
        GPIO.output(m1PUL, GPIO.HIGH)
        sleep(delay)
        GPIO.output(m1PUL, GPIO.LOW)
        sleep(delay)
        sem.acquire()
        x += 1
        sem.release()
    endTime = time.time()
    sleep(.5)  # pause for possible change direction
    timeDuration = endTime - startTime
    print timeDuration
    return


def m2forward(lock):
    GPIO.output(m2ENA, GPIO.HIGH)
    sleep(.5)  # pause due to a possible change direction
    startTime = time.time()
    GPIO.output(m2DIR, GPIO.LOW)
    print 'm2DIR set to LOW - Moving Forward at ' + str(delay2)
    print 'Controller m2PUL being driven.'
    for x in range(durationRotate):
        GPIO.output(m2PUL, GPIO.HIGH)
        sleep(delay2)
        GPIO.output(m2PUL, GPIO.LOW)
        sleep(delay2)
        sem.acquire()
        x += 1
        sem.release()
    endTime = time.time()
    sleep(.5)  # pause for possible change direction
    timeDuration = endTime - startTime
    print timeDuration


def m3forward(lock):
    GPIO.output(m3ENA, GPIO.HIGH)
    sleep(.5)  # pause due to a possible change direction
    startTime = time.time()
    GPIO.output(m3DIR, GPIO.LOW)
    print 'm3DIR set to LOW - Moving Forward at ' + str(delay3)
    print 'Controller m3PUL being driven.'
    for x in range(durationRotate2):
        GPIO.output(m3PUL, GPIO.HIGH)
        sleep(delay3)
        GPIO.output(m3PUL, GPIO.LOW)
        sleep(delay3)
        sem.acquire()
        x += 1
        sem.release()
    endTime = time.time()
    sleep(.5)  # pause for possible change direction
    timeDuration = endTime - startTime
    print timeDuration


def main_task():
    lock = threading.Lock()
    t1 = threading.Thread(target=m1forward, args=(lock, ))
    t2 = threading.Thread(target=m2forward, args=(lock, ))
    t3 = threading.Thread(target=m3forward, args=(lock, ))
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()


if __name__ == '__main__':
    # creating thread
    main_task()
    print 'Done!'
