import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while(True):
    print("wait")
    GPIO.wait_for_edge(sensor, GPIO.RISING)
    print("click")

GPIO.cleanup()